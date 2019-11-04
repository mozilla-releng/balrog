from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    instructionSet = Column("instructionSet", String(1000))
    instructionSet.create(Table("rules", metadata, autoload=True))

    history_instructionSet = Column("instructionSet", String(1000))
    history_instructionSet.create(Table("rules_history", metadata, autoload=True))

    base_instructionSet = Column("base_instructionSet", String(1000))
    base_instructionSet.create(Table("rules_scheduled_changes", metadata, autoload=True))

    base_instructionSet = Column("base_instructionSet", String(1000))
    base_instructionSet.create(Table("rules_scheduled_changes_history", metadata, autoload=True))

    # systemCapabilities -> instructionSet is a two-part rename (we create the new column in one migration,
    # and drop it in the next), so we need to copy data over.
    conn = migrate_engine.connect()
    conn.execute("UPDATE rules SET instructionSet=systemCapabilities;")
    conn.execute("UPDATE rules_history SET instructionSet=systemCapabilities;")
    conn.execute("UPDATE rules_scheduled_changes SET base_instructionSet=base_systemCapabilities;")
    conn.execute(
        "UPDATE rules_scheduled_changes_history SET base_instructionSet=base_systemCapabilities;"
    )
    conn.close()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.instructionSet.drop()
    Table("rules_history", metadata, autoload=True).c.instructionSet.drop()
    Table("rules_scheduled_changes", metadata, autoload=True).c.base_instructionSet.drop()
    Table("rules_scheduled_changes_history", metadata, autoload=True).c.base_instructionSet.drop()
