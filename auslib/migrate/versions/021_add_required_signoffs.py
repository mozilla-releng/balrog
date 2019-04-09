from sqlalchemy import (BigInteger, Boolean, Column, Integer, MetaData, String,
                        Table)


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer

    product_required_signoffs = Table( # noqa
        "product_req_signoffs", metadata,
        Column("product", String(15), primary_key=True),
        Column("channel", String(75), primary_key=True),
        Column("role", String(50), primary_key=True),
        Column("signoffs_required", Integer, nullable=False),
        Column("data_version", Integer, nullable=False),
    )

    product_required_signoffs_history = Table(
        "product_req_signoffs_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("product", String(15), nullable=False),
        Column("channel", String(75), nullable=False),
        Column("role", String(50), nullable=False),
        Column("signoffs_required", Integer),
        Column("data_version", Integer),
    )
    product_required_signoffs_history.append_column(Column("timestamp", bigintType, nullable=False))

    product_required_signoffs_scheduled_changes = Table( # noqa
        "product_req_signoffs_scheduled_changes", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer, nullable=False),
        Column("base_product", String(15), nullable=False),
        Column("base_channel", String(75), nullable=False),
        Column("base_role", String(50), nullable=False),
        Column("base_signoffs_required", Integer),
        Column("base_data_version", Integer),
    )

    product_required_signoffs_scheduled_changes_history = Table(
        "product_req_signoffs_scheduled_changes_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=True),
        Column("scheduled_by", String(100)),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50)),
        Column("data_version", Integer),
        Column("base_product", String(15)),
        Column("base_channel", String(75)),
        Column("base_role", String(50)),
        Column("base_signoffs_required", Integer),
        Column("base_data_version", Integer),
    )
    product_required_signoffs_scheduled_changes_history.append_column(Column("timestamp", bigintType, nullable=False))

    product_required_signoffs_scheduled_changes_conditions = Table(
        "product_req_signoffs_scheduled_changes_conditions", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("data_version", Integer),
    )
    product_required_signoffs_scheduled_changes_conditions.append_column(Column("when", bigintType))

    product_required_signoffs_scheduled_changes_conditions_history = Table(
        "product_req_signoffs_scheduled_changes_conditions_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("data_version", Integer),
    )
    product_required_signoffs_scheduled_changes_conditions_history.append_column(Column("timestamp", bigintType, nullable=False))
    product_required_signoffs_scheduled_changes_conditions_history.append_column(Column("when", bigintType))

    product_required_signoffs_scheduled_changes_signoffs = Table( # noqa
        "product_req_signoffs_scheduled_changes_signoffs", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    product_required_signoffs_scheduled_changes_signoffs_history = Table( # noqa
        "product_req_signoffs_scheduled_changes_signoffs_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=False),
        Column("username", String(100), nullable=False),
        Column("role", String(50)),
    )
    product_required_signoffs_scheduled_changes_signoffs_history.append_column(Column("timestamp", bigintType, nullable=False))

    permissions_signoffs = Table( # noqa
        "permissions_req_signoffs", metadata,
        Column("product", String(15), primary_key=True),
        Column("role", String(50), primary_key=True),
        Column("signoffs_required", Integer, nullable=False),
        Column("data_version", Integer, nullable=False),
    )

    permissions_signoffs_history = Table(
        "permissions_req_signoffs_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("product", String(15), nullable=False),
        Column("role", String(50), nullable=False),
        Column("signoffs_required", Integer),
        Column("data_version", Integer),
    )
    permissions_signoffs_history.append_column(Column("timestamp", bigintType, nullable=False))

    permissions_signoffs_scheduled_changes = Table( # noqa
        "permissions_req_signoffs_scheduled_changes", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("scheduled_by", String(100), nullable=False),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50), nullable=False),
        Column("data_version", Integer, nullable=False),
        Column("base_product", String(15), nullable=False),
        Column("base_role", String(50), nullable=False),
        Column("base_signoffs_required", Integer),
        Column("base_data_version", Integer),
    )

    permissions_signoffs_scheduled_changes_history = Table(
        "permissions_req_signoffs_scheduled_changes_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=True),
        Column("scheduled_by", String(100)),
        Column("complete", Boolean, default=False),
        Column("change_type", String(50)),
        Column("data_version", Integer),
        Column("base_product", String(15)),
        Column("base_role", String(50)),
        Column("base_signoffs_required", Integer),
        Column("base_data_version", Integer),
    )
    permissions_signoffs_scheduled_changes_history.append_column(Column("timestamp", bigintType, nullable=False))

    permissions_signoffs_scheduled_changes_conditions = Table(
        "permissions_req_signoffs_scheduled_changes_conditions", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=True),
        Column("data_version", Integer),
    )
    permissions_signoffs_scheduled_changes_conditions.append_column(Column("when", bigintType))

    permissions_signoffs_scheduled_changes_conditions_history = Table(
        "permissions_req_signoffs_scheduled_changes_conditions_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False),
        Column("data_version", Integer),
    )
    permissions_signoffs_scheduled_changes_conditions_history.append_column(Column("timestamp", bigintType, nullable=False))
    permissions_signoffs_scheduled_changes_conditions_history.append_column(Column("when", bigintType))

    permissions_signoffs_scheduled_changes_signoffs = Table( # noqa
        "permissions_req_signoffs_scheduled_changes_signoffs", metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    permissions_signoffs_scheduled_changes_signoffs_history = Table( # noqa
        "permissions_req_signoffs_scheduled_changes_signoffs_history", metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=False),
        Column("username", String(100), nullable=False),
        Column("role", String(50)),
    )
    permissions_signoffs_scheduled_changes_signoffs_history.append_column(Column("timestamp", bigintType, nullable=False))

    metadata.create_all()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("product_req_signoffs", metadata, autoload=True).drop()
    Table("product_req_signoffs_history", metadata, autoload=True).drop()
    Table("product_req_signoffs_scheduled_changes", metadata, autoload=True).drop()
    Table("product_req_signoffs_scheduled_changes_history", metadata, autoload=True).drop()
    Table("product_req_signoffs_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("product_req_signoffs_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("product_req_signoffs_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("product_req_signoffs_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
    Table("permissions_req_signoffs", metadata, autoload=True).drop()
    Table("permissions_req_signoffs_history", metadata, autoload=True).drop()
    Table("permissions_req_signoffs_scheduled_changes", metadata, autoload=True).drop()
    Table("permissions_req_signoffs_scheduled_changes_history", metadata, autoload=True).drop()
    Table("permissions_req_signoffs_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("permissions_req_signoffs_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("permissions_req_signoffs_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("permissions_req_signoffs_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
