"""Alembic environment configuration.

Supports both programmatic use (engine passed via config.attributes["connection"])
and CLI use (for developers running `alembic revision --autogenerate`).
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    # disable_existing_loggers=False is required to preserve loggers set up before
    # migrations run
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# Get target_metadata from config attributes (set programmatically)
# or create an AUSDatabase instance for CLI/autogenerate use
target_metadata = config.attributes.get("target_metadata")
if target_metadata is None:
    # CLI mode - create a database instance to get metadata
    from auslib.db import AUSDatabase

    db = AUSDatabase()
    # Get database URI from alembic.ini or environment
    db_uri = config.get_main_option("sqlalchemy.url")
    if db_uri:
        db.setDburi(db_uri)
        target_metadata = db.metadata
    else:
        raise ValueError(
            "No target_metadata in config.attributes and no sqlalchemy.url in config. "
            "Either pass metadata programmatically or set sqlalchemy.url in alembic.ini"
        )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Check if a connection was passed programmatically
    connectable = config.attributes.get("connection")

    if connectable is None:
        # CLI mode - create engine from config
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
