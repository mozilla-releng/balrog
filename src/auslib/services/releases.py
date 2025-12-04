import asyncio
import logging
from collections import defaultdict
from copy import deepcopy

from aiohttp import ClientError
from deepmerge import Merger
from flask import current_app as app
from sentry_sdk import capture_exception
from sqlalchemy import join, select

from auslib.services import releases
from auslib.util.versions import MozillaVersion

from ..blobs.base import createBlob
from ..errors import PermissionDeniedError, ReadOnlyError, SignoffRequiredError
from ..global_state import cache, dbo
from ..util.data_structures import ensure_path_exists, get_by_path, infinite_defaultdict, set_by_path
from ..util.signoffs import serialize_signoff_requirements
from ..util.timestamp import getMillisecondTimestamp

log = logging.getLogger(__file__)

store = object()


def await_coroutines(coros):
    # We use `asyncio.run` to wait on the results of a number of coroutines below.
    # `asyncio.gather` cannot be used directly with it, so we need to wrap it in
    # a coroutine.
    async def coroutine_gather(*args, **kwargs):
        return await asyncio.gather(*args, **kwargs)

    results = asyncio.run(coroutine_gather(*coros, return_exceptions=True))
    for r in results:
        if isinstance(r, Exception):
            # aiohttp exceptions indicate a failure uploading to GCS, which don't warrant
            # sending an error back to the client.
            if isinstance(r, ClientError):
                capture_exception(r)
            else:
                raise r

    return results


# fmt: off
APP_RELEASE_ASSETS = {
    "platforms": {
        "*": {
            "locales": {
                "*": store
            }
        }
    }
}
RELEASE_BLOB_ASSETS = {
    1: APP_RELEASE_ASSETS,
    2: APP_RELEASE_ASSETS,
    3: APP_RELEASE_ASSETS,
    4: APP_RELEASE_ASSETS,
    5: APP_RELEASE_ASSETS,
    6: APP_RELEASE_ASSETS,
    7: APP_RELEASE_ASSETS,
    8: APP_RELEASE_ASSETS,
    9: APP_RELEASE_ASSETS,
}
# fmt: on


release_merger = Merger(
    [
        # Merge dictionaries
        (dict, ["merge"])
    ],
    # Overwrite values for any other type
    ["override"],
    # Overwrite values for type mismatches
    ["override"],
)


def separate_base_blob(blob, assets_keys):
    """Split a full or partial Release into two separate dictionaries containing the base in one,
    and the assets in the other.

        :param blob: The Release to split
        :type blob: dict

        :param assets_keys: The keys that should end up in the `assets`.
        :type assets_keys: dict

        :return: tuple of base (dict) and assets (dict)
        :rtype: tuple
    """
    base = {}

    for k, v in blob.items():
        # If none of this key's value belongs in assets, put everything in the base and move on
        if not assets_keys or (k not in assets_keys and "*" not in assets_keys):
            base[k] = v
            continue

        assets_value = assets_keys.get(k) or assets_keys["*"]
        # If this key's entire value belongs in assets, nothing to do!
        if assets_value == store:
            continue

        # Otherwise, split the value and store both results
        # TODO: walrus me when pycodestyle supports it
        # if base_data := separate_base_blob(v, assets_value):
        base_data = separate_base_blob(v, assets_value)
        if base_data:
            base[k] = base_data

    return base


def separate_assets(blob, assets_keys, path=()):
    """Separate the assets of a Release into individual parts according to the structure provided in "asset_keys".
    :Example:

    Given the following arguments:
    assets: {
        "platforms": {
            "WINNT_x86_64-msvc": {
                "locales": {
                    "af": {
                        "buildID": "123456789",
                        "completes": [...],
                        "partials": [...],
                    }
                    "de": {
                        "buildID": "123456789",
                        "completes": [...],
                        "partials": [...],
                    }
                }
            }
        }
    }
    asset_keys: {
        "platforms": {
            "*": {
                "locales": {
                    "*": store
                }
            }
        }
    }

    This function will yield these items:
    (("platforms", "WINNT_x86_64-msvc", "locales", "af"), {"buildID": "123456789", "completes": [...], "partials": [...]})
    (("platforms", "WINNT_x86_64-msvc", "locales", "de"), {"buildID": "123456789", "completes": [...], "partials": [...]})

    :param assets: Release data that contains one or more parts not considered part of the "base" Release.
    :type assets: dict

    :param asset_keys: A deeply nested dictionary containing information about how assets are split. Dictionary values may be
                       either another dictionary, or a "store" object, which is a sentinel value that indicates that the current
                       nesting level represents one asset, and any values beneath it stored as is as part of that asset.
    :type asset_keys: dict or "store" sentinel value

    :param path:
    :type path: tuple

    :return: yields tuples of (path, assets), where path is the path in the dict that the assets are associated with,
             and assets are a dict of details
    :rtype: tuple of (tuple, dict)
    """
    if assets_keys == store:
        yield (path, blob)
        # Short circuit, because we don't need to iterate over something
        # we're going to store in its own row.
        return

    for k, v in blob.items():
        if k in assets_keys or "*" in assets_keys:
            newpath = (*path, k)
            yield from separate_assets(v, assets_keys.get(k) or assets_keys["*"], newpath)


