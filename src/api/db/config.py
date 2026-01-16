from decouple import config as decouple_config
from dotenv import load_dotenv
import os

# Load .env file before reading config
load_dotenv()

DATABASE_URL = decouple_config("DATABASE_URL", '')
DB_TIMEZONE = decouple_config("DB_TIMEZONE", 'utc')