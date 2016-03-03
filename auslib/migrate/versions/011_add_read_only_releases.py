from sqlalchemy import Column, Boolean, MetaData, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    releases = Table('releases', metadata, autoload=True)
    releases_history = Table('releases_history', metadata, autoload=True)

    read_only = Column('read_only', Boolean)
    read_only.create(releases)

    history_read_only = Column('read_only', Boolean)
    history_read_only.create(releases_history)


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    releases = Table('releases', metadata, autoload=True)
    releases_history = Table('releases', metadata, autoload=True)

    releases.c.read_only.drop()
    releases_history.c.read_only.drop()
