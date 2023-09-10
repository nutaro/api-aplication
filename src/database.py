import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

drive = os.getenv("db_drive")
user = os.getenv("db_user")
password = quote_plus(os.getenv("db_password"))
host = os.getenv("POSTGRES_SERVICE_HOST")
port = os.getenv("POSTGRES_SERVICE_PORT")
name = os.getenv("db_name")

def get_session() -> Session:

    url = f'{drive}://{user}:{password}@{host}:{port}/{name}'
    engine = create_engine(url)
    session = sessionmaker(engine)
    return session()
