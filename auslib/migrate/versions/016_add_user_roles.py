from sqlalchemy import BigInteger, Column, Integer, MetaData, String, Table

metadata = MetaData()

user_roles = Table(
    "user_roles", metadata, Column("username", String(100), primary_key=True), Column("role", String(50), primary_key=True), Column("data_version", Integer)
)

user_roles_history = Table(
    "user_roles_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("username", String(100), nullable=False),
    Column("role", String(50), nullable=False),
    Column("data_version", Integer),
)


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    if migrate_engine.name == "mysql":
        bigintType = BigInteger
    elif migrate_engine.name == "sqlite":
        bigintType = Integer
    user_roles_history.append_column(Column("timestamp", bigintType, nullable=False))
    metadata.create_all()
