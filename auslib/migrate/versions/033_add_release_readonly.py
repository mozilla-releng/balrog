from sqlalchemy import Table, Column, Integer, BigInteger, String, Boolean, MetaData


metadata = MetaData()


releases_readonly = Table(
    "releases_readonly", metadata, Column("release_name", String(100), nullable=False, primary_key=True), Column("data_version", Integer, nullable=False)
)


releases_readonly_history = Table(
    "releases_readonly_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("release_name", String(100), nullable=False),
    Column("changed_by", String(100), nullable=False),
    Column("data_version", Integer),
)


releases_readonly_scheduled_changes = Table(
    "releases_readonly_scheduled_changes",
    metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=True),
    Column("scheduled_by", String(100), nullable=False),
    Column("complete", Boolean, default=False),
    Column("change_type", String(50), nullable=False),
    Column("data_version", Integer, nullable=False),
    Column("base_release_name", String(100), nullable=False),
    Column("base_data_version", Integer),
)


releases_readonly_scheduled_changes_history = Table(
    "releases_readonly_scheduled_changes_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False),
    Column("scheduled_by", String(100)),
    Column("complete", Boolean, default=False),
    Column("change_type", String(50)),
    Column("data_version", Integer),
    Column("base_release_name", String(100)),
    Column("base_data_version", Integer),
)


releases_readonly_scheduled_changes_conditions = Table(
    "releases_readonly_scheduled_changes_conditions",
    metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=True),
    Column("data_version", Integer, nullable=False),
)


releases_readonly_scheduled_changes_conditions_history = Table(
    "releases_readonly_scheduled_changes_conditions_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False),
    Column("data_version", Integer),
)


releases_readonly_scheduled_changes_signoffs = Table(
    "releases_readonly_scheduled_changes_signoffs",
    metadata,
    Column("sc_id", Integer, primary_key=True, autoincrement=False),
    Column("username", String(100), primary_key=True),
    Column("role", String(50), nullable=False),
)


releases_readonly_scheduled_changes_signoffs_history = Table(
    "releases_readonly_scheduled_changes_signoffs_history",
    metadata,
    Column("change_id", Integer, primary_key=True, autoincrement=True),
    Column("changed_by", String(100), nullable=False),
    Column("sc_id", Integer, nullable=False),
    Column("username", String(100), nullable=False),
    Column("role", String(50)),
)


def upgrade_data(migrate_engine):
    insert_query = """
        INSERT INTO releases_readonly(release_name, data_version)
        SELECT name, data_version FROM releases WHERE read_only = 1;
    """
    migrate_engine.execute(insert_query)

    insert_history_query = """
        INSERT INTO releases_readonly_history(release_name, data_version, changed_by, `timestamp`)
        SELECT name, data_version, changed_by, `timestamp`
        FROM releases_history where read_only = 1;
    """
    migrate_engine.execute(insert_history_query)


def drop_releases_readonly_columns_sqlite(metadata):
    tables = ["releases", "releases_history", "releases_scheduled_changes", "releases_scheduled_changes_history"]

    new_tables = []

    for table in tables:
        db_table = Table(table, metadata, autoload=True)
        new_columns = []
        for column in db_table.c:
            if column.name not in ["read_only", "base_read_only"]:
                new_columns.append(column.copy())
        db_table.drop()
        metadata.remove(db_table)
        new_tables.append(Table(table, metadata, *new_columns))

    metadata.create_all(tables=new_tables)


def drop_releases_readonly_columns(metadata):
    releases = Table("releases", metadata, autoload=True)
    releases.c.read_only.drop()

    releases_history = Table("releases_history", metadata, autoload=True)
    releases_history.c.read_only.drop()

    releases_scheduled_changes = Table("releases_scheduled_changes", metadata, autoload=True)
    releases_scheduled_changes.c.base_read_only.drop()

    releases_scheduled_changes_history = Table("releases_scheduled_changes_history", metadata, autoload=True)
    releases_scheduled_changes_history.c.base_read_only.drop()


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    bigintType = BigInteger

    if migrate_engine.name == "sqlite":
        bigintType = Integer

    releases_readonly_history.append_column(Column("timestamp", bigintType, nullable=False))

    releases_readonly_scheduled_changes_history.append_column(Column("timestamp", bigintType, nullable=False))

    releases_readonly_scheduled_changes_conditions.append_column(Column("when", bigintType))

    releases_readonly_scheduled_changes_conditions_history.append_column(Column("when", bigintType))
    releases_readonly_scheduled_changes_conditions_history.append_column(Column("timestamp", bigintType, nullable=False))

    releases_readonly_scheduled_changes_signoffs_history.append_column(Column("timestamp", bigintType, nullable=False))

    metadata.create_all()
    upgrade_data(migrate_engine)

    if migrate_engine.name == "sqlite":
        drop_releases_readonly_columns_sqlite(metadata)
    else:
        drop_releases_readonly_columns(metadata)


def create_releases_readonly_columns(metadata):
    releases = Table("releases", metadata, autoload=True)
    read_only_column = Column("read_only", Boolean)
    read_only_column.create(releases, default=False)

    releases_history = Table("releases_history", metadata, autoload=True)
    read_only_column_history = Column("read_only", Boolean)
    read_only_column_history.create(releases_history, default=False)

    releases_scheduled_changes = Table("releases_scheduled_changes", metadata, autoload=True)
    read_only_column_scheduled_changes = Column("read_only", Boolean)
    read_only_column_scheduled_changes.create(releases_scheduled_changes, default=False)

    releases_scheduled_changes_history = Table("releases_scheduled_changes_history", metadata, autoload=True)
    read_only_column_scheduled_changes_history = Column("read_only", Boolean)
    read_only_column_scheduled_changes_history.create(releases_scheduled_changes_history, default=False)


def downgrade_data(migrate_engine):
    update_query = """
        UPDATE releases as R
        INNER JOIN releases_readonly AS RR
        ON R.name = RR.release_name
        SET R.read_only = 1
    """
    migrate_engine.execute(update_query)

    update_history_query = """
        UPDATE releases_history as R
        INNER JOIN releases_readonly_history AS RR
        ON R.name = RR.release_name
        SET R.read_only = 1
        where R.data_version = RR.data_version
    """
    migrate_engine.execute(update_history_query)


def downgrade(migrate_engine):
    metadata.bind = migrate_engine

    create_releases_readonly_columns(metadata)

    if migrate_engine.name != "sqlite":
        downgrade_data(migrate_engine)

    Table("releases_readonly", metadata, autoload=True).drop()
    Table("releases_readonly_history", metadata, autoload=True).drop()
    Table("releases_readonly_scheduled_changes", metadata, autoload=True).drop()
    Table("releases_readonly_scheduled_changes_history", metadata, autoload=True).drop()
    Table("releases_readonly_scheduled_changes_conditions", metadata, autoload=True).drop()
    Table("releases_readonly_scheduled_changes_conditions_history", metadata, autoload=True).drop()
    Table("releases_readonly_scheduled_changes_signoffs", metadata, autoload=True).drop()
    Table("releases_readonly_scheduled_changes_signoffs_history", metadata, autoload=True).drop()
