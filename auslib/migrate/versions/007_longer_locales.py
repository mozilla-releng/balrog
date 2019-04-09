from sqlalchemy import MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.locale.alter(type=String(200))
    Table('rules_history', metadata, autoload=True).c.locale.alter(type=String(200))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.locale.alter(type=String(10))
    Table('rules_history', metadata, autoload=True).c.locale.alter(type=String(10))
