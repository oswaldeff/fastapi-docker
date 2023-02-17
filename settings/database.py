
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class SQLAlchemy:
    def __init__(self) -> None:
        self.engine = create_engine(
            os.environ["SQLALCHEMY_DATABASE_URL"],
            echo=True, # SQL log
            pool_size=5, # connection size of QueuePool
            max_overflow=10, # connection limit size of QueuePool, ( connection limit size = pool_size + max_overflow)
            pool_recycle=900, # for lost connection, must be less than wait_timeout(default 30sec)
            pool_pre_ping=True # for disconnect handling
        )
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()

async def session():
    
    try:
        db = SQLAlchemy()
        db_session = db.session
        yield db_session

    except Exception as e:
        db_session.rollback()
    
    finally:
        db_session.close()
