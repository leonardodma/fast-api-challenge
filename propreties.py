from dotenv import load_dotenv
import os

load_dotenv()
SQLITE_DATA_PATH = os.getenv("SQLITE_DATA_PATH")