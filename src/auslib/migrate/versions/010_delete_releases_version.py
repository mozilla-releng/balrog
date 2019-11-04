from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("releases", metadata, autoload=True).c.version.drop()
    Table("releases_history", metadata, autoload=True).c.version.drop()


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    version = Column("version", String(25), unique=True)
    version.create(Table("releases", metadata, autoload=True), unique_name="version_unique")

    history_version = Column("version", String(25))
    history_version.create(Table("releases_history", metadata, autoload=True))
