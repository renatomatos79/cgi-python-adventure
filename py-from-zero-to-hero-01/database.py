from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite Database
DATABASE_URL = "sqlite:///users_groups.db"

# Factory function to create a Database connection
# When echo=True is set, SQLAlchemy prints all SQL statements executed under the hood.
engine = create_engine(DATABASE_URL, echo=False)

# Creates a Session Factory
SessionLocal = sessionmaker(bind=engine)
