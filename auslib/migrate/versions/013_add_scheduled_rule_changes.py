from sqlalchemy import (BigInteger, Boolean, Column, Integer, MetaData, String,
                        Table)

metadata = MetaData()

rules_scheduled_changes = Table(
    "rules_scheduled_changes", metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=True),
    Column("scheduled_by", String(100), nullable=False),
    Column("complete", Boolean, default=False),
    Column("telemetry_product", String(15)),
    Column("telemetry_channel", String(75)),
    Column("telemetry_uptake", Integer),
    Column("data_version", Integer),
    Column("base_rule_id", Integer, autoincrement=True),
    Column("base_priority", Integer),
    Column("base_mapping", String(100)),
    Column("base_backgroundRate", Integer),
    Column("base_update_type", String(15), nullable=False),
    Column("base_product", String(15)),
    Column("base_version", String(10)),
    Column("base_channel", String(75)),
    Column("base_buildTarget", String(75)),
    Column("base_buildID", String(20)),
    Column("base_locale", String(200)),
    Column("base_osVersion", String(1000)),
    Column("base_systemCapabilities", String(1000)),
    Column("base_distribution", String(100)),
    Column("base_distVersion", String(100)),
    Column("base_headerArchitecture", String(10)),
    Column("base_comment", String(500)),
    Column("base_whitelist", String(100)),
    Column("base_alias", String(50)),
    Column("base_data_version", Integer)
)


rules_scheduled_changes_history = Table(
    "rules_scheduled_changes_history", metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False, autoincrement=True),
    Column("scheduled_by", String(100)),
    Column("complete", Boolean, default=False),
    Column("telemetry_product", String(15)),
    Column("telemetry_channel", String(75)),
    Column("telemetry_uptake", Integer),
    Column("data_version", Integer),
    Column("base_rule_id", Integer, autoincrement=True),
    Column("base_priority", Integer),
    Column("base_mapping", String(100)),
    Column("base_backgroundRate", Integer),
    Column("base_update_type", String(15)),
    Column("base_product", String(15)),
    Column("base_version", String(10)),
    Column("base_channel", String(75)),
    Column("base_buildTarget", String(75)),
    Column("base_buildID", String(20)),
    Column("base_locale", String(200)),
    Column("base_osVersion", String(1000)),
    Column("base_systemCapabilities", String(1000)),
    Column("base_distribution", String(100)),
    Column("base_distVersion", String(100)),
    Column("base_headerArchitecture", String(10)),
    Column("base_comment", String(500)),
    Column("base_whitelist", String(100)),
    Column("base_alias", String(50)),
    Column("base_data_version", Integer)
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
