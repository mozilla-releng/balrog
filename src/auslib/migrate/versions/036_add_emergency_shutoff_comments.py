from sqlalchemy import Column, MetaData, String, Table


def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)

    comment = Column("comment", String(500), nullable=True)
    comment.create(Table("emergency_shutoffs", metadata, autoload=True))

    history_comment = Column("comment", String(500), nullable=True)
    history_comment.create(Table("emergency_shutoffs_history", metadata, autoload=True))

    base_comment = Column("base_comment", String(500), nullable=True)
    base_comment.create(Table("emergency_shutoffs_scheduled_changes", metadata, autoload=True))

    history_base_comment = Column("base_comment", String(500), nullable=True)
    history_base_comment.create(Table("emergency_shutoffs_scheduled_changes_history", metadata, autoload=True))


def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table("emergency_shutoffs", metadata, autoload=True).c.comment.drop()
    Table("emergency_shutoffs_history", metadata, autoload=True).c.comment.drop()
    Table("emergency_shutoffs_scheduled_changes", metadata, autoload=True).c.base_comment.drop()
    Table("emergency_shutoffs_scheduled_changes_history", metadata, autoload=True).c.base_comment.drop()