def split_release(blob, schema_version):
    """Split a full or partial Release into its base object and list of assets objects.

    :param blob: The Release to split
    :type blob: auslib.blobs.base.Blob

    :param schema_version: The schema version of the blob. Because this function can handle
                           splitting partial Releases (eg: just "platforms"), this must be passed
                           because it may not exist in the blob.
    :type schema_version: int

    :return: A tuple whose first item is the parts of the blob that are part of the "base", and whose second item
             is a list of non-base assets. This list contains tuples whose first item is the path to the asset, relative
             to the root of the base (eg: ("platforms", "WINNT_x86_64-msvc", "locales", "en-US")), and whose second
             item is a dict of the contents of that asset.
    :rtype: tuple of (dict, list of tuples)
    """
    assets_keys = RELEASE_BLOB_ASSETS.get(schema_version, {})

    base = separate_base_blob(blob, assets_keys)
    assets = [p for p in separate_assets(blob, assets_keys)]

    return base, assets


def get_schema_version(name, trans):
    # Set a constant name for the returned column. Otherwise this will end up as "anon_1", with no guarantee
    # that it won't change in the future.
    column = dbo.releases_json.data["schema_version"]
    label = column.label("schema_version")
    return dbo.releases_json.select(where={"name": name}, columns=[label], transaction=trans)[0]["schema_version"]


def exists(name, trans):
    if dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.name], transaction=trans):
        return True

    return False


def sc_exists(name, trans):
    if any(
        [
            dbo.releases_json.scheduled_changes.select(
                where={"base_name": name, "complete": False}, columns=[dbo.releases_json.scheduled_changes.base_name], transaction=trans
            ),
            dbo.release_assets.scheduled_changes.select(
                where={"base_name": name, "complete": False}, columns=[dbo.release_assets.scheduled_changes.base_name], transaction=trans
            ),
        ]
    ):
        return True

    return False


def is_read_only(name, trans):
    return dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.read_only], transaction=trans)[0].get("read_only")


def get_assets(name, trans):
    assets = {}
    for asset in dbo.release_assets.select(where={"name": name}, transaction=trans):
        assets[asset["path"]] = asset

    return assets


def get_release_names(trans, product=None):
    where = {}
    if product:
        where["product"] = product

    return sorted([r["name"] for r in dbo.releases_json.select(columns=[dbo.releases_json.name], where=where, transaction=trans)])


