from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    # In order to add a column a nullable=False:
    # 1) Add the column with nullable=True
    change_type = Column("change_type", String(50))
    change_type.create(Table("rules_scheduled_changes", metadata, autoload=True))

    # 2) Update the values of change_type depending on base_data_version

    migrate_engine.execute("""
        UPDATE rules_scheduled_changes
        SET change_type = "insert"
        WHERE base_data_version is NULL;
        """)
    migrate_engine.execute("""
        UPDATE rules_scheduled_changes
        SET change_type = "update"
        WHERE base_data_version is not NULL;
        """)

    # 3) Alter the column and set nullable=False
    change_type.alter(nullable=False)

    change_type = Column("change_type", String(50))
    change_type.create(Table("rules_scheduled_changes_history", metadata,
                             autoload=True))

    migrate_engine.execute("""
        UPDATE rules_scheduled_changes_history
        SET change_type = "insert"
        WHERE base_data_version is NULL;
        """)
    migrate_engine.execute("""
        UPDATE rules_scheduled_changes_history
        SET change_type = "update"
        WHERE base_data_version is not NULL;
        """)
    rules_scheduled_changes = Table("rules_scheduled_changes", metadata, autoload=True)
    rules_scheduled_changes.c.base_update_type.alter(nullable=True)


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules_scheduled_changes", metadata, autoload=True).c.change_type.drop()
    Table("rules_scheduled_changes_history", metadata,
          autoload=True).c.change_type.drop()
