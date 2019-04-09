from sqlalchemy import Index, MetaData, Table

# Because releases get modified so often, and are so big -
# their history table ends huge and slow. An index helps negate
# the bad effects of this.


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    t = Table("releases_history", metadata, autoload=True)
    Index("timestamp", t.c.timestamp).create()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    t = Table("releases_history", metadata, autoload=True)
    Index("timestamp", t.c.timestamp).drop()
