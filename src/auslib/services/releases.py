import asyncio
import logging
from copy import deepcopy
from itertools import chain

from aiohttp import ClientError
from deepmerge import Merger
from flask import current_app as app
from sentry_sdk import capture_exception
from sqlalchemy import join, select

from ..blobs.base import createBlob
from ..errors import PermissionDeniedError, ReadOnlyError, SignoffRequiredError
from ..global_state import dbo
from ..util.data_structures import ensure_path_exists, get_by_path, infinite_defaultdict, set_by_path

log = logging.getLogger(__file__)

store = object()

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
    column.anon_label = "schema_version"
    return dbo.releases_json.select(where={"name": name}, columns=[column], transaction=trans)[0]["schema_version"]


def exists(name, trans):
    if dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.name], transaction=trans):
        return True

    return False


def is_read_only(name, trans):
    return dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.read_only], transaction=trans)[0].get("read_only")


def get_assets(name, trans):
    assets = {}
    for asset in dbo.release_assets.select(where={"name": name}, transaction=trans):
        assets[asset["path"]] = asset

    return assets


def get_releases(trans):
    releases = dbo.releases_json.select(
        columns=[dbo.releases_json.name, dbo.releases_json.product, dbo.releases_json.data_version, dbo.releases_json.read_only], transaction=trans
    )
    j = join(dbo.releases_json.t, dbo.rules.t, ((dbo.releases_json.name == dbo.rules.mapping) | (dbo.releases_json.name == dbo.rules.fallbackMapping)))
    rule_mappings = trans.execute(select([dbo.releases_json.name, dbo.rules.rule_id, dbo.rules.product, dbo.rules.channel]).select_from(j)).fetchall()
    for row in releases:
        refs = [ref for ref in rule_mappings if ref[0] == row["name"]]
        row["rule_info"] = {str(ref[1]): {"product": ref[2], "channel": ref[3]} for ref in refs}
        row["scheduled_changes"] = []

    for sc in chain(dbo.releases_json.scheduled_changes.select(), dbo.release_assets.scheduled_changes.select()):
        release = [r for r in releases if r["name"] == sc["base_name"]]
        if release:
            release = release[0]
            if "scheduled_changes" not in release:
                release["scheduled_changes"] = []
        else:
            release = {
                "name": sc["base_name"],
                "product": None,
                "data_version": None,
                "read_only": None,
                "rule_info": {},
                "scheduled_changes": [],
            }

        munged_sc = {}
        for k in sc:
            if k == "base_data":
                continue
            elif k == "data_version":
                munged_sc["sc_data_version"] = sc[k]
            else:
                munged_sc[k.replace("base_", "")] = sc[k]

        release["scheduled_changes"].append(munged_sc)

        if release not in releases:
            releases.append(release)

    return {"releases": sorted(releases, key=lambda r: r["name"])}


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
    futures = []

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
            new_data_versions["."] = {"sc_id": sc_id, "change_type": "update", "data_version": 1}
        else:
            future = dbo.releases_json.async_update(
                where={"name": name}, what={"data": new_base_blob}, old_data_version=old_data_versions["."], changed_by=changed_by, transaction=trans
            )
            futures.append(future)
            new_data_versions["."] += 1

    for path, item in assets:
        str_path = "." + ".".join(path)
        current_assets = dbo.release_assets.select(where={"name": name, "path": str_path}, transaction=trans)
        if current_assets:
            old_data_version = get_by_path(old_data_versions, path)
            new_assets = current_assets[0]["data"]
            if item != new_assets:
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
                    set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "update", "data_version": 1})
                else:
                    future = dbo.release_assets.async_update(
                        where={"name": name, "path": str_path},
                        what={"data": new_assets},
                        old_data_version=old_data_version,
                        changed_by=changed_by,
                        transaction=trans,
                    )
                    futures.append(future)
                    set_by_path(new_data_versions, path, old_data_version + 1)
        else:
            if when:
                sc_id = dbo.release_assets.scheduled_changes.insert(
                    name=name, path=str_path, data=item, when=when, change_type="insert", changed_by=changed_by, transaction=trans,
                )
                set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "insert", "data_version": 1})
            else:
                future = dbo.release_assets.async_insert(name=name, path=str_path, data=item, changed_by=changed_by, transaction=trans)
                futures.append(future)
                set_by_path(new_data_versions, path, 1)

    # Raises if there are errors
    createBlob(full_blob).validate(current_product, app.config["WHITELISTED_DOMAINS"])

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(asyncio.gather(*futures, return_exceptions=True))
        for r in results:
            if isinstance(r, Exception):
                # aiohttp exceptions indicate a failure uploading to GCS, which don't warrant
                # sending an error back to the client.
                if isinstance(r, ClientError):
                    capture_exception(r)
                else:
                    raise r
    finally:
        loop.close()

    return new_data_versions


