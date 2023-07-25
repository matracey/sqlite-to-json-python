import json
import sqlite3
from typing import Any, Dict, List, Tuple


def dict_factory(cursor: sqlite3.Cursor, row: Tuple) -> Dict[str, Any]:
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


# connect to the SQlite databases
def open_connection(db_path: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(db_path)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    return connection, cursor


def get_all_records_in_table(table_name: str, db_path: str) -> str:
    conn, curs = open_connection(db_path)
    conn.row_factory = dict_factory
    curs.execute(f"SELECT * FROM '{table_name}' ")
    # fetchall as result
    results = curs.fetchall()
    # close connection
    conn.close()
    return json.dumps(results)


def sqlite_to_json(db_path: str) -> None:
    connection, cursor = open_connection(db_path)
    # select all the tables from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables: List[Dict[str, str]] = cursor.fetchall()
    # for each of the tables , select all the records from the table
    for table_name in tables:
        # Get the records in table
        results = get_all_records_in_table(table_name["name"], db_path)

        # generate and save JSON files with the table name for each of the
        # database tables and save in results folder
        with open(
            f"./results/{table_name['name']}.json", "w", encoding="utf-8"
        ) as the_file:
            the_file.write(results)
    # close connection
    connection.close()


if __name__ == "__main__":
    # modify path to SQLite DB
    PATH_TO_SQLITE_DB = "path/to/db.sqlite3"
    sqlite_to_json(PATH_TO_SQLITE_DB)
