from sqlalchemy import (BigInteger, Column, Integer, MetaData, String, Table,
                        Text)

metadata = MetaData()

rules = Table('rules', metadata,
              Column('rule_id', Integer, primary_key=True, autoincrement=True),
              Column('priority', Integer),
              Column('mapping', String(100)),
              Column('throttle', Integer),
              Column('update_type', String(15), nullable=False),
              Column('product', String(15)),
              Column('version', String(10)),
              Column('channel', String(75)),
              Column('buildTarget', String(75)),
              Column('buildID', String(20)),
              Column('locale', String(10)),
              Column('osVersion', String(100)),
              Column('distribution', String(100)),
              Column('distVersion', String(100)),
              Column('headerArchitecture', String(10)),
              Column('data_version', Integer, nullable=False)
              )

rules_history = Table('rules_history', metadata,
                      Column('change_id', Integer, primary_key=True, autoincrement=True),
                      Column('changed_by', String(100), nullable=False),
                      Column('rule_id', Integer, nullable=False),
                      Column('priority', Integer),
                      Column('mapping', String(100)),
                      Column('throttle', Integer),
                      Column('update_type', String(15)),
                      Column('product', String(15)),
                      Column('version', String(10)),
                      Column('channel', String(75)),
                      Column('buildTarget', String(75)),
                      Column('buildID', String(20)),
                      Column('locale', String(10)),
                      Column('osVersion', String(100)),
                      Column('distribution', String(100)),
                      Column('distVersion', String(100)),
                      Column('headerArchitecture', String(10)),
                      Column('data_version', Integer)
                      )

releases = Table('releases', metadata,
                 Column('name', String(100), primary_key=True),
                 Column('product', String(15), nullable=False),
                 Column('version', String(25), nullable=False),
                 Column('data_version', Integer, nullable=False)
                 )

releases_history = Table('releases_history', metadata,
                         Column('change_id', Integer, primary_key=True, autoincrement=True),
                         Column('changed_by', String(100), nullable=False),
                         Column('name', String(100), nullable=False),
                         Column('product', String(15)),
                         Column('version', String(25)),
                         Column('data_version', Integer)
                         )

permissions = Table('permissions', metadata,
                    Column('permission', String(50), primary_key=True),
                    Column('username', String(100), primary_key=True),
                    Column('options', Text),
                    Column('data_version', Integer, nullable=False)
                    )
permissions_history = Table('permissions_history', metadata,
                            Column('change_id', Integer, primary_key=True, autoincrement=True),
                            Column('changed_by', String(100), nullable=False),
                            Column('permission', String(50), nullable=False),
                            Column('username', String(100), nullable=False),
                            Column('options', Text),
                            Column('data_version', Integer)
                            )


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    if migrate_engine.name == 'mysql':
        from sqlalchemy.dialects.mysql import LONGTEXT
        textType = LONGTEXT
        bigintType = BigInteger
    elif migrate_engine.name == 'sqlite':
        textType = Text
        bigintType = Integer
    else:
        textType = Text
    releases.append_column(Column('data', textType, nullable=False))
    releases_history.append_column(Column('data', textType))
    rules_history.append_column(Column('timestamp', bigintType, nullable=False))
    releases_history.append_column(Column('timestamp', bigintType, nullable=False))
    permissions_history.append_column(Column('timestamp', bigintType, nullable=False))
    metadata.create_all()
