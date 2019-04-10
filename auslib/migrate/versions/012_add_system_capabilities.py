from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    systemCapabilities = Column("systemCapabilities", String(1000))
    systemCapabilities.create(Table("rules", metadata, autoload=True))

    history_systemCapabilities = Column("systemCapabilities", String(1000))
    history_systemCapabilities.create(Table("rules_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.systemCapabilities.drop()
    Table("rules_history", metadata, autoload=True).c.systemCapabilities.drop()
