from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    def add_comment(table):
        comment = Column('comment', String(500))
        comment.create(table)
    add_comment(Table('rules', metadata, autoload=True))
    add_comment(Table('rules_history', metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('rules', metadata, autoload=True).c.comment.drop()
    Table('rules_history', metadata, autoload=True).c.comment.drop()
