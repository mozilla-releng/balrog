from sqlalchemy import BigInteger, Column, Integer, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    rules_scheduled_changes_signoffs = Table(  # noqa - to hush pyflakes about this not being used.
        "rules_scheduled_changes_signoffs",
        metadata,
        Column("sc_id", Integer, primary_key=True, autoincrement=False),
        Column("username", String(100), primary_key=True),
        Column("role", String(50), nullable=False),
    )

    rules_scheduled_changes_signoffs_history = Table(
        "rules_scheduled_changes_signoffs_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("sc_id", Integer, nullable=False, autoincrement=False),
        Column("username", String(100), nullable=False),
        Column("role", String(50)),
    )
    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer
    rules_scheduled_changes_signoffs_history.append_column(Column("timestamp", bigintType, nullable=False))
    metadata.create_all()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("rules_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("rules_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
