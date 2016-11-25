from sqlalchemy import Column, String, MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    change_type = Column("change_type", String(50))
    change_type.create(Table("rules_scheduled_changes", metadata, autoload=True))

    change_type = Column("change_type", String(50))
    change_type.create(Table("rules_scheduled_changes_history", metadata,
                             autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules_scheduled_changes", metadata, autoload=True).c.change_type.drop()
    Table("rules_scheduled_changes_history", metadata,
          autoload=True).c.change_type.drop()
