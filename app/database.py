from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:321456@localhost/My FASTAPI DATABSE local"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

############DB CONNECTION####################
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost',
#                             database='My FASTAPI DATABSE local',
#                             user='postgres',
#                             password='321456',
#                             cursor_factory=RealDictCursor)

#         cursor = conn.cursor()
#         print("Database connection was succesfull!!")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("error", error)
#         time.sleep(2)