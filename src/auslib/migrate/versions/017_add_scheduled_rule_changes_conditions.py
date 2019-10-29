from sqlalchemy import BigInteger, Column, Integer, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    # To preserve any existing data, we must do a few things in a particular order:
    # 1) Create the new Conditions tables.
    rules_scheduled_changes_conditions = Table(
        "rules_scheduled_changes_conditions",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("telemetry_product", String(15)),
        Column("telemetry_channel", String(75)),
        Column("telemetry_uptake", Integer),
        Column("data_version", Integer),
    )

    rules_scheduled_changes_conditions_history = Table(
        "rules_scheduled_changes_conditions_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=True),
        Column("telemetry_product", String(15)),
        Column("telemetry_channel", String(75)),
        Column("telemetry_uptake", Integer),
        Column("data_version", Integer),
    )
    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer
    rules_scheduled_changes_conditions.append_column(Column("when", bigintType))
    rules_scheduled_changes_conditions_history.append_column(Column("when", bigintType))
    rules_scheduled_changes_conditions_history.append_column(Column("timestamp", bigintType, nullable=False))
    metadata.create_all()

    # 2) Copy the conditions from the existing Scheduled Changes tables to them.
    migrate_engine.execute(
        """INSERT INTO rules_scheduled_changes_conditions
(sc_id, telemetry_product, telemetry_channel, telemetry_uptake, data_version, `when`)
SELECT sc_id, telemetry_product, telemetry_channel, telemetry_uptake, data_version, `when` from rules_scheduled_changes;
"""
    )
    migrate_engine.execute(
        """INSERT INTO rules_scheduled_changes_conditions_history
(change_id, changed_by, timestamp, sc_id, telemetry_product, telemetry_channel, telemetry_uptake, data_version, `when`)
SELECT change_id, changed_by, timestamp, sc_id, telemetry_product, telemetry_channel, telemetry_uptake,
       data_version, `when` from rules_scheduled_changes_history;
"""
    )

    # 3) _Then_ drop the conditions columns from the existing Tables.
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
