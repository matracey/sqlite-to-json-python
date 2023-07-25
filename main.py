"""
This module provides functionality to convert all tables in an SQLite database
to JSON files and save them in a 'results' folder in the current directory.
"""

import argparse
import json
import os
import sqlite3
from typing import Any, Dict, List, Tuple


def dict_factory(cursor: sqlite3.Cursor, row: Tuple) -> Dict[str, Any]:
    """
    Converts a row from an SQLite query result into a dictionary.

    :param cursor: The cursor object used to execute the query.
    :param row: A row from the query result.
    :return: A dictionary representing the row.
    """
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


# connect to the SQlite databases
def open_connection(db_path: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Opens a connection to the SQLite database and returns a tuple containing
    the connection and cursor objects.

    :param db_path: The path to the SQLite database.
    :return: A tuple containing the connection and cursor objects.
    """
    connection = sqlite3.connect(db_path)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    return connection, cursor


def get_all_records_in_table(table_name: str, db_path: str) -> str:
    """
    Retrieves all records from a specified table in an SQLite database and
    returns them as a JSON string.

    :param table_name: The name of the table to retrieve records from.
    :param db_path: The path to the SQLite database.
    :return: A JSON string containing all records from the specified table.
    """
    conn, curs = open_connection(db_path)
    conn.row_factory = dict_factory
    curs.execute(f"SELECT * FROM '{table_name}' ")
    # fetchall as result
    results = curs.fetchall()
    # close connection
    conn.close()
    return json.dumps(results)


def sqlite_to_json(db_path: str, output_path: str) -> None:
    """
    Converts all tables in an SQLite database to JSON files and saves them in a
    'results' folder in the current directory.

    :param db_path: The path to the SQLite database.
    :param output_path: The path to the output folder where JSON files will be
        saved.
    :return: None
    """
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
            os.path.join(output_path, f"{table_name['name']}.json"),
            "w",
            encoding="utf-8",
        ) as the_file:
            the_file.write(results)
    # close connection
    connection.close()


def main():
    """
    The main function of the module. It parses command line arguments,
    validates them, and calls the `sqlite_to_json` function to convert
    all tables in a SQLite database to JSON files and save them in a
    'results' folder in the current directory.

    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "db_path",
        help="Path to SQLite database that will be converted to JSON files",
        type=str,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to output folder where JSON files will be saved",
        type=str,
        default=os.path.join(os.getcwd(), "results"),
    )

    args = parser.parse_args()
    db_path = os.path.abspath(args.db_path)
    output_path = os.path.abspath(args.output)

    sqlite_exts = [".sqlite", ".sqlite3", ".db", ".db3", ".s3db", ".sl3"]

    db_is_file = os.path.isfile(db_path)
    db_ext_is_sqlite = db_path.endswith(tuple(sqlite_exts))

    if not db_is_file or not db_ext_is_sqlite:
        raise ValueError("db_path must be a valid SQLite database")

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    output_is_dir = os.path.isdir(output_path)
    output_writeable = os.access(output_path, os.W_OK)

    if not output_is_dir or not output_writeable:
        raise ValueError("output must be a valid directory that is writable")

    sqlite_to_json(db_path, output_path)


if __name__ == "__main__":
    main()
