from sqlalchemy import MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.systemCapabilities.alter(name="instructionSet")
    Table('rules_history', metadata, autoload=True).c.systemCapabilities.alter(name="instructionSet")
    Table('rules_scheduled_changes', metadata, autoload=True).c.base_systemCapabilities.alter(name="base_instructionSet")
    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_systemCapabilities.alter(name="base_instructionSet")


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.instructionSet.alter(name="systemCapabilities")
    Table('rules_history', metadata, autoload=True).c.instructionSet.alter(name="systemCapabilities")
    Table('rules_scheduled_changes', metadata, autoload=True).c.base_instructionSet.alter(name="base_systemCapabilities")
    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_instructionSet.alter(name="base_systemCapabilities")
