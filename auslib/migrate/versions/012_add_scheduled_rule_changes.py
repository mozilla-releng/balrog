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
    Column("sc_rule_id", Integer, autoincrement=True),
    Column("sc_priority", Integer),
    Column("sc_mapping", String(100)),
    Column("sc_backgroundRate", Integer),
    Column("sc_update_type", String(15), nullable=False),
    Column("sc_product", String(15)),
    Column("sc_version", String(10)),
    Column("sc_channel", String(75)),
    Column("sc_buildTarget", String(75)),
    Column("sc_buildID", String(20)),
    Column("sc_locale", String(200)),
    Column("sc_osVersion", String(1000)),
    Column("sc_distribution", String(100)),
    Column("sc_distVersion", String(100)),
    Column("sc_headerArchitecture", String(10)),
    Column("sc_comment", String(500)),
    Column("sc_whitelist", String(100)),
    Column("sc_alias", String(50)),
    Column("sc_data_version", Integer)
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
    Column("sc_rule_id", Integer, autoincrement=True),
    Column("sc_priority", Integer),
    Column("sc_mapping", String(100)),
    Column("sc_backgroundRate", Integer),
    Column("sc_update_type", String(15)),
    Column("sc_product", String(15)),
    Column("sc_version", String(10)),
    Column("sc_channel", String(75)),
    Column("sc_buildTarget", String(75)),
    Column("sc_buildID", String(20)),
    Column("sc_locale", String(200)),
    Column("sc_osVersion", String(1000)),
    Column("sc_distribution", String(100)),
    Column("sc_distVersion", String(100)),
    Column("sc_headerArchitecture", String(10)),
    Column("sc_comment", String(500)),
    Column("sc_whitelist", String(100)),
    Column("sc_alias", String(50)),
    Column("sc_data_version", Integer)
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