def get_releases(trans, args=None):
    if args is None:
        args = {}

    if args.get("names_only"):
        return get_release_names(trans)

    releases = dbo.releases_json.select(
        columns=[dbo.releases_json.name, dbo.releases_json.product, dbo.releases_json.data_version, dbo.releases_json.read_only], transaction=trans
    )

    j = join(dbo.releases_json.t, dbo.rules.t, ((dbo.releases_json.name == dbo.rules.mapping) | (dbo.releases_json.name == dbo.rules.fallbackMapping)))
    rule_mappings = trans.execute(select([dbo.releases_json.name, dbo.rules.rule_id, dbo.rules.product, dbo.rules.channel]).select_from(j)).fetchall()

    rule_mappings_by_name = defaultdict(list)
    for ref in rule_mappings:
        rule_mappings_by_name[ref[0]].append(ref)

    product_required_signoffs = {}
    for row in releases:
        refs = rule_mappings_by_name.get(row["name"], [])
        row["rule_info"] = {str(ref[1]): {"product": ref[2], "channel": ref[3]} for ref in refs}
        row["scheduled_changes"] = []
        row["required_signoffs"] = serialize_signoff_requirements(
            [obj for v in dbo.releases_json.getPotentialRequiredSignoffs([row], transaction=trans).values() for obj in v]
        )
        if row["product"] not in product_required_signoffs:
            product_required_signoffs[row["product"]] = serialize_signoff_requirements(
                dbo.releases_json.getPotentialRequiredSignoffsForProduct(row["product"], transaction=trans)["rs"]
            )
        row["product_required_signoffs"] = product_required_signoffs[row["product"]]

    for table in (dbo.releases_json.scheduled_changes, dbo.release_assets.scheduled_changes):
        for sc in table.select(where={"complete": False}, transaction=trans):
            release = [r for r in releases if r["name"] == sc["base_name"]]
            if release:
                release = release[0]
            else:
                release = {
                    "name": sc["base_name"],
                    "product": None,
                    "data_version": None,
                    "read_only": None,
                    "rule_info": {},
                    "scheduled_changes": [],
                }

            munged_sc = {"signoffs": {}}
            for k in sc:
                if k == "base_data":
                    continue
                elif k == "data_version":
                    munged_sc["sc_data_version"] = sc[k]
                else:
                    munged_sc[k.replace("base_", "")] = sc[k]

            for signoff in table.signoffs.select(where={"sc_id": sc["sc_id"]}, transaction=trans):
                munged_sc["signoffs"][signoff["username"]] = signoff["role"]

            release["scheduled_changes"].append(munged_sc)

            if release not in releases:
                releases.append(release)

    return {"releases": sorted(releases, key=lambda r: r["name"])}


def get_base_row(name, trans):
    row = dbo.releases_json.select(where={"name": name}, transaction=trans)
    if row:
        return row[0]

    return None


def get_base_data_version(name, trans):
    row = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.data_version], transaction=trans)
    if row:
        return row[0]["data_version"]

    return None


def get_asset_rows(name, trans):
    return dbo.release_assets.select(where={"name": name}, order_by=[dbo.release_assets.path], transaction=trans) or []


def get_asset_data_versions(name, trans):
    return (
        dbo.release_assets.select(where={"name": name}, columns=[dbo.release_assets.data_version], order_by=[dbo.release_assets.path], transaction=trans) or []
    )


def get_release(name, trans, include_sc=True):
    # Get all of the base and asset information, potentially from a cache
    base_row = cache.get("releases", name, lambda: get_base_row(name, trans))
    base_data_version = cache.get("releases_data_version", name, lambda: get_base_data_version(name, trans))
    asset_rows = cache.get("release_assets", name, lambda: get_asset_rows(name, trans))
    asset_data_versions = cache.get("release_assets_data_versions", name, lambda: get_asset_data_versions(name, trans))

    data_versions = infinite_defaultdict()
    sc_data_versions = infinite_defaultdict()
    base_blob = {}
    sc_blob = {}
    if base_row:
        # base_data_version is cached for a shorter period of time than the overall row
        # because it's cheap to retrieve. if the cached row's data_version is older than
        # the cached data_version we will forcibly update it to make sure we minimize
        # the time we're serving old release data
        if base_row["data_version"] < base_data_version:
            base_row = get_base_row(name, trans)
        base_blob = base_row["data"]
        data_versions["."] = base_row["data_version"]

    # same thing here for the assets -- if any of the full asset data versions
    # do not match the cached asset data versions, we forcibly update
    if [r["data_version"] for r in asset_rows] != [r["data_version"] for r in asset_data_versions]:
        asset_rows = get_asset_rows(name, trans)

    for asset in asset_rows:
        path = asset["path"].split(".")[1:]
        ensure_path_exists(base_blob, path)
        set_by_path(base_blob, path, asset["data"])
        set_by_path(data_versions, path, asset["data_version"])
        if sc_blob:
            ensure_path_exists(sc_blob, path)
            set_by_path(sc_blob, path, asset["data"])

    if include_sc:
        scheduled_row = dbo.releases_json.scheduled_changes.select(where={"base_name": name, "complete": False}, transaction=trans)
        if sc_exists(name, trans) and (not scheduled_row or scheduled_row[0]["change_type"] != "delete"):
            sc_blob = deepcopy(base_blob)

        if scheduled_row:
            sc_data_versions["."] = scheduled_row[0]["data_version"]
            if scheduled_row[0]["change_type"] != "delete":
                # We have to merge rather than update because sc_blob
                # may contain assets and base data, and updating will fully
                # overwrite any root level keys from sc_blob with the new
                # data (rather than doing a deep update/merge).
                release_merger.merge(sc_blob, scheduled_row[0]["base_data"])

        for scheduled_asset in dbo.release_assets.scheduled_changes.select(where={"base_name": name, "complete": False}, transaction=trans):
            path = scheduled_asset["base_path"].split(".")[1:]
            set_by_path(sc_data_versions, path, scheduled_asset["data_version"])
            if scheduled_asset["change_type"] != "delete":
                ensure_path_exists(sc_blob, path)
                set_by_path(sc_blob, path, scheduled_asset["base_data"])

    if base_blob or sc_blob:
        return {"blob": base_blob, "data_versions": data_versions, "sc_blob": sc_blob, "sc_data_versions": sc_data_versions}
    else:
        return None


