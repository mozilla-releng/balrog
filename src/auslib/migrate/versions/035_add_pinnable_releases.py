from sqlalchemy import BigInteger, Boolean, Column, Integer, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer

    pinnable_releases = Table(  # noqa
        "pinnable_releases",
        metadata,
        Column("product", String(15), nullable=False, primary_key=True),
        Column("version", String(75), nullable=False, primary_key=True),
        Column("channel", String(75), nullable=False, primary_key=True),
        Column("mapping", String(100), nullable=False),
        Column("data_version", Integer, nullable=False),
    )

    pinnable_releases_history = Table(  # noqa
        "pinnable_releases_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("product", String(15), nullable=False),
        Column("version", String(75), nullable=False),
        Column("channel", String(75), nullable=False),
        Column("mapping", String(100), nullable=True),
        Column("data_version", Integer, nullable=True),
    )

    pinnable_releases_scheduled_changes = Table(  # noqa
        "pinnable_releases_scheduled_changes",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer, nullable=False),
        Column("base_product", String(15), nullable=False),
        Column("base_version", String(75), nullable=False),
        Column("base_channel", String(75), nullable=False),
        Column("base_mapping", String(100), nullable=True),
        Column("base_data_version", Integer, nullable=True),
    )

    pinnable_releases_scheduled_changes_history = Table(  # noqa
        "pinnable_releases_scheduled_changes_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("scheduled_by", String(100)),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=True),
        Column("data_version", Integer),
        Column("base_product", String(15), nullable=True),
        Column("base_version", String(75), nullable=True),
        Column("base_channel", String(75), nullable=True),
        Column("base_mapping", String(100), nullable=True),
        Column("base_data_version", Integer, nullable=True),
    )

    pinnable_releases_scheduled_changes_conditions = Table(  # noqa
        "pinnable_releases_scheduled_changes_conditions",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("when", bigintType),
        Column("data_version", Integer, nullable=False),
    )

    pinnable_releases_scheduled_changes_conditions_history = Table(  # noqa
        "pinnable_releases_scheduled_changes_conditions_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("when", bigintType),
        Column("data_version", Integer),
    )

    pinnable_releases_scheduled_changes_signoffs = Table(  # noqa
        "pinnable_releases_scheduled_changes_signoffs",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    pinnable_releases_scheduled_changes_signoffs_history = Table(  # noqa
        "pinnable_releases_scheduled_changes_signoffs_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("username", String(100), nullable=False),
        Column("role", String(50), nullable=True),
    )

    metadata.create_all()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("pinnable_releases", metadata, autoload=True).drop()
    Table("pinnable_releases_scheduled_changes", metadata, autoload=True).drop()
    Table("pinnable_releases_scheduled_changes_history", metadata, autoload=True).drop()
    Table("pinnable_releases_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("pinnable_releases_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("pinnable_releases_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("pinnable_releases_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
