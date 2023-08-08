from dotenv import load_dotenv
from os import environ
load_dotenv()
from mysql import connector

def get_connection():
    return connector.connect(
        host=environ.get("DB_HOST"),
        user=environ.get("DB_USER"),
        password=environ.get("DB_PASS"),
        database=environ.get("DB_NAME"),
        port=environ.get("DB_PORT") if environ.get("DB_PORT") else 3306
    )