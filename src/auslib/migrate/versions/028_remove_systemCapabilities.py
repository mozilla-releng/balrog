from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    Table("rules", metadata, autoload=True).c.systemCapabilities.drop()
    Table("rules_history", metadata, autoload=True).c.systemCapabilities.drop()
    Table("rules_scheduled_changes", metadata, autoload=True).c.base_systemCapabilities.drop()
    Table(
        "rules_scheduled_changes_history", metadata, autoload=True
    ).c.base_systemCapabilities.drop()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    systemCapabilities = Column("systemCapabilities", String(1000))
    systemCapabilities.create(Table("rules", metadata, autoload=True))

    history_systemCapabilities = Column("systemCapabilities", String(1000))
    history_systemCapabilities.create(Table("rules_history", metadata, autoload=True))

    base_systemCapabilities = Column("base_systemCapabilities", String(1000))
    base_systemCapabilities.create(Table("rules_scheduled_changes", metadata, autoload=True))

    base_systemCapabilities = Column("base_systemCapabilities", String(1000))
    base_systemCapabilities.create(
        Table("rules_scheduled_changes_history", metadata, autoload=True)
    )

    # make a best effort to restore the data
    conn = migrate_engine.connect()
    conn.execute("UPDATE rules SET systemCapabilities=instructionSet;")
    conn.execute("UPDATE rules_history SET systemCapabilities=instructionSet;")
    conn.execute("UPDATE rules_scheduled_changes SET base_systemCapabilities=base_instructionSet;")
    conn.execute(
        "UPDATE rules_scheduled_changes_history SET base_systemCapabilities=base_instructionSet;"
    )
    conn.close()
