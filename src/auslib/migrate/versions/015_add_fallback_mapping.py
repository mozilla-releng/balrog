from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    fallbackMapping = Column("fallbackMapping", String(100))
    fallbackMapping.create(Table("rules", metadata, autoload=True))

    history_fallbackMapping = Column("fallbackMapping", String(100))
    history_fallbackMapping.create(Table("rules_history", metadata, autoload=True))

    base_fallbackMapping = Column("base_fallbackMapping", String(100))
    base_fallbackMapping.create(Table("rules_scheduled_changes", metadata, autoload=True))

    base_fallbackMapping = Column("base_fallbackMapping", String(100))
    base_fallbackMapping.create(Table("rules_scheduled_changes_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.fallbackMapping.drop()
    Table("rules_history", metadata, autoload=True).c.fallbackMapping.drop()
    Table("rules_scheduled_changes", metadata, autoload=True).c.fallbackMapping.drop()
    Table("rules_scheduled_changes_history", metadata, autoload=True).c.fallbackMapping.drop()
