from sqlalchemy import Table, Column, Integer, String, MetaData, \
    BigInteger

metadata = MetaData()

# TODO: double check this against the db.py class before merging!
rules_scheduled_changes = Table(
    "rules_scheduled_changes", metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=True),
    Column("scheduled_by", String(100), nullable=False),
    Column("telemetry_product", String(15)),
    Column("telemetry_channel", String(75)),
    Column("telemetry_uptake", Integer),
    Column("data_version", Integer),
    Column("rule_id", Integer, autoincrement=True),
    Column("priority", Integer),
    Column("mapping", String(100)),
    Column("backgroundRate", Integer),
    Column("update_type", String(15), nullable=False),
    Column("product", String(15)),
    Column("version", String(10)),
    Column("channel", String(75)),
    Column("buildTarget", String(75)),
    Column("buildID", String(20)),
    Column("locale", String(200)),
    Column("osVersion", String(1000)),
    Column("distribution", String(100)),
    Column("distVersion", String(100)),
    Column("headerArchitecture", String(10)),
    Column("comment", String(500)),
    Column("whitelist", String(100)),
    Column("alias", String(50)),
    Column("table_data_version", Integer)
)


rules_scheduled_changes_history = Table(
    "rules_scheduled_changes_history", metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False, autoincrement=True),
    Column("scheduled_by", String(100)),
    Column("telemetry_product", String(15)),
    Column("telemetry_channel", String(75)),
    Column("telemetry_uptake", Integer),
    Column("data_version", Integer),
    Column("rule_id", Integer, autoincrement=True),
    Column("priority", Integer),
    Column("mapping", String(100)),
    Column("backgroundRate", Integer),
    Column("update_type", String(15)),
    Column("product", String(15)),
    Column("version", String(10)),
    Column("channel", String(75)),
    Column("buildTarget", String(75)),
    Column("buildID", String(20)),
    Column("locale", String(200)),
    Column("osVersion", String(1000)),
    Column("distribution", String(100)),
    Column("distVersion", String(100)),
    Column("headerArchitecture", String(10)),
    Column("comment", String(500)),
    Column("whitelist", String(100)),
    Column("alias", String(50)),
    Column("table_data_version", Integer)
)


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer
    rules_scheduled_changes.append_column(Column("when", bigintType))
    rules_scheduled_changes_history.append_column(Column("when", bigintType))
    rules_scheduled_changes_history.append_column(Column("timestamp", bigintType, nullable=False))
    metadata.create_all()
