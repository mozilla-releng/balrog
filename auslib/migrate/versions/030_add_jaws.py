from sqlalchemy import Column, MetaData, Table

from auslib.db import CompatibleBooleanColumn


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    jaws = Column("jaws", CompatibleBooleanColumn)
    jaws.create(Table("rules", metadata, autoload=True))

    history_jaws = Column("jaws", CompatibleBooleanColumn)
    history_jaws.create(Table("rules_history", metadata, autoload=True))

    base_jaws = Column("base_jaws", CompatibleBooleanColumn)
    base_jaws.create(Table("rules_scheduled_changes", metadata, autoload=True))

    history_base_jaws = Column("base_jaws", CompatibleBooleanColumn)
    history_base_jaws.create(Table("rules_scheduled_changes_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.jaws.drop()
    Table('rules_history', metadata, autoload=True).c.jaws.drop()
    Table('rules_scheduled_changes', metadata, autoload=True).c.base_jaws.drop()
    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_jaws.drop()
