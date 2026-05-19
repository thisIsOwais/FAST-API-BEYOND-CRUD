"""
Database initialization module.

This module creates an asynchronous SQLModel/SQLAlchemy engine
and provides a helper to initialize a connection and execute
a simple test statement.
"""

# Import create_engine to build a synchronous SQLAlchemy engine
# and text for creating textual SQL statements.
from sqlmodel import create_engine, text
# Import AsyncEngine type for wrapping the created engine to async usage.
from sqlalchemy.ext.asyncio import AsyncEngine
# Import configuration values (DATABASE_URL) from project config.
from src.config import Config


# Build an AsyncEngine by first creating a standard engine with SQLModel's
# create_engine using the configured DATABASE_URL. echo=True enables SQL statement logging for debugging. Wrapping with AsyncEngine exposes an async API.
# logging for debugging. Wrapping with AsyncEngine exposes an async API.
engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def initdb():
    """Initialize the database connection and execute a test statement.

    This coroutine opens an asynchronous connection via engine.begin(),
    constructs a simple SQL text statement (select 'Hello World'), executes
    it using the async connection, and prints the raw Result object.
    """

    # Begin an asynchronous transaction/context-managed connection.
    async with engine.begin() as conn:
        # Create a textual SQL statement to test the connection.
        statement = text("select 'Hello World'")

        # Execute the statement asynchronously and await the Result.
        result = await conn.execute(statement)

        # Print the Result object (not the rows) for debugging purposes.
        print(result)