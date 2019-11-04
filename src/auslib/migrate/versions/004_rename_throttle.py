from sqlalchemy import MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.throttle.alter(name="backgroundRate")
    Table("rules_history", metadata, autoload=True).c.throttle.alter(name="backgroundRate")


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("rules", metadata, autoload=True).c.backgroundRate.alter(name="throttle")
    Table("rules_history", metadata, autoload=True).c.backgroundRate.alter(name="throttle")
