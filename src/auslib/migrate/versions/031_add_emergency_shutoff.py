from sqlalchemy import BigInteger, Boolean, Column, Integer, MetaData, String, Table

metadata = MetaData()


emergency_shutoffs = Table(
    "emergency_shutoffs",
    metadata,
    Column("product", String(15), nullable=False, primary_key=True),
    Column("channel", String(75), nullable=False, primary_key=True),
    Column("data_version", Integer, nullable=False),
)


emergency_shutoffs_history = Table(
    "emergency_shutoffs_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("product", String(15), nullable=False),
    Column("channel", String(75), nullable=False),
    Column("data_version", Integer),
)


emergency_shutoffs_scheduled_changes = Table(
    "emergency_shutoffs_scheduled_changes",
    metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=True),
    Column("scheduled_by", String(100), nullable=False),
    Column("complete", Boolean, default=False),
    Column("change_type", String(50), nullable=False),
    Column("data_version", Integer, nullable=False),
    Column("base_product", String(15), nullable=False),
    Column("base_channel", String(75), nullable=False),
    Column("base_data_version", Integer),
)


emergency_shutoffs_scheduled_changes_history = Table(
    "emergency_shutoffs_scheduled_changes_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False, autoincrement=True),
    Column("scheduled_by", String(100)),
    Column("complete", Boolean, default=False),
    Column("change_type", String(50)),
    Column("data_version", Integer),
    Column("base_product", String(15)),
    Column("base_channel", String(75)),
    Column("base_data_version", Integer),
)


emergency_shutoffs_scheduled_changes_conditions = Table(
    "emergency_shutoffs_scheduled_changes_conditions",
    metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=True),
    Column("data_version", Integer, nullable=False),
)


emergency_shutoffs_scheduled_changes_conditions_history = Table(
    "emergency_shutoffs_scheduled_changes_conditions_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False),
    Column("data_version", Integer),
)


emergency_shutoffs_scheduled_changes_signoffs = Table(
    "emergency_shutoffs_scheduled_changes_signoffs",
    metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=False),
    Column("username", String(100), primary_key=True),
    Column("role", String(50), nullable=False),
)


emergency_shutoffs_scheduled_changes_signoffs_history = Table(
    "emergency_shutoffs_scheduled_changes_signoffs_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False, autoincrement=False),
    Column("username", String(100), nullable=False),
    Column("role", String(50)),
)


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    bigintType = BigInteger

    if migrate_engine.name == "sqlite":
        bigintType = Integer

    emergency_shutoffs_history.append_column(Column("timestamp", bigintType, nullable=False))

    emergency_shutoffs_scheduled_changes_history.append_column(
        Column("timestamp", bigintType, nullable=False)
    )

    emergency_shutoffs_scheduled_changes_conditions.append_column(Column("when", bigintType))
    emergency_shutoffs_scheduled_changes_conditions_history.append_column(
        Column("when", bigintType)
    )
    emergency_shutoffs_scheduled_changes_conditions_history.append_column(
        Column("timestamp", bigintType, nullable=False)
    )

    emergency_shutoffs_scheduled_changes_signoffs_history.append_column(
        Column("timestamp", bigintType, nullable=False)
    )

    metadata.create_all()


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    Table("emergency_shutoffs", metadata, autoload=True).drop()
    Table("emergency_shutoffs_history", metadata, autoload=True).drop()
    Table("emergency_shutoffs_scheduled_changes", metadata, autoload=True).drop()
    Table("emergency_shutoffs_scheduled_changes_history", metadata, autoload=True).drop()
    Table("emergency_shutoffs_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("emergency_shutoffs_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("emergency_shutoffs_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("emergency_shutoffs_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
