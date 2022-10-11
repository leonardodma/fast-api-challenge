import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from propreties import SQLITE_DATA_PATH
from app.database.models import ItemDB, OrderDB, PurchaseDB, Base

engine = create_engine(f'sqlite:///{SQLITE_DATA_PATH}', echo=True)
Session = sessionmaker(bind=engine)
db = Session()

# Create the database if it doesn't exist
if not os.path.isfile(SQLITE_DATA_PATH):
    Base.metadata.create_all(engine)