def get_product(name, trans):
    if not exists(name, trans):
        return None

    return dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.product], transaction=trans)[0]["product"]


def get_data_versions(name, trans):
    data_versions = infinite_defaultdict()
    base_row = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.data_version])
    if not base_row:
        return None

    data_versions["."] = base_row[0]["data_version"]
    for asset in dbo.release_assets.select(where={"name": name}, columns=[dbo.release_assets.path, dbo.release_assets.data_version], transaction=trans):
        path = asset["path"].split(".")[1:]
        set_by_path(data_versions, path, asset["data_version"])

    return {"data_versions": data_versions}


def get_data_version(name, path, trans):
    row = dbo.release_assets.select(where={"name": name, "path": path}, columns=[dbo.release_assets.data_version], transaction=trans)
    if not row:
        return None

    return {"data_version": row[0]["data_version"]}


def update_release(name, blob, old_data_versions, when, changed_by, trans):
    live_on_product_channels = dbo.releases_json.getPotentialRequiredSignoffs([{"name": name}], trans)
    new_data_versions = deepcopy(old_data_versions)

    if not when and any([v for v in live_on_product_channels.values()]):
        raise SignoffRequiredError("Signoff is required, cannot update Release directly")

    current_product = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.product], transaction=trans)[0]["product"]
    if not dbo.hasPermission(changed_by, "release", "modify", current_product, trans):
        raise PermissionDeniedError(f"{changed_by} is not allowed to modify {current_product} releases")

    if is_read_only(name, trans):
        raise ReadOnlyError("Cannot update a Release that is marked as read-only")

    current_base_blob = dbo.releases_json.select(where={"name": name}, transaction=trans)[0]["data"]
    base_blob, assets = split_release(blob, get_schema_version(name, trans))
    coros = []

    # new_base_blob is used to update the releases_json row, and ends up
    # with the current blob + requested changes
    # full_blob is used to validate the entire new blob after all
    # (base and asset) changes have been applied
    new_base_blob = infinite_defaultdict()
    new_base_blob.update(current_base_blob)
    full_blob = deepcopy(new_base_blob)
    if base_blob and current_base_blob != base_blob:
        release_merger.merge(new_base_blob, base_blob)
        release_merger.merge(full_blob, base_blob)
        if when:
            sc_id = dbo.releases_json.scheduled_changes.insert(
                name=name,
                product=current_product,
                data=new_base_blob,
                data_version=old_data_versions["."],
                when=when,
                change_type="update",
                changed_by=changed_by,
                transaction=trans,
            )
            signoffs = {}
            for signoff in dbo.releases_json.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
                signoffs[signoff["username"]] = signoff["role"]
            new_data_versions["."] = {"sc_id": sc_id, "change_type": "update", "data_version": 1, "signoffs": signoffs, "when": when}
        else:
            coro = dbo.releases_json.async_update(
                where={"name": name}, what={"data": new_base_blob}, old_data_version=old_data_versions["."], changed_by=changed_by, transaction=trans
            )
            coros.append(coro)
            new_data_versions["."] += 1

    current_assets = get_assets(name, trans)
    for path, item in assets:
        str_path = "." + ".".join(path)

        if current_assets.get(str_path):
            if item != current_assets[str_path]["data"]:
                old_data_version = get_by_path(old_data_versions, path)
                if not old_data_version:
                    raise ValueError(f"Missing data_version for {str_path}")
                new_assets = current_assets[str_path]["data"]
                release_merger.merge(new_assets, item)
                ensure_path_exists(full_blob, path)
                set_by_path(full_blob, path, new_assets)
                if when:
                    sc_id = dbo.release_assets.scheduled_changes.insert(
                        name=name,
                        path=str_path,
                        data=new_assets,
                        data_version=old_data_version,
                        when=when,
                        change_type="update",
                        changed_by=changed_by,
                        transaction=trans,
                    )
                    signoffs = {}
                    for signoff in dbo.release_assets.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
                        signoffs[signoff["username"]] = signoff["role"]
                    set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "update", "data_version": 1, "signoffs": signoffs, "when": when})
                else:
                    coro = dbo.release_assets.async_update(
                        where={"name": name, "path": str_path},
                        what={"data": new_assets},
                        old_data_version=old_data_version,
                        changed_by=changed_by,
                        transaction=trans,
                    )
                    coros.append(coro)
                    set_by_path(new_data_versions, path, old_data_version + 1)
        else:
            if when:
                sc_id = dbo.release_assets.scheduled_changes.insert(
                    name=name,
                    path=str_path,
                    data=item,
                    when=when,
                    change_type="insert",
                    changed_by=changed_by,
                    transaction=trans,
                )
                signoffs = {}
                for signoff in dbo.release_assets.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
                    signoffs[signoff["username"]] = signoff["role"]
                set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "insert", "data_version": 1, "signoffs": signoffs, "when": when})
            else:
                coro = dbo.release_assets.async_insert(name=name, path=str_path, data=item, changed_by=changed_by, transaction=trans)
                coros.append(coro)
                set_by_path(new_data_versions, path, 1)

    # Raises if there are errors
    createBlob(full_blob).validate(current_product, app.config["ALLOWLISTED_DOMAINS"])

    await_coroutines(coros)

    return new_data_versions


