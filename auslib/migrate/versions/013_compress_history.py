

def upgrade(migrate_engine):
    con = migrate_engine.connect()
    if migrate_engine.name == 'mysql':
        con.execute('ALTER TABLE releases_history ROW_FORMAT=COMPRESSED')


def downgrade(migrate_engine):
    con = migrate_engine.connect()
    if migrate_engine.name == 'mysql':
        con.execute('ALTER TABLE releases_history ROW_FORMAT=DEFAULT')
