import os
from dotenv import load_dotenv
import psycopg2
import typing


class EnvConfig(typing.TypedDict):
    host: str
    port: str
    password: str
    user: str


load_dotenv()


def validate_env() -> EnvConfig:
    HOST = os.getenv("POSTGRES_HOST")
    PORT = os.getenv("POSTGRES_PORT")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    USER = os.getenv("POSTGRES_USER")

    if not HOST:
        raise ValueError("Missing POSTGRES_HOST environment variable")
    if not PORT:
        raise ValueError("Missing POSTGRES_PORT environment variable")
    if not PASSWORD:
        raise ValueError("Missing POSTGRES_PASSWORD environment variable")
    if not USER:
        raise ValueError("Missing POSTGRES_USER environment variable")

    return {"host": HOST, "port": PORT, "password": PASSWORD, "user": USER}


config = validate_env()

conn = psycopg2.connect(
    dbname=config["user"],
    user=config["user"],
    password=config["password"],
    host=config["host"],
    port=config["port"],
)


if conn:
    print("Connection opened successfully")
else:
    print("Failed to open connection")


conn.close()
