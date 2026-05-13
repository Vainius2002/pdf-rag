from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)  
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

#engine = the central connection object. Knows how to reach Postgres. Created once, reused for every query.
#echo = True prints every SQL statement to your console.
#SessionLocal = a factory for creating "sessions." A session is a temporary workspace for queries. We use this constantly.
#Base = every database model class will inherit from this. SQLAlchemy uses it to know "this Python class represents a table."