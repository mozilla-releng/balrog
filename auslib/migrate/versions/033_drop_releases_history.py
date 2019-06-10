from sqlalchemy import Column, MetaData, String, Table, Boolean, Integer, Index, BigInteger, Text


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("releases_history", metadata, autoload=True).drop()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    if migrate_engine.name == "mysql":
        from sqlalchemy.dialects.mysql import LONGTEXT

        textType = LONGTEXT
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        textType = Text
        bigintType = Integer
    else:
        textType = Text

    releases_history = Table(
        "releases_history",
        metadata,
        Column("change_id", Integer, primary_key=True, autoincrement=True),
        Column("changed_by", String(100), nullable=False),
        Column("name", String(100), nullable=False),
        Column("product", String(15)),
        Column("data_version", Integer),
        Column("read_only", Boolean),
        Column("data", textType),
        Column("timestamp", bigintType, nullable=False),
    )
    metadata.create_all()
    Index("timestamp", releases_history.c.timestamp).create()
    Index("name", releases_history.c.timestamp).create()
