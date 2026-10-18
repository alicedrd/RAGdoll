from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from ragdoll.models.registry.docrecord import AppDeclarativeBase

def get_sessionmaker(db_url: str):
    engine = create_engine(db_url)
    # conditional, will not overwrite if tables already exist
    AppDeclarativeBase.metadata.create_all(engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)