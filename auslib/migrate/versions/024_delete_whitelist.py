from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("rules", metadata, autoload=True).c.whitelist.drop()
    Table("rules_history", metadata, autoload=True).c.whitelist.drop()
    Table("rules_scheduled_changes_history", metadata, autoload=True).c.base_whitelist.drop()
    Table("rules_scheduled_changes", metadata, autoload=True).c.base_whitelist.drop()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    def add_whitelist(table):
        whitelist = Column("whitelist", String(100))
        whitelist.create(table)

    add_whitelist(Table("rules", metadata, autoload=True))
    add_whitelist(Table("rules_history", metadata, autoload=True))

    def add_base_whitelist(table):
        base_whitelist = Column("base_whitelist", String(100))
        base_whitelist.create(table)

    add_base_whitelist(Table("rules_scheduled_changes", metadata, autoload=True))
    add_base_whitelist(Table("rules_scheduled_changes_history", metadata, autoload=True))
