from sqlalchemy import Column, MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    def get_column_type():
        if migrate_engine.name == "mysql":
            from sqlalchemy.dialects.mysql import BIT
            return BIT
        else:
            from sqlalchemy import Integer
            return Integer

    mig64 = Column("mig64", get_column_type())
    mig64.create(Table("rules", metadata, autoload=True))

    history_mig64 = Column("mig64", get_column_type())
    history_mig64.create(Table("rules_history", metadata, autoload=True))

    base_mig64 = Column("base_mig64", get_column_type())
    base_mig64.create(Table("rules_scheduled_changes", metadata, autoload=True))

    base_mig64 = Column("base_mig64", get_column_type())
    base_mig64.create(Table("rules_scheduled_changes_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.mig64.drop()
    Table('rules_history', metadata, autoload=True).c.mig64.drop()
    Table('rules_scheduled_changes', metadata, autoload=True).c.base_mig64.drop()
    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_mig64.drop()
