from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from propreties import SQLITE_DATA_PATH

engine = create_engine(f'sqlite:///{SQLITE_DATA_PATH}', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)