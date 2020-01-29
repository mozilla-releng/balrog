import logging
import operator
from copy import deepcopy
from functools import reduce

from deepmerge import Merger
from sqlalchemy import select

from ..db import SignoffRequiredError
from ..global_state import dbo

log = logging.getLogger(__file__)

store = object()

# fmt: off
APP_RELEASE_DETAILS = {
    "platforms": {
        "*": {
            "locales": {
                "*": store
            }
        }
    }
}
RELEASE_BLOB_DETAILS = {
    1: APP_RELEASE_DETAILS,
    2: APP_RELEASE_DETAILS,
    3: APP_RELEASE_DETAILS,
    4: APP_RELEASE_DETAILS,
    5: APP_RELEASE_DETAILS,
    6: APP_RELEASE_DETAILS,
    7: APP_RELEASE_DETAILS,
    8: APP_RELEASE_DETAILS,
    9: APP_RELEASE_DETAILS,
}
# fmt: on


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


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


def do_split_release(blob, details_keys):
    """Split a full Release into two separate dictionaries containing the base in one,
    and the details in the other.

        :param blob: The full Release to split
        :type blob: dict

        :param details_keys: The keys that should end up in the `details`.
        :type details_keys: dict
    """
    base = {}
    details = {}

    for k, v in blob.items():
        # If none of this key's value belongs in details, put everything in the base and move on
        if not details_keys or (k not in details_keys and "*" not in details_keys):
            base[k] = v
            continue

        details_value = details_keys.get(k) or details_keys["*"]
        # If this key's entire value belongs in details, put everything in details and move on
        if details_value == store:
            details[k] = v
            continue

        # Otherwise, split the value and store both results
        base_data, details_data = do_split_release(v, details_value)
        if base_data:
            base[k] = base_data
        if details_data:
            details[k] = details_data

    return base, details


def separate_details(details, details_keys, path=()):
    """Split the details of a Release into individual parts"""
    if details_keys == store:
        yield (path, details)
        # Short circuit, because we don't need to iterate over something
        # we're going to store in its own row.
        return

    for k, v in details.items():
        if k in details_keys or "*" in details_keys:
            newpath = (*path, k)
            yield from separate_details(v, details_keys.get(k) or details_keys["*"], newpath)


def split_release(blob, schema_version):
    """Split an entire Release into its base object and list of details objects"""
    detail_parts = []
    details_keys = RELEASE_BLOB_DETAILS.get(schema_version, {})

    base, details = do_split_release(blob, details_keys)
    if details:
        detail_parts = [p for p in separate_details(details, details_keys)]

    return base, detail_parts


def get_schema_version(name, trans):
    # TODO: Can we make "anon_1" into something useful?
    return dbo.releases_json.select(where={"name": name}, columns=[dbo.releases_json.data["schema_version"]], transaction=trans)[0]["anon_1"]


def get_existing_locales(name, trans):
    existing_locales = dbo.release_details.select(where={"name": name}, columns=[dbo.release_details.path], transaction=trans)
    return set([l["path"] for l in existing_locales])


def update_release(name, blob, old_data_versions, trans):
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

    base_blob, details = split_release(blob, get_schema_version(name, trans))
    for path, item in details:
        old_data_version = get_by_path(old_data_versions, path)
        set_by_path(new_data_versions, path, old_data_version + 1)
        path = "." + ".".join(path)
        new_details = dbo.release_details.select(where={"name": name, "path": path}, transaction=trans)[0]["data"]
        release_merger.merge(new_details, item)
        dbo.release_details.update(where={"name": name, "path": path}, what={"data": new_details}, old_data_version=old_data_version, transaction=trans)

    new_blob = dbo.releases_json.select(where={"name": name}, transaction=trans)[0]["data"]
    release_merger.merge(new_blob, base_blob)
    dbo.releases_json.update(where={"name": name}, what={"data": new_blob}, old_data_version=old_data_versions["."], transaction=trans)
    new_data_versions["."] += 1

    return new_data_versions


def overwrite_release(name, blob, old_data_versions, trans):
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

    base_blob, details = split_release(blob, get_schema_version(name, trans))
    seen_locales = set()
    for path, item in details:
        old_data_version = get_by_path(old_data_versions, path)
        set_by_path(new_data_versions, path, old_data_version + 1)
        path = "." + ".".join(path)
        seen_locales.add(path)
        dbo.release_details.update(where={"name": name, "path": path}, what={"data": item}, old_data_version=old_data_version, transaction=trans)

    existing_locales = get_existing_locales(name, trans)
    removed_locales = existing_locales - seen_locales
    if removed_locales:
        query = dbo.release_details.t.delete().where(dbo.release_details.name == name).where(dbo.release_details.path.in_(removed_locales))
        trans.execute(query)

    dbo.releases_json.update(where={"name": name}, what={"data": base_blob}, old_data_version=old_data_versions["."], transaction=trans)
    new_data_versions["."] += 1

    return new_data_versions
