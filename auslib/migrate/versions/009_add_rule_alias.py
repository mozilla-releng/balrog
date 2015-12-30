from sqlalchemy import Column, String, MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    def add_alias(table):
        alias = Column('alias', String(50))
        alias.create(table)
    add_alias(Table('rules', metadata, autoload=True))
    add_alias(Table('rules_history', metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.alias.drop()
    Table('rules_history', metadata, autoload=True).c.alias.drop()
