from sqlalchemy import Table, Column, Integer, MetaData


DOCKERFLOW_TABLE_NAME = 'dockerflow'

metadata = MetaData()

dockerflow = Table(DOCKERFLOW_TABLE_NAME, metadata,
                   Column('watchdog', Integer, nullable=False),
                   Column('data_version', Integer, nullable=False)
                   )


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.create_all()


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.create_all()
