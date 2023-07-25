# SQLite to JSON Converter

This Python script provides functionality to convert all tables in an SQLite database to JSON files and save them in a 'results' folder in the current directory.

## Requirements

- Python 3.x
- SQLite3

## Usage

1. Place the `main.py` script in the same directory as the SQLite database you want to convert.
2. Open a terminal or command prompt and navigate to the directory containing the script and database.
3. Run the script with the following command: `python main.py <database_name>.{sqlite,sqlite3,db,db3,s3db,sl3}`
4. The script will create a 'results' folder in the current directory and save a JSON file for each table in the database.

## Contributing

Contributions are welcome! Please submit a pull request with any bug fixes or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
