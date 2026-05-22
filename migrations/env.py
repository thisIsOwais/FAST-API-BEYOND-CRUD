# Import necessary modules for async operations and logging
import asyncio
from logging.config import fileConfig

# Import SQLAlchemy components for database operations
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import Alembic context and configuration
from alembic import context
from src.auth.schema import User
from src.books.schema import Book
from src.reviews.schema import Review
from sqlmodel import SQLModel
from src.config import Config

# Get database URL from configuration
database_url = Config.DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the database URL in the Alembic configuration
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Function to run migrations in offline mode
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Get the database URL from config
    url = config.get_main_option("sqlalchemy.url")
    # Configure the migration context with the URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Begin transaction and run migrations
    with context.begin_transaction():
        context.run_migrations()

# Helper function to execute migrations with a connection
def do_run_migrations(connection: Connection) -> None:
    # Configure context with the connection and target metadata
    context.configure(connection=connection, target_metadata=target_metadata)

    # Begin transaction and run migrations
    with context.begin_transaction():
        context.run_migrations()

# Async function to run migrations with async engine
async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # Create async engine from configuration
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Connect to database and run migrations synchronously
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Dispose of the engine
    await connectable.dispose()

# Function to run migrations in online mode
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    # Run async migrations
    asyncio.run(run_async_migrations())

# Check if running in offline or online mode and execute accordingly
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
