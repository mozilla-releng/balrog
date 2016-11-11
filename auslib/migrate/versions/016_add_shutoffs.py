from sqlalchemy import Table, Column, String, MetaData, UniqueConstraint

metadata = MetaData()

shutoffs = Table(
    "shutoffs", metadata,
    Column("product", String(15), nullable=False),
    Column("channel", String(75)),
    Column("mapping", String(100)),
    UniqueConstraint('product', 'channel')
)


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.create_all()


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.create_all()
