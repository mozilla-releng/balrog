from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    def add_whitelist(table):
        whitelist = Column('whitelist', String(100))
        whitelist.create(table)
    add_whitelist(Table('rules', metadata, autoload=True))
    add_whitelist(Table('rules_history', metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.whitelist.drop()
    Table('rules_history', metadata, autoload=True).c.whitelist.drop()
