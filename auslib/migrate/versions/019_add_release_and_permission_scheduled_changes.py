from sqlalchemy import Table, Column, Integer, String, MetaData, \
    BigInteger, Boolean, Text


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    if migrate_engine.name == "mysql":
        from sqlalchemy.dialects.mysql import LONGTEXT
        bigintType = BigInteger
        dataType = LONGTEXT
    elif migrate_engine.name == "sqlite":
        bigintType = Integer
        dataType = Text

    releases_scheduled_changes = Table(
        "releases_scheduled_changes", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer),
        Column("base_name", String(100), nullable=False),
        Column("base_product", String(15), nullable=False),
        Column("base_read_only", Boolean, default=False),
        Column("base_data_version", Integer),
    )

    releases_scheduled_changes_history = Table(
        "releases_scheduled_changes_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("scheduled_by", String(100)),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=True),
        Column("data_version", Integer),
        Column("base_name", String(100)),
        Column("base_product", String(15)),
        Column("base_read_only", Boolean, default=False),
        Column("base_data_version", Integer)
    )

    releases_scheduled_changes_conditions = Table(
        "releases_scheduled_changes_conditions", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("data_version", Integer),
    )

    releases_scheduled_changes_conditions_history = Table(
        "releases_scheduled_changes_conditions_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("data_version", Integer),
    )

    releases_scheduled_changes.append_column(Column("base_data", dataType, nullable=False))
    releases_scheduled_changes_history.append_column(Column("base_data", dataType))
    releases_scheduled_changes_history.append_column(Column("timestamp", bigintType, nullable=False))
    releases_scheduled_changes_conditions.append_column(Column("when", bigintType))
    releases_scheduled_changes_conditions_history.append_column(Column("when", bigintType))
    releases_scheduled_changes_conditions_history.append_column(Column("timestamp", bigintType, nullable=False))

    permissions_scheduled_changes = Table( # noqa
        "permissions_scheduled_changes", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer),
        Column('base_permission', String(50), nullable=False),
        Column('base_username', String(100), nullable=False),
        Column('base_options', Text),
        Column("base_data_version", Integer),
    )

    permissions_scheduled_changes_history = Table(
        "permissions_scheduled_changes_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("scheduled_by", String(100)),
        Column("change_type", String(50), nullable=True),
        Column("complete", Boolean, default=False),
        Column("data_version", Integer),
        Column('base_permission', String(50)),
        Column('base_username', String(100)),
        Column('base_options', Text),
        Column("base_data_version", Integer)
    )

    permissions_scheduled_changes_conditions = Table(
        "permissions_scheduled_changes_conditions", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("data_version", Integer),
    )

    permissions_scheduled_changes_conditions_history = Table(
        "permissions_scheduled_changes_conditions_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("data_version", Integer),
    )

    permissions_scheduled_changes_history.append_column(Column("timestamp", bigintType, nullable=False))
    permissions_scheduled_changes_conditions.append_column(Column("when", bigintType))
    permissions_scheduled_changes_conditions_history.append_column(Column("when", bigintType))
    permissions_scheduled_changes_conditions_history.append_column(Column("timestamp", bigintType, nullable=False))

    metadata.create_all()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("releases_scheduled_changes", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_history", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_history", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_conditions_history", metadata, autoload=True).drop()
