import os
import sys
import pyodbc
import logging
import configparser
import warnings

warnings.filterwarnings('ignore')


def create_tables(server_name, database_name):
    conn_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;'
    # Establishing the connection
    try:
        conn = pyodbc.connect(conn_string)
    except pyodbc.Error as e:
        logging.error(f"Error connecting to SQL Server: {e}")
        raise e

    cursor = conn.cursor()

    commands = [
        '''CREATE TABLE actions (
            id VARCHAR(50) NOT NULL,
            action VARCHAR(255) NOT NULL,
            timestamp DATETIME NOT NULL
        );'''
    ]

    # Execute each command to create the tables
    for command in commands:
        cursor.execute(command)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # Check if the folder exists
    if not os.path.exists("logs"):
        # Create the folder
        os.makedirs("logs")
    else:
        pass
    # Call the function to create the database and tables
    logging.basicConfig(filename="./logs/db.log",
                        level=logging.INFO,
                        format='%(levelname)s   %(asctime)s   %(message)s')
    try:
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(config_path)
        driver_name = config['config']['driver_name']
        server_name = config['config']['server_name']
        database_name = config['config']['database_name2']
        logging.info("Config file read successfully")
    except Exception as e:
        logging.error("Error reading config file: " + str(e))
        sys.exit()

    try:
        create_tables(server_name, database_name)
        logging.info("Tables created successfully")
    except Exception as e:
        logging.error("Error creating tables: " + str(e))
        sys.exit()
