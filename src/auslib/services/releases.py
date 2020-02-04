import logging
from copy import deepcopy

from deepmerge import Merger
from flask import current_app as app
from sqlalchemy import select

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


def do_split_release(blob, assets_keys):
    """Split a full Release into two separate dictionaries containing the base in one,
    and the assets in the other.

        :param blob: The full Release to split
        :type blob: dict

        :param assets_keys: The keys that should end up in the `assets`.
        :type assets_keys: dict
    """
    base = {}
    assets = {}

    for k, v in blob.items():
        # If none of this key's value belongs in assets, put everything in the base and move on
        if not assets_keys or (k not in assets_keys and "*" not in assets_keys):
            base[k] = v
            continue

        assets_value = assets_keys.get(k) or assets_keys["*"]
        # If this key's entire value belongs in assets, put everything in assets and move on
        if assets_value == store:
            assets[k] = v
            continue

        # Otherwise, split the value and store both results
        base_data, assets_data = do_split_release(v, assets_value)
        if base_data:
            base[k] = base_data
        if assets_data:
            assets[k] = assets_data

    return base, assets


def separate_assets(assets, assets_keys, path=()):
    """Split the assets of a Release into individual parts"""
    if assets_keys == store:
        yield (path, assets)
        # Short circuit, because we don't need to iterate over something
        # we're going to store in its own row.
        return

    for k, v in assets.items():
        if k in assets_keys or "*" in assets_keys:
            newpath = (*path, k)
            yield from separate_assets(v, assets_keys.get(k) or assets_keys["*"], newpath)


def split_release(blob, schema_version):
    """Split an entire Release into its base object and list of assets objects"""
    detail_parts = []
    assets_keys = RELEASE_BLOB_ASSETS.get(schema_version, {})

    base, assets = do_split_release(blob, assets_keys)
    if assets:
        detail_parts = [p for p in separate_assets(assets, assets_keys)]

    return base, detail_parts


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


def update_release(name, blob, old_data_versions, changed_by, trans):
    live_on_product_channels = []
    new_data_versions = deepcopy(old_data_versions)

    stmt = select([dbo.rules.rule_id, dbo.rules.product, dbo.rules.channel]).where(
        ((dbo.releases_json.name == dbo.rules.mapping) | (dbo.releases_json.name == dbo.rules.fallbackMapping)) & (dbo.releases_json.name == name)
    )
    for row in trans.execute(stmt).fetchall():
        live_on_product_channels.append(dict(row))

    if live_on_product_channels:
        log.debug(f"{name} is live on {live_on_product_channels}")
        prs = dbo.rules.getPotentialRequiredSignoffs(live_on_product_channels, transaction=trans)
        if any([v for v in prs.values()]):
            raise SignoffRequiredError("Signoff is required, cannot update Release directly")

    current_product = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.product], transaction=trans)[0]["product"]
    if not dbo.hasPermission(changed_by, "release", "modify", current_product, trans):
        raise PermissionDeniedError(f"{changed_by} is not allowed to modify {current_product} releases")

    if is_read_only(name, trans):
        raise ReadOnlyError("Cannot update a Release that is marked as read-only")

    base_blob, assets = split_release(blob, get_schema_version(name, trans))

    # new_blob is first used to update the releases_json table
    # later, it has all asset information added to it so we can
    # do a full blob validation before committing the transaction
    new_blob = infinite_defaultdict()
    new_blob.update(dbo.releases_json.select(where={"name": name}, transaction=trans)[0]["data"])
    if base_blob:
        release_merger.merge(new_blob, base_blob)
        dbo.releases_json.update(
            where={"name": name}, what={"data": new_blob}, old_data_version=old_data_versions["."], changed_by=changed_by, transaction=trans
        )
        new_data_versions["."] += 1

    for path, item in assets:
        str_path = "." + ".".join(path)
        current_assets = dbo.release_assets.select(where={"name": name, "path": str_path}, transaction=trans)
        if current_assets:
            new_assets = current_assets[0]["data"]
            release_merger.merge(new_assets, item)
            old_data_version = get_by_path(old_data_versions, path)
            set_by_path(new_data_versions, path, old_data_version + 1)
            ensure_path_exists(new_blob, path)
            set_by_path(new_blob, path, new_assets)
            dbo.release_assets.update(
                where={"name": name, "path": str_path}, what={"data": new_assets}, old_data_version=old_data_version, changed_by=changed_by, transaction=trans
            )
        else:
            set_by_path(new_data_versions, path, 1)
            dbo.release_assets.insert(name=name, path=str_path, data=item, changed_by=changed_by, transaction=trans)

    # Raises if there are errors
    createBlob(new_blob).validate(current_product, app.config["WHITELISTED_DOMAINS"])

    return new_data_versions


def overwrite_release(name, blob, product, old_data_versions, changed_by, trans):
    live_on_product_channels = []
    if not old_data_versions:
        old_data_versions = {}
    new_data_versions = infinite_defaultdict()

    stmt = select([dbo.rules.rule_id, dbo.rules.product, dbo.rules.channel]).where(
        ((dbo.releases_json.name == dbo.rules.mapping) | (dbo.releases_json.name == dbo.rules.fallbackMapping)) & (dbo.releases_json.name == name)
    )
    for row in trans.execute(stmt).fetchall():
        live_on_product_channels.append(dict(row))

    if live_on_product_channels:
        log.debug(f"{name} is live on {live_on_product_channels}")
        prs = dbo.rules.getPotentialRequiredSignoffs(live_on_product_channels, transaction=trans)
        if any([v for v in prs.values()]):
            raise SignoffRequiredError("Signoff is required, cannot update Release directly")

    current_release = dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.product], transaction=trans)
    current_product = None
    if current_release:
        current_product = current_release[0]["product"]
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
    for path, item in new_assets:
        str_path = "." + ".".join(path)
        seen_assets.add(str_path)
        if item == current_assets.get(str_path, {}).get("data"):
            continue

        old_data_version = get_by_path(old_data_versions, path)
        if old_data_version:
            set_by_path(new_data_versions, path, old_data_version + 1)
            dbo.release_assets.update(
                where={"name": name, "path": str_path}, what={"data": item}, old_data_version=old_data_version, changed_by=changed_by, transaction=trans
            )
        else:
            set_by_path(new_data_versions, path, 1)
            dbo.release_assets.insert(name=name, path=str_path, data=item, changed_by=changed_by, transaction=trans)

    removed_assets = {a for a in current_assets} - seen_assets
    for path in removed_assets:
        abc = path.split(".")[1:]
        dbo.release_assets.delete(
            where={"name": name, "path": path}, old_data_version=get_by_path(old_data_versions, abc), changed_by=changed_by, transaction=trans
        )

    if old_data_versions.get("."):
        what = {"data": base_blob}
        if product:
            what["product"] = product
        dbo.releases_json.update(where={"name": name}, what=what, old_data_version=old_data_versions["."], changed_by=changed_by, transaction=trans)
        new_data_versions["."] = old_data_versions["."] + 1
    else:
        dbo.releases_json.insert(name=name, product=product, data=base_blob, changed_by=changed_by, transaction=trans)
        new_data_versions["."] = 1

    return new_data_versions
