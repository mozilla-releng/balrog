from sqlalchemy import MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    string_column = String(2000)
    Table('rules', metadata, autoload=True).c.distribution.alter(type=string_column)
    Table('rules_history', metadata, autoload=True).c.distribution.alter(type=string_column)
    Table('rules_scheduled_changes', metadata, autoload=True).c.base_distribution.alter(type=string_column)
    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_distribution.alter(type=string_column)


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    string_column = String(100)
    Table('rules', metadata, autoload=True).c.distribution.alter(type=string_column)
    Table('rules_history', metadata, autoload=True).c.distribution.alter(type=string_column)
    Table('rules_scheduled_changes', metadata, autoload=True).c.base_distribution.alter(type=string_column)
    Table('rules_scheduled_changes_history', metadata, autoload=True).c.base_distribution.alter(type=string_column)
