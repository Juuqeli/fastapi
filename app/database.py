from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_pwd}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Connecting to database with psycopg2
# try:
#     conn = psycopg2.connect(host = '', database = '', user = '', password = '', cursor_factory = RealDictCursor)
#     cursor = conn.cursor()
#     print('Database connection succesful')
# except Exception as e:
#     print(f'connection failed: {e}')