def set_release(name, blob, product, old_data_versions, when, changed_by, trans):
    live_on_product_channels = dbo.releases_json.getPotentialRequiredSignoffs([{"name": name}], trans)
    if not old_data_versions:
        old_data_versions = {}
    new_data_versions = infinite_defaultdict()

    current_release = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.data, dbo.releases_json.product], transaction=trans)
    current_base_blob = {}
    current_product = None
    if current_release:
        current_base_blob = current_release[0]["data"]
        current_product = current_release[0]["product"]
    if current_product:
        if not dbo.hasPermission(changed_by, "release", "modify", current_product, trans):
            raise PermissionDeniedError(f"{changed_by} is not allowed to modify {current_product} releases")
        if product and not dbo.hasPermission(changed_by, "release", "modify", product, trans):
            raise PermissionDeniedError(f"{changed_by} is not allowed to modify {product} releases")
    else:
        if not dbo.hasPermission(changed_by, "release", "create", product, trans):
            raise PermissionDeniedError(f"{changed_by} is not allowed to create {product} releases")

    if current_release and is_read_only(name, trans):
        raise ReadOnlyError("Cannot overwrite a Release that is marked as read-only")

    # Raises if there are errors
    createBlob(blob).validate(product or current_product, app.config["ALLOWLISTED_DOMAINS"])

    current_assets = get_assets(name, trans)
    base_blob, new_assets = split_release(blob, blob["schema_version"])

    # if current == new, we will just be cancelling a scheduled change
    if current_base_blob != base_blob and current_assets != new_assets and not when and any([v for v in live_on_product_channels.values()]):
        raise SignoffRequiredError("Signoff is required, cannot update Release directly")

    seen_assets = set()
    coros = []
    for path, item in new_assets:
        str_path = "." + ".".join(path)
        seen_assets.add(str_path)
        if item == current_assets.get(str_path, {}).get("data"):
            # If the desired state in the same as the current state, we should cancel any
            # pending scheduled changes, if they exist.
            sc = dbo.release_assets.scheduled_changes.select(
                where={"base_name": name, "base_path": str_path, "complete": False},
                columns=[dbo.release_assets.scheduled_changes.sc_id, dbo.release_assets.scheduled_changes.data_version],
                transaction=trans,
            )
            if sc:
                dbo.release_assets.scheduled_changes.delete(
                    where={"sc_id": sc[0]["sc_id"]}, old_data_version=sc[0]["data_version"], changed_by=changed_by, transaction=trans
                )
            continue

        old_data_version = get_by_path(old_data_versions, path)
        if old_data_version:
            if when:
                sc_id = dbo.release_assets.scheduled_changes.insert(
                    name=name,
                    path=str_path,
                    data=item,
                    data_version=old_data_version,
                    when=when,
                    change_type="update",
                    changed_by=changed_by,
                    transaction=trans,
                )
                signoffs = {}
                for signoff in dbo.release_assets.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
                    signoffs[signoff["username"]] = signoff["role"]
                set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "update", "data_version": 1, "signoffs": signoffs, "when": when})
            else:
                coro = dbo.release_assets.async_update(
                    where={"name": name, "path": str_path}, what={"data": item}, old_data_version=old_data_version, changed_by=changed_by, transaction=trans
                )
                coros.append(coro)
                set_by_path(new_data_versions, path, old_data_version + 1)
        else:
            if when:
                sc_id = dbo.release_assets.scheduled_changes.insert(
                    name=name, path=str_path, data=item, when=when, change_type="insert", changed_by=changed_by, transaction=trans
                )
                signoffs = {}
                for signoff in dbo.release_assets.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
                    signoffs[signoff["username"]] = signoff["role"]
                set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "insert", "data_version": 1, "signoffs": signoffs, "when": when})
            else:
                coro = dbo.release_assets.async_insert(name=name, path=str_path, data=item, changed_by=changed_by, transaction=trans)
                coros.append(coro)
                set_by_path(new_data_versions, path, 1)

    removed_assets = {a for a in current_assets} - seen_assets
    for str_path in removed_assets:
        path = str_path.split(".")[1:]
        if when:
            sc_id = dbo.release_assets.scheduled_changes.insert(
                name=name,
                path=str_path,
                data_version=get_by_path(old_data_versions, path),
                when=when,
                change_type="delete",
                changed_by=changed_by,
                transaction=trans,
            )
            signoffs = {}
            for signoff in dbo.release_assets.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
                signoffs[signoff["username"]] = signoff["role"]
            set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "delete", "data_version": 1, "signoffs": signoffs, "when": when})
        else:
            coro = dbo.release_assets.async_delete(
                where={"name": name, "path": str_path}, old_data_version=get_by_path(old_data_versions, path), changed_by=changed_by, transaction=trans
            )
            coros.append(coro)

    if current_base_blob == base_blob:
        sc = dbo.releases_json.scheduled_changes.select(
            where={"base_name": name, "complete": False},
            columns=[dbo.releases_json.scheduled_changes.sc_id, dbo.releases_json.scheduled_changes.data_version],
            transaction=trans,
        )
        if sc:
            dbo.releases_json.scheduled_changes.delete(
                where={"sc_id": sc[0]["sc_id"]}, old_data_version=sc[0]["data_version"], changed_by=changed_by, transaction=trans
            )
    else:
        if old_data_versions.get("."):
            what = {"data": base_blob, "product": product or current_product}
            if when:
                sc_id = dbo.releases_json.scheduled_changes.insert(
                    name=name, data_version=old_data_versions["."], when=when, change_type="update", changed_by=changed_by, transaction=trans, **what
                )
                signoffs = {}
                for signoff in dbo.releases_json.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
                    signoffs[signoff["username"]] = signoff["role"]
                new_data_versions["."] = {"sc_id": sc_id, "change_type": "update", "data_version": 1, "signoffs": signoffs, "when": when}
            else:
                coro = dbo.releases_json.async_update(
                    where={"name": name}, what=what, old_data_version=old_data_versions["."], changed_by=changed_by, transaction=trans
                )
                coros.append(coro)
                new_data_versions["."] = old_data_versions["."] + 1
        else:
            coro = dbo.releases_json.async_insert(name=name, product=product, data=base_blob, changed_by=changed_by, transaction=trans)
            coros.append(coro)
            new_data_versions["."] = 1

    await_coroutines(coros)

    return new_data_versions


