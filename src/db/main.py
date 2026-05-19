"""
Database initialization module.

This module creates an asynchronous SQLModel/SQLAlchemy engine
and provides a helper to initialize a connection and execute
a simple test statement.
"""

# Import create_engine to build a synchronous SQLAlchemy engine
# and text for creating textual SQL statements.
from sqlmodel import SQLModel

# Import AsyncEngine type for wrapping the created engine to async usage.
from sqlalchemy.ext.asyncio import async_session, create_async_engine

# Import configuration values (DATABASE_URL) from project config.
from src.config import Config



from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


# Build an AsyncEngine by first creating a standard engine with SQLModel's
# create_engine using the configured DATABASE_URL. echo=True enables SQL statement logging for debugging. Wrapping with AsyncEngine exposes an async API.
# logging for debugging. Wrapping with AsyncEngine exposes an async API.
engine =create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)





async def initdb():
    """create our database models in the database"""
    # Begin an asynchronous transaction/context-managed connection.
    async with engine.begin() as conn:
        # Create a textual SQL statement to test the connection.
        # statement = text("select 'Hello World'")

        # Execute the statement asynchronously and await the Result.
        # result = await conn.execute(statement)
        
       await conn.run_sync(SQLModel.metadata.create_all)

       print("Database initialized successfully.")

        # Print the Result object (not the rows) for debugging purposes.
        # print(result)


... # rest of main.py

async def get_session() -> AsyncSession:
    """Dependency to provide the session object"""
    async_session = sessionmaker(
    bind= engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session