from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from fastapi import Depends #type: ignore
from typing import Annotated
from sqlalchemy.orm import Session
# import database.model as model
from utils.config import DataBase_config as dbconfig


if not dbconfig.cloud_db:
    raise ValueError("Database URL (cloud_db) is not configured")

engine = create_engine(
    dbconfig.cloud_db,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionlocal()

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()   

db_dependency = Annotated[Session, Depends(get_db)]