def delete_release(name, changed_by, trans):
    coros = []

    # Delete scheduled changes first because the database layer doesn't allow
    # objects with scheduled changes to be deleted.
    if sc_exists(name, trans):
        # No permissions checks need to be done here because releases that are only
        # scheduled changes (aka scheduled inserts do not require permission to delete)
        # Releases that truly exist will have their permissions checked further down
        row = dbo.releases_json.scheduled_changes.select(
            where={"base_name": name, "complete": False},
            columns=[
                dbo.releases_json.scheduled_changes.sc_id,
                dbo.releases_json.scheduled_changes.base_product,
                dbo.releases_json.scheduled_changes.data_version,
            ],
        )
        if row:
            row = row[0]
            sc_id = row["sc_id"]
            old_data_version = row["data_version"]

            dbo.releases_json.scheduled_changes.delete(where={"sc_id": sc_id}, old_data_version=old_data_version, changed_by=changed_by, transaction=trans)

        for asset in dbo.release_assets.scheduled_changes.select(
            where={"base_name": name, "complete": False},
            columns=[dbo.release_assets.scheduled_changes.sc_id, dbo.release_assets.scheduled_changes.data_version],
            transaction=trans,
        ):
            dbo.release_assets.scheduled_changes.delete(
                where={"sc_id": asset["sc_id"]}, old_data_version=asset["data_version"], changed_by=changed_by, transaction=trans
            )

    if exists(name, trans):
        row = dbo.releases_json.select(where={"name": name}, columns={dbo.releases_json.product, dbo.releases_json.data_version})[0]
        product = row["product"]
        old_data_version = row["data_version"]

        stmt = select([dbo.rules.rule_id, dbo.rules.product, dbo.rules.channel]).where(
            ((dbo.releases_json.name == dbo.rules.mapping) | (dbo.releases_json.name == dbo.rules.fallbackMapping)) & (dbo.releases_json.name == name)
        )
        if trans.execute(stmt).fetchall():
            raise ValueError("Cannot delete release that is mapped to")
        if dbo.pinnable_releases.mappingHasPin(name, transaction=trans):
            raise ValueError("Cannot delete release that is pinnable")

        if not dbo.hasPermission(changed_by, "release", "delete", product, trans):
            raise PermissionDeniedError(f"{changed_by} is not allowed to delete {product} releases")

        if is_read_only(name, trans):
            raise ReadOnlyError("Cannot delete a Release that is marked as read-only")

        coro = dbo.releases_json.async_delete(where={"name": name}, old_data_version=old_data_version, changed_by=changed_by, transaction=trans)
        coros.append(coro)

        for asset in dbo.release_assets.select(where={"name": name}, columns=[dbo.release_assets.path, dbo.release_assets.data_version], transaction=trans):
            coro = dbo.release_assets.async_delete(
                where={"name": name, "path": asset["path"]}, old_data_version=asset["data_version"], changed_by=changed_by, transaction=trans
            )
            coros.append(coro)

    await_coroutines(coros)


