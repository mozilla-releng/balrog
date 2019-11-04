from sqlalchemy import Column, MetaData, Table

from auslib.db import CompatibleBooleanColumn


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    mig64 = Column("mig64", CompatibleBooleanColumn)
    mig64.create(Table("rules", metadata, autoload=True))

    history_mig64 = Column("mig64", CompatibleBooleanColumn)
    history_mig64.create(Table("rules_history", metadata, autoload=True))

    base_mig64 = Column("base_mig64", CompatibleBooleanColumn)
    base_mig64.create(Table("rules_scheduled_changes", metadata, autoload=True))

    history_base_mig64 = Column("base_mig64", CompatibleBooleanColumn)
    history_base_mig64.create(Table("rules_scheduled_changes_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.mig64.drop()
    Table("rules_history", metadata, autoload=True).c.mig64.drop()
    Table("rules_scheduled_changes", metadata, autoload=True).c.base_mig64.drop()
    Table("rules_scheduled_changes_history", metadata, autoload=True).c.base_mig64.drop()
