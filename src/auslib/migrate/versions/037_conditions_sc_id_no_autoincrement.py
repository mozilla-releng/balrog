"""Remove AUTO_INCREMENT from sc_id on all conditions tables.

sc_id on conditions tables is a foreign key to the corresponding
scheduled_changes table and is always set explicitly on insert.
It was never intended to be AUTO_INCREMENT.
"""

CONDITIONS_TABLES = [
    "emergency_shutoffs_scheduled_changes_conditions",
    "permissions_req_signoffs_scheduled_changes_conditions",
    "permissions_scheduled_changes_conditions",
    "pinnable_releases_scheduled_changes_conditions",
    "product_req_signoffs_scheduled_changes_conditions",
    "release_assets_scheduled_changes_conditions",
    "releases_json_scheduled_changes_conditions",
    "releases_scheduled_changes_conditions",
    "rules_scheduled_changes_conditions",
]


def upgrade(migrate_engine):
    if migrate_engine.name == "mysql":
        for table in CONDITIONS_TABLES:
            migrate_engine.execute("ALTER TABLE %s MODIFY sc_id INTEGER NOT NULL" % table)


def downgrade(migrate_engine):
    if migrate_engine.name == "mysql":
        for table in CONDITIONS_TABLES:
            migrate_engine.execute("ALTER TABLE %s MODIFY sc_id INTEGER NOT NULL AUTO_INCREMENT" % table)