def set_release(name, blob, product, old_data_versions, when, changed_by, trans):
    live_on_product_channels = dbo.releases_json.getPotentialRequiredSignoffs([{"name": name}], trans)
    if not old_data_versions:
        old_data_versions = {}
    new_data_versions = infinite_defaultdict()

    if not when and any([v for v in live_on_product_channels.values()]):
        raise SignoffRequiredError("Signoff is required, cannot update Release directly")

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
    createBlob(blob).validate(product or current_product, app.config["WHITELISTED_DOMAINS"])

    current_assets = get_assets(name, trans)
    base_blob, new_assets = split_release(blob, blob["schema_version"])
    seen_assets = set()
    futures = []
    for path, item in new_assets:
        str_path = "." + ".".join(path)
        seen_assets.add(str_path)
        if item == current_assets.get(str_path, {}).get("data"):
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
                set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "update", "data_version": 1})
            else:
                future = dbo.release_assets.async_update(
                    where={"name": name, "path": str_path}, what={"data": item}, old_data_version=old_data_version, changed_by=changed_by, transaction=trans
                )
                futures.append(future)
                set_by_path(new_data_versions, path, old_data_version + 1)
        else:
            if when:
                sc_id = dbo.release_assets.scheduled_changes.insert(
                    name=name, path=str_path, data=item, when=when, change_type="insert", changed_by=changed_by, transaction=trans
                )
                set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "insert", "data_version": 1})
            else:
                future = dbo.release_assets.async_insert(name=name, path=str_path, data=item, changed_by=changed_by, transaction=trans)
                futures.append(future)
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
            set_by_path(new_data_versions, path, {"sc_id": sc_id, "change_type": "delete", "data_version": 1})
        else:
            future = dbo.release_assets.async_delete(
                where={"name": name, "path": str_path}, old_data_version=get_by_path(old_data_versions, path), changed_by=changed_by, transaction=trans
            )
            futures.append(future)

    if current_base_blob != base_blob:
        if old_data_versions.get("."):
            what = {"data": base_blob}
            if product:
                what["product"] = product
            if when:
                sc_id = dbo.releases_json.scheduled_changes.insert(
                    name=name, data_version=old_data_versions["."], when=when, change_type="update", changed_by=changed_by, transaction=trans, **what
                )
                new_data_versions["."] = {"sc_id": sc_id, "change_type": "update", "data_version": 1}
            else:
                future = dbo.releases_json.async_update(
                    where={"name": name}, what=what, old_data_version=old_data_versions["."], changed_by=changed_by, transaction=trans
                )
                futures.append(future)
                new_data_versions["."] = old_data_versions["."] + 1
        else:
            future = dbo.releases_json.async_insert(name=name, product=product, data=base_blob, changed_by=changed_by, transaction=trans)
            futures.append(future)
            new_data_versions["."] = 1

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(asyncio.gather(*futures, return_exceptions=True))

        for r in results:
            if isinstance(r, Exception):
                # aiohttp exceptions indicate a failure uploading to GCS, which don't warrant
                # sending an error back to the client.
                if isinstance(r, ClientError):
                    capture_exception(r)
                else:
                    raise r

    finally:
        loop.close()
    return new_data_versions
