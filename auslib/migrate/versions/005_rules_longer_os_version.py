from sqlalchemy import MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.osVersion.alter(type=String(1000))
    Table('rules_history', metadata, autoload=True).c.osVersion.alter(type=String(1000))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.osVersion.alter(type=String(100))
    Table('rules_history', metadata, autoload=True).c.osVersion.alter(type=String(100))
