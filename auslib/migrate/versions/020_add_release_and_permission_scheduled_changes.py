from sqlalchemy import (BigInteger, Boolean, Column, Integer, MetaData, String,
                        Table, Text)


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    if migrate_engine.name == "mysql":
        from sqlalchemy.dialects.mysql import LONGTEXT
        bigintType = BigInteger
        dataType = LONGTEXT
    elif migrate_engine.name == "sqlite":
        bigintType = Integer
        dataType = Text

    releases_scheduled_changes = Table( # noqa - to hush pyflakes about this not being used
        "releases_scheduled_changes", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer),
        Column("base_name", String(100), nullable=False),
        Column("base_product", String(15)),
        Column("base_data", dataType),
        Column("base_read_only", Boolean, default=False),
        Column("base_data_version", Integer),
    )

    releases_scheduled_changes_history = Table( # noqa
        "releases_scheduled_changes_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("scheduled_by", String(100)),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=True),
        Column("data_version", Integer),
        Column("base_name", String(100)),
        Column("base_product", String(15)),
        Column("base_data", dataType),
        Column("base_read_only", Boolean, default=False),
        Column("base_data_version", Integer)
    )

    releases_scheduled_changes_conditions = Table( # noqa
        "releases_scheduled_changes_conditions", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("when", bigintType, nullable=False),
        Column("data_version", Integer),
    )

    releases_scheduled_changes_conditions_history = Table( # noqa
        "releases_scheduled_changes_conditions_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("when", bigintType),
        Column("data_version", Integer),
    )

    releases_scheduled_changes_signoffs = Table( # noqa
        "releases_scheduled_changes_signoffs", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    releases_scheduled_changes_signoffs_history = Table( # noqa
        "releases_scheduled_changes_signoffs_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=False),
        Column("username", String(100), nullable=False),
        Column("role", String(50)),
    )

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

    permissions_scheduled_changes_history = Table( # noqa
        "permissions_scheduled_changes_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
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

    permissions_scheduled_changes_conditions = Table( # noqa
        "permissions_scheduled_changes_conditions", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("when", bigintType, nullable=False),
        Column("data_version", Integer),
    )

    permissions_scheduled_changes_conditions_history = Table( # noqa
        "permissions_scheduled_changes_conditions_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("when", bigintType),
        Column("data_version", Integer),
    )

    permissions_scheduled_changes_signoffs = Table( # noqa
        "permissions_scheduled_changes_signoffs", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    permissions_scheduled_changes_signoffs_history = Table( # noqa
        "permissions_scheduled_changes_signoffs_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=False),
        Column("username", String(100), nullable=False),
        Column("role", String(50)),
    )

    metadata.create_all()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("releases_scheduled_changes", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_history", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("releases_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_history", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("permissions_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
