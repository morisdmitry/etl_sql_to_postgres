import sqlite3
import psycopg2
import logging


from config import Config
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from utils import SQLiteLoader, PostgresSaver

load_dotenv()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    cursor = connection.cursor()
    pg_cursor = pg_conn.cursor()

    sqlite_loader = SQLiteLoader(cursor, connection)
    data_names_of_tables = sqlite_loader.load_tables_names()
    data_file_paths = []
    try:
        for name_of_table in data_names_of_tables:

            data_table_info = sqlite_loader.load_table_columns_info(name_of_table)

            (
                attrs,
                unconflict_attrs,
            ) = sqlite_loader.forming_attrs_and_attrs_for_unconflict(
                name_of_table, data_table_info
            )

            sqlite_loader.load_data(name_of_table, attrs, 10, data_file_paths)

            cols_slots = sqlite_loader.create_cols_slots(name_of_table)

            save_to_postgres = PostgresSaver(pg_cursor)
            save_to_postgres.save_all_data(
                name_of_table, cols_slots, attrs, unconflict_attrs, sqlite_loader
            )
            print("done!")
    except Exception as e:
        logging.exception()
    finally:
        connection.commit()
        connection.close()


if __name__ == "__main__":

    dsl = {
        "dbname": Config.DB_NAME,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
    }
    print("dsl", dsl)
    with sqlite3.connect("./db.sqlite") as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
