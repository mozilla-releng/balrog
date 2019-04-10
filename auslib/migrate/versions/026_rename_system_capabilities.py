def upgrade(migrate_engine):
    pass
    # Migration disabled prior to code going to production. This was replaced by
    # a two part migration that added instructionSet in one migration, and
    # removed systemRequirements in another.


#    metadata = MetaData(bind=migrate_engine)
#    Table('rules', metadata, autoload=True).c.systemCapabilities.alter(name="instructionSet")
#    Table('rules_history', metadata, autoload=True).c.systemCapabilities.alter(name="instructionSet")
#    Table('rules_scheduled_changes', metadata, autoload=True).c.base_systemCapabilities.alter(name="base_instructionSet")
#    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_systemCapabilities.alter(name="base_instructionSet")


def downgrade(migrate_engine):
    pass
    # Migration disabled prior to code going to production. This was replaced by
    # a two part migration that added instructionSet in one migration, and
    # removed systemRequirements in another.


#    metadata = MetaData(bind=migrate_engine)
#    Table('rules', metadata, autoload=True).c.instructionSet.alter(name="systemCapabilities")
#    Table('rules_history', metadata, autoload=True).c.instructionSet.alter(name="systemCapabilities")
#    Table('rules_scheduled_changes', metadata, autoload=True).c.base_instructionSet.alter(name="base_systemCapabilities")
#    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_instructionSet.alter(name="base_systemCapabilities")
