from sqlalchemy import MetaData, Table

data_version_nullable_tbls = [
    "permissions_req_signoffs_scheduled_changes_conditions",
    "permissions_scheduled_changes",
    "permissions_scheduled_changes_conditions",
    "product_req_signoffs_scheduled_changes_conditions",
    "releases_scheduled_changes",
    "releases_scheduled_changes_conditions",
    "rules_scheduled_changes",
    "rules_scheduled_changes_conditions",
    "user_roles",
]

when_nullable_tbls = ["permissions_scheduled_changes_conditions", "releases_scheduled_changes_conditions"]


def _change_nullable_attr(table_name, column, metadata, nullable):
    tbl = Table(table_name, metadata, autoload=True)

    tbl.c[column].alter(nullable=nullable)


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    for tbl in data_version_nullable_tbls:
        _change_nullable_attr(tbl, "data_version", metadata, False)

    for tbl in when_nullable_tbls:
        _change_nullable_attr(tbl, "when", metadata, True)


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    for tbl in data_version_nullable_tbls:
        _change_nullable_attr(tbl, "data_version", metadata, True)

    for tbl in when_nullable_tbls:
        _change_nullable_attr(tbl, "when", metadata, False)
