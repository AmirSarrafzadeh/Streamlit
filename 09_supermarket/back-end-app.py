"""
The back-end-app.py file is the FastAPI application that will be used to interact with the database.
The application will have several endpoints to insert records into the database tables. The application will also serve an image in full-screen mode when the root URL is accessed.

Author: Your full name
Date: 2024-05-13

Preconditions:
1. FastAPI is installed.
2. The necessary python libraries are installed. You can use requirements.txt to install them.

Procedure:
1. Import the necessary libraries.
2. Read the configuration file to get the database connection details.
3. Create a FastAPI application.
4. Define the data models for the warehouse record, product, producer, customer, staff, buy record, and sell record.
5. Define the endpoint to serve an image in full-screen mode.
6. Define the endpoint to get the image.
7. Define the endpoint to insert a warehouse record.
8. Define the endpoint to insert a product.
9. Define the endpoint to insert a producer.
10. Define the endpoint to insert a customer.
11. Define the endpoint to insert a staff member.
12. Define the endpoint to insert a buy record.
13. Define the endpoint to insert a sell record.
14. Run the FastAPI application.
"""

# Import necessary libraries
import io
import os
import sys
import pyodbc
import logging
import uvicorn
import configparser
from pyodbc import OperationalError
from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

# Check if the folder exists
if not os.path.exists("logs"):
    # Create the folder
    os.makedirs("logs")
else:
    pass

# Configure logging
logging.basicConfig(filename='./logs/backend.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Read the configuration file to get the database connection details
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

# Create a FastAPI application
app = FastAPI()

# Define the data models for the warehouse record
class WarehouseRecord(BaseModel):
    product_id: str
    product_amount: int

# Define the data models for the product
class Product(BaseModel):
    id: str
    product_name: str
    product_price: float
    producer_id: str
    product_category: str

# Define the data models for the producer
class Producer(BaseModel):
    id: str
    name: str
    surname: str
    company_name: str
    phone: str

# Define the data models for the customer
class Customer(BaseModel):
    id: str
    name: str
    surname: str
    phone: str
    address: str

# Define the data models for the staff
class Staff(BaseModel):
    id: str
    name: str
    surname: str
    position: str

# Define the data models for the buy record
class BuyRecord(BaseModel):
    id: str
    producer_id: str
    product_id: str
    quantity: int
    paid: str

# Define the data models for the sell record
class SellRecord(BaseModel):
    id: str
    customer_id: str
    product_id: str
    quantity: int
    paid: str

# Function to get the database connection
def get_database_connection():
    try:
        conn_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name}'
        conn = pyodbc.connect(conn_string)
        return conn
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define the endpoint to serve an image in full-screen mode
@app.get("/")
async def show_fullscreen_image():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body, html {
        height: 100%;
        margin: 0;
        overflow: hidden;
    }

    .fullscreen-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    </style>
    </head>
    <body>
    <img class="fullscreen-img" src="/image" />
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# Define the endpoint to get the image
@app.get("/image")
async def get_image():
    with open("./images/get.jpg", "rb") as f:
        image_data = f.read()
    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")

# Define the endpoint to get the favicon
@app.get("/favicon.ico")
async def get_favicon():
    # Return a default favicon.ico file
    return FileResponse("ai.ico")

# Define the endpoint to insert a warehouse record
@app.post("/insert-warehouse-record/")
def insert_warehouse_record(warehouse_record: WarehouseRecord):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        # Inserting data into the warehouse table
        cursor.execute('''
            INSERT INTO warehouse (product_id, product_amount)
            VALUES (?, ?);
        ''', (warehouse_record.product_id, warehouse_record.product_amount))
        conn.commit()
    except pyodbc.Error as e:
        conn.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=f"Failed to insert warehouse record: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return {"status": "success", "message": "Warehouse record inserted successfully"}

# Define the endpoint to insert a product
@app.post("/insert-product/")
def insert_product(product: Product):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO products (id, product_name, product_price, producer_id, product_category)
            VALUES (?, ?, ?, ?, ?);
        ''', (product.id, product.product_name, product.product_price, product.producer_id, product.product_category))
        conn.commit()
    except pyodbc.Error as e:
        conn.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=f"Failed to insert product: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return {"status": "success", "message": "Product inserted successfully"}

# Define the endpoint to insert a producer
@app.post("/insert-producer/")
def insert_producer(producer: Producer):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO producers (id, name, surname, company_name, phone)
            VALUES (?, ?, ?, ?, ?);
        ''', (producer.id, producer.name, producer.surname, producer.company_name, producer.phone))
        conn.commit()
    except pyodbc.Error as e:
        conn.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=f"Failed to insert producer: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return {"status": "success", "message": "Producer inserted successfully"}

# Define the endpoint to insert a customer
@app.post("/insert-customer/")
def insert_customer(customer: Customer):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO customers (id, name, surname, phone, address)
            VALUES (?, ?, ?, ?, ?);
        ''', (customer.id, customer.name, customer.surname, customer.phone, customer.address))
        conn.commit()
    except pyodbc.Error as e:
        conn.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=f"Failed to insert customer: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return {"status": "success", "message": "Customer inserted successfully"}

# Define the endpoint to insert a staff member
@app.post("/insert-staff/")
def insert_staff(staff: Staff):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        # SQL command to insert data into the staff table
        cursor.execute('''
            INSERT INTO staff (id, name, surname, position)
            VALUES (?, ?, ?, ?);
        ''', (staff.id, staff.name, staff.surname, staff.position))
        conn.commit()
    except pyodbc.Error as e:
        conn.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=f"Failed to insert staff: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return {"status": "success", "message": "Staff member inserted successfully"}

# Define the endpoint to insert a buy record
@app.post("/insert-buy-record/")
def insert_buy_record(buy_record: BuyRecord):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO buy (id, producer_id, product_id, quantity, paid)
            VALUES (?, ?, ?, ?, ?);
        ''', (buy_record.id, buy_record.producer_id, buy_record.product_id, buy_record.quantity, buy_record.paid))

        cursor.execute('''
            UPDATE warehouse SET product_amount = product_amount + ?
            WHERE product_id = ?;
        ''', (buy_record.quantity, buy_record.product_id))

        conn.commit()
    except pyodbc.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert buy record and update warehouse: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return {"status": "success", "message": "Buy record inserted and warehouse updated successfully"}

# Define the endpoint to insert a sell record
@app.post("/insert-sell-record/")
def insert_sell_record(sell_record: SellRecord):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO sell (id, customer_id, product_id, quantity, paid)
            VALUES (?, ?, ?, ?, ?);
        ''', (sell_record.id, sell_record.customer_id, sell_record.product_id, sell_record.quantity, sell_record.paid))

        cursor.execute('''
            UPDATE warehouse SET product_amount = product_amount - ?
            WHERE product_id = ?;
        ''', (sell_record.quantity, sell_record.product_id))

        conn.commit()
    except pyodbc.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert sell record and update warehouse: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return {"status": "success", "message": "Sell record inserted and warehouse updated successfully"}


if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(app, host="127.0.0.1", port=8000)
