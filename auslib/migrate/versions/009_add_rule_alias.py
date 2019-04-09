from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    alias = Column("alias", String(50), unique=True)
    alias.create(Table("rules", metadata, autoload=True), unique_name="alias_unique")

    history_alias = Column("alias", String(50))
    history_alias.create(Table("rules_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.alias.drop()
    Table("rules_history", metadata, autoload=True).c.alias.drop()
