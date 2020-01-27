from sqlalchemy import JSON, BigInteger, Boolean, Column, Integer, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer

    releases_json = Table(  # noqa
        "releases_json",
        metadata,
        Column("name", String(100), primary_key=True),
        Column("product", String(15), nullable=False),
        Column("read_only", Boolean, default=False),
        Column("data", JSON),
        Column("data_version", Integer, nullable=False),
    )

    releases_json_scheduled_changes = Table(  # noqa
        "releases_json_scheduled_changes",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer, nullable=False),
        Column("base_name", String(100), nullable=False),
        Column("base_product", String(15)),
        Column("base_data", JSON),
        Column("base_read_only", Boolean, default=False),
        Column("base_data_version", Integer),
    )

    releases_json_scheduled_changes_history = Table(  # noqa
        "releases_json_scheduled_changes_history",
        metadata,
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
        Column("base_data", JSON),
        Column("base_read_only", Boolean, default=False),
        Column("base_data_version", Integer),
    )

    releases_json_scheduled_changes_conditions = Table(  # noqa
        "releases_json_scheduled_changes_conditions",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("when", bigintType),
        Column("data_version", Integer, nullable=False),
    )

    releases_json_scheduled_changes_conditions_history = Table(  # noqa
        "releases_json_scheduled_changes_conditions_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("when", bigintType),
        Column("data_version", Integer),
    )

    releases_json_scheduled_changes_signoffs = Table(  # noqa
        "releases_json_scheduled_changes_signoffs",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    releases_json_scheduled_changes_signoffs_history = Table(  # noqa
        "releases_json_scheduled_changes_signoffs_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=False),
        Column("username", String(100), nullable=False),
        Column("role", String(50)),
    )

    release_assets = Table(  # noqa
        "release_assets",
        metadata,
        Column("name", String(100), primary_key=True),
        Column("path", String(200), primary_key=True),
        Column("data", JSON),
        Column("data_version", Integer, nullable=False),
    )

    release_assets_scheduled_changes = Table(  # noqa
        "release_assets_scheduled_changes",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer, nullable=False),
        Column("base_name", String(100), nullable=False),
        Column("base_path", String(200), nullable=False),
        Column("base_data", JSON),
        Column("base_data_version", Integer),
    )

    release_assets_scheduled_changes_history = Table(  # noqa
        "release_assets_scheduled_changes_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("scheduled_by", String(100)),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=True),
        Column("data_version", Integer),
        Column("base_name", String(100)),
        Column("base_path", String(200)),
        Column("base_data", JSON),
        Column("base_data_version", Integer),
    )

    release_assets_scheduled_changes_conditions = Table(  # noqa
        "release_assets_scheduled_changes_conditions",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("when", bigintType),
        Column("data_version", Integer, nullable=False),
    )

    release_assets_scheduled_changes_conditions_history = Table(  # noqa
        "release_assets_scheduled_changes_conditions_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("timestamp", bigintType, nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("when", bigintType),
        Column("data_version", Integer),
    )

    release_assets_scheduled_changes_signoffs = Table(  # noqa
        "release_assets_scheduled_changes_signoffs",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    release_assets_scheduled_changes_signoffs_history = Table(  # noqa
        "release_assets_scheduled_changes_signoffs_history",
        metadata,
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

    Table("releases_json", metadata, autoload=True).drop()
    Table("releases_json_scheduled_changes", metadata, autoload=True).drop()
    Table("releases_json_scheduled_changes_history", metadata, autoload=True).drop()
    Table("releases_json_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("releases_json_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("releases_json_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("releases_json_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
    Table("release_assets", metadata, autoload=True).drop()
    Table("release_assets_scheduled_changes", metadata, autoload=True).drop()
    Table("release_assets_scheduled_changes_history", metadata, autoload=True).drop()
    Table("release_assets_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("release_assets_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("release_assets_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("release_assets_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
