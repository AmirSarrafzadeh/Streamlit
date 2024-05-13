"""
This script creates a database and tables in SQL Server.

Author: Your full name
Date: 2024-05-13

Preconditions:
1. SQL Server is installed.
2. SQL Server Management Studio (SSMS) is installed.
3. You have the necessary permissions to create a database and tables.
4. Create a new database in SSMS called 'supermarket'.
5. The necessary python libraries are installed. You can use requirements.txt to install them.
"""


# SQL Server Management Studio (SSMS) -> Connect to the server -> Databases -> Create new database -> supermarket
import os
import sys
import pyodbc
import logging
import configparser
import warnings

warnings.filterwarnings('ignore')


def create_tables(server_name, database_name):
    conn_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name}'
    # Establishing the connection
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()

    commands = [
        '''CREATE TABLE producers (
            id VARCHAR(50) PRIMARY KEY NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            phone VARCHAR(50) NOT NULL
        );''',
        '''CREATE TABLE products (
            id VARCHAR(50) PRIMARY KEY NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            product_price FLOAT NOT NULL,
            producer_id VARCHAR(50) NOT NULL,
            product_category VARCHAR(255) NOT NULL,
            FOREIGN KEY (producer_id) REFERENCES producers(id)
        );''',
        '''CREATE TABLE warehouse (
            product_id VARCHAR(50) PRIMARY KEY NOT NULL,
            product_amount VARCHAR(50) NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );''',
        '''CREATE TABLE customers (
            id VARCHAR(50) PRIMARY KEY NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            address VARCHAR(255) NOT NULL
        );''',
        '''CREATE TABLE sell (
            id VARCHAR(50) PRIMARY KEY NOT NULL,
            customer_id VARCHAR(50) NOT NULL,
            product_id VARCHAR(50) NOT NULL,
            quantity INTEGER NOT NULL,
            paid VARCHAR(50) NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );''',
        '''CREATE TABLE buy (
            id VARCHAR(50) PRIMARY KEY NOT NULL,
            producer_id VARCHAR(50) NOT NULL,
            product_id VARCHAR(50) NOT NULL,
            quantity INTEGER NOT NULL,
            paid VARCHAR(50) NOT NULL,
            FOREIGN KEY (producer_id) REFERENCES producers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );''',
        '''CREATE TABLE staff (
            id VARCHAR(50) PRIMARY KEY NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            position VARCHAR(255) NOT NULL
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
        database_name = config['config']['database_name']
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
