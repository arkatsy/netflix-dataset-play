import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import typing
import csv
import csv_fix


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

drop_netflix_titles_table = """
    DROP TABLE IF EXISTS netflix_titles;
"""

netflix_titles_table = """
    CREATE TABLE netflix_titles (
        show_id VARCHAR(255) PRIMARY KEY,
        type VARCHAR(255),
        title VARCHAR(255),
        director VARCHAR(255),
        show_cast TEXT,
        country VARCHAR(255),
        date_added DATE,
        release_year INT,
        rating VARCHAR(255),
        duration VARCHAR(255),
        listed_in VARCHAR(255),
        description TEXT
    );
"""

with psycopg2.connect(
    dbname=config["user"],
    user=config["user"],
    password=config["password"],
    host=config["host"],
    port=config["port"],
) as conn:
    with conn.cursor() as curs:
        # Modify the csv file
        csv_encoding = "latin1"
        new_csv_path = "./netflix_titles_fixed.csv"
        csv_fix.rename_cast_to_show_cast(
            write_to_file_path=new_csv_path, encoding=csv_encoding
        )

        # Reset the netflix_titles table
        curs.execute(drop_netflix_titles_table)
        curs.execute(netflix_titles_table)

        with open(new_csv_path, "r", encoding=csv_encoding) as file:
            reader = csv.reader(file)
            header = list(filter(None, next(reader)))

            for row in reader:

                # Truncate row to the length of the header
                row = row[: len(header)]

                row = [None if cell == "" else cell for cell in row]

                insert_data_query = sql.SQL(
                    "INSERT INTO {table} ({cols}) VALUES ({records})"
                ).format(
                    table=sql.Identifier("netflix_titles"),
                    cols=sql.SQL(", ").join(map(sql.Identifier, header)),
                    records=sql.SQL(", ").join(map(sql.Literal, row)),
                )

                curs.execute(insert_data_query)
