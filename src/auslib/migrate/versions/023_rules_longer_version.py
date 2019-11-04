from sqlalchemy import MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.version.alter(type=String(75))
    Table("rules_history", metadata, autoload=True).c.version.alter(type=String(75))
    Table("rules_scheduled_changes", metadata, autoload=True).c.base_version.alter(type=String(75))
    Table("rules_scheduled_changes_history", metadata, autoload=True).c.base_version.alter(
        type=String(75)
    )


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.version.alter(type=String(10))
    Table("rules_history", metadata, autoload=True).c.version.alter(type=String(10))
    Table("rules_scheduled_changes", metadata, autoload=True).c.base_version.alter(type=String(10))
    Table("rules_scheduled_changes_history", metadata, autoload=True).c.base_version.alter(
        type=String(10)
    )
