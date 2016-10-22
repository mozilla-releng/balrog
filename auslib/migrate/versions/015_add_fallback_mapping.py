from sqlalchemy import Column, String, MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    fallbackMapping = Column("fallbackMapping", String(1000))
    fallbackMapping.create(Table("rules", metadata, autoload=True))

    history_fallbackMapping = Column("fallbackMapping", String(1000))
    history_fallbackMapping.create(Table("rules_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.fallbackMapping.drop()
    Table('rules_history', metadata, autoload=True).c.fallbackMapping.drop()

