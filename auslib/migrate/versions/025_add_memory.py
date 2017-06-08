from sqlalchemy import Column, Integer, MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    memory = Column("memory", Integer)
    memory.create(Table("rules", metadata, autoload=True))

    history_memory = Column("memory", Integer)
    history_memory.create(Table("rules_history", metadata, autoload=True))

    base_memory = Column("base_memory", Integer)
    base_memory.create(Table("rules_scheduled_changes", metadata, autoload=True))

    base_memory = Column("base_memory", Integer)
    base_memory.create(Table("rules_scheduled_changes_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.memory.drop()
    Table('rules_history', metadata, autoload=True).c.memory.drop()
    Table('rules_scheduled_changes', metadata, autoload=True).c.base_memory.drop()
    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_memory.drop()