def set_read_only(name, read_only, old_data_version, changed_by, trans):
    product = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.product], transaction=trans)[0]["product"]

    # If the Release is being changed to read-write, it may require signoff
    use_sc = False
    if read_only is False:
        live_on_product_channels = []
        stmt = select([dbo.rules.rule_id, dbo.rules.product, dbo.rules.channel]).where(
            ((dbo.releases_json.name == dbo.rules.mapping) | (dbo.releases_json.name == dbo.rules.fallbackMapping)) & (dbo.releases_json.name == name)
        )
        for row in trans.execute(stmt).fetchall():
            live_on_product_channels.append(dict(row))

        if live_on_product_channels:
            log.debug(f"{name} is live on {live_on_product_channels}")
            prs = dbo.rules.getPotentialRequiredSignoffs(live_on_product_channels, transaction=trans)
            # If the Release is mapped to by a Rule that requires signoff, we cannot proceed
            if any([v for v in prs.values()]):
                use_sc = True

        # If it wasn't mapped to by a Rule that requires signoff, check for _any_ required signoffs
        # for its product. This is a bit aggressive, but it protects against Releases for important
        # products (eg: Firefox) from being modified before they go live on a protected channel.
        if dbo.productRequiredSignoffs.select(where={"product": product}, transaction=trans):
            use_sc = True

    permission = "unset" if read_only else "set"
    if not dbo.hasPermission(changed_by, "release_read_only", permission, product, trans):
        raise PermissionDeniedError(f"{changed_by} is not allow to {permission} read_only for {product} releeases")

    if use_sc:
        data = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.data], transaction=trans)[0]["data"]
        # 30 seconds in the future
        when = getMillisecondTimestamp() + 30000
        sc_id = dbo.releases_json.scheduled_changes.insert(
            name=name,
            product=product,
            data=data,
            read_only=read_only,
            data_version=old_data_version,
            when=when,
            change_type="update",
            changed_by=changed_by,
            transaction=trans,
        )
        signoffs = {}
        for signoff in dbo.releases_json.scheduled_changes.signoffs.select(where={"sc_id": sc_id}, transaction=trans):
            signoffs[signoff["username"]] = signoff["role"]
        return {".": {"sc_id": sc_id, "change_type": "update", "data_version": 1, "signoffs": signoffs, "when": when}}
    else:
        coro = dbo.releases_json.async_update(
            where={"name": name}, what={"read_only": read_only}, old_data_version=old_data_version, changed_by=changed_by, transaction=trans
        )
        await_coroutines([coro])
        return {".": old_data_version + 1}


