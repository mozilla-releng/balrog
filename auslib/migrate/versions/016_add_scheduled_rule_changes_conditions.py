from sqlalchemy import Table, Column, Integer, String, MetaData, \
    BigInteger



# TODO: migrate data from sc -> sc conditions before deleting
def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    rules_scheduled_changes_conditions = Table(
        "rules_scheduled_changes_conditions", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("telemetry_product", String(15)),
        Column("telemetry_channel", String(75)),
        Column("telemetry_uptake", Integer),
        Column("data_version", Integer),
    )

    rules_scheduled_changes_conditions_history = Table(
        "rules_scheduled_changes_conditions_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=True),
        Column("telemetry_product", String(15)),
        Column("telemetry_channel", String(75)),
        Column("telemetry_uptake", Integer),
        Column("data_version", Integer),
    )
    rules_scheduled_changes = Table("rules_scheduled_changes", metadata, autoload=True)
    rules_scheduled_changes.c.when.drop()
    rules_scheduled_changes.c.telemetry_product.drop()
    rules_scheduled_changes.c.telemetry_channel.drop()
    rules_scheduled_changes.c.telemetry_uptake.drop()
    rules_scheduled_changes_history = Table("rules_scheduled_changes_history", metadata, autoload=True)
    rules_scheduled_changes_history.c.when.drop()
    rules_scheduled_changes_history.c.telemetry_product.drop()
    rules_scheduled_changes_history.c.telemetry_channel.drop()
    rules_scheduled_changes_history.c.telemetry_uptake.drop()

    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer
    rules_scheduled_changes_conditions.append_column(Column("when", bigintType))
    rules_scheduled_changes_conditions_history.append_column(Column("when", bigintType))
    rules_scheduled_changes_conditions_history.append_column(Column("timestamp", bigintType, nullable=False))
    metadata.create_all()
