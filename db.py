import os
from dotenv import load_dotenv
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    retries = 5
    print("Starting...")
    while retries:
        try:
            print("Before engine connect...")
            with engine.connect() as connection:
                print(f"{connection} to the database is successful!")
            Base.metadata.create_all(bind=engine)
            print("Database initialized with tables!")
            return
        except OperationalError as e:
            print(f"Database connection failed: {e}. Retrying in 5 seconds...")
            retries -= 1
            sleep(5)
        except Exception as e:
            print(f"Unexpected error initializing the database: {e}")
            return