def signoff(name, role, username, trans):
    base_sc = dbo.releases_json.scheduled_changes.select(
        where={"base_name": name, "complete": False}, columns=[dbo.releases_json.scheduled_changes.sc_id], transaction=trans
    )
    if base_sc:
        dbo.releases_json.scheduled_changes.signoffs.insert(username, sc_id=base_sc[0]["sc_id"], role=role, transaction=trans)

    for sc in dbo.release_assets.scheduled_changes.select(
        where={"base_name": name, "complete": False}, columns=[dbo.release_assets.scheduled_changes.sc_id], transaction=trans
    ):
        dbo.release_assets.scheduled_changes.signoffs.insert(username, sc_id=sc["sc_id"], role=role, transaction=trans)


def revoke_signoff(name, username, trans):
    base_sc = dbo.releases_json.scheduled_changes.select(
        where={"base_name": name, "complete": False}, columns=[dbo.releases_json.scheduled_changes.sc_id], transaction=trans
    )
    if base_sc:
        dbo.releases_json.scheduled_changes.signoffs.delete({"sc_id": base_sc[0]["sc_id"], "username": username}, changed_by=username, transaction=trans)

    for sc in dbo.release_assets.scheduled_changes.select(
        where={"base_name": name, "complete": False}, columns=[dbo.release_assets.scheduled_changes.sc_id], transaction=trans
    ):
        dbo.release_assets.scheduled_changes.signoffs.delete({"sc_id": sc["sc_id"], "username": username}, changed_by=username, transaction=trans)


def enact_scheduled_changes(name, username, trans):
    coros = []
    base_sc = dbo.releases_json.scheduled_changes.select(
        where={"base_name": name, "complete": False}, columns=[dbo.releases_json.scheduled_changes.sc_id], transaction=trans
    )
    if base_sc:
        coro = dbo.releases_json.scheduled_changes.asyncEnactChange(base_sc[0]["sc_id"], username, trans)
        coros.append(coro)

    for sc in dbo.release_assets.scheduled_changes.select(
        where={"base_name": name, "complete": False}, columns=[dbo.release_assets.scheduled_changes.sc_id], transaction=trans
    ):
        coro = dbo.release_assets.scheduled_changes.asyncEnactChange(sc["sc_id"], username, trans)
        coros.append(coro)

    await_coroutines(coros)


def set_pinnable(name, product, channel, version, when, username, trans):
    if not exists(name, trans):
        raise ValueError(f"'{name}' is not an existing mapping.")
    old_row = dbo.pinnable_releases.getPinRow(product=product, channel=channel, version=version, transaction=trans)

    def get_version(mapping, trans):
        release = releases.get_release(mapping, trans=trans, include_sc=False)
        blob = None
        if release:
            blob = createBlob(release["blob"])
        if not blob:
            return None
        version = blob.getApplicationVersion(None, None)
        if not version:
            return None
        return MozillaVersion(version)

    if old_row is not None:
        current_pin_version = get_version(old_row["mapping"], trans=trans)
        submitted_version = get_version(name, trans=trans)
        if current_pin_version and submitted_version and current_pin_version > submitted_version:
            # Just in case we build, for example, '102.1.0' and later build '102.0.3', we
            # don't want to update the '102.' pin to '102.0.3'.
            return {"pin_not_set": True, "reason": "existing_pin_is_newer"}

    if not when:
        if old_row is None:
            row = dbo.pinnable_releases.insert(changed_by=username, product=product, channel=channel, version=version, mapping=name, transaction=trans)
        else:
            row = dbo.pinnable_releases.update(
                where=[dbo.pinnable_releases.product == product, dbo.pinnable_releases.channel == channel, dbo.pinnable_releases.version == version],
                what={"mapping": name},
                changed_by=username,
                old_data_version=old_row["data_version"],
                transaction=trans,
            )
        return {".": row["data_version"]}

    if old_row is None:
        sc_id = dbo.pinnable_releases.scheduled_changes.insert(
            mapping=name,
            product=product,
            channel=channel,
            version=version,
            when=when,
            change_type="insert",
            changed_by=username,
            transaction=trans,
        )
        return {".": {"sc_id": sc_id, "change_type": "insert", "data_version": 1, "signoffs": {}, "when": when}}
    else:
        sc_id = dbo.pinnable_releases.scheduled_changes.insert(
            mapping=name,
            product=product,
            channel=channel,
            version=version,
            when=when,
            change_type="update",
            changed_by=username,
            transaction=trans,
            data_version=old_row["data_version"],
        )
        return {".": {"sc_id": sc_id, "change_type": "update", "data_version": old_row["data_version"] + 1, "signoffs": {}, "when": when}}
