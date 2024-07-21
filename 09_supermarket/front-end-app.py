"""
This script is the front-end application for the supermarket management system.

Author: Your full name
Date: 2024-05-13

Preconditions:
1. The database and tables are created in SQL Server.
2. The necessary python libraries are installed. You can use requirements.txt to install them.
3. The config.ini file is created and configured with the necessary information.
4. The images folder contains the necessary images for the front-end application.
5. The logs folder is created to store the log files.

Procedure:
1. Run the create_db.py script to create the database and tables.
2. Run this script to start the front-end application.
3. Use the Streamlit UI to interact with the supermarket management system.
"""

# Import necessary libraries
import os
import sys
import pyodbc
import base64
import logging
import datetime
import pandas as pd
import configparser
import streamlit as st
from fastapi import HTTPException

# Check if the folder exists
if not os.path.exists("logs"):
    # Create the folder
    os.makedirs("logs")
else:
    pass

# Configure logging
logging.basicConfig(filename='./logs/frontend.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Read the configuration file and get the necessary information
try:
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)
    driver_name = config['config']['driver_name']
    server_name = config['config']['server_name']
    database_name = config['config']['database_name']
    database_name2 = config['config']['database_name2']
    logging.info("Config file read successfully")
except Exception as e:
    logging.error("Error reading config file: " + str(e))
    sys.exit()


# Function to get the base64 encoding of an image
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Function to set the dimensions of the data tables
def set_table_dimensions():
    st.markdown(
        """
        <style>
        .css-1av738x {  /* This is the class for data tables */
            width: 100% !important;
            height: 500px !important;  /* You can set height here if you want */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Function to get the database connection using pyodbc
set_table_dimensions()


# Function to set the background image of the Streamlit app
def set_background_image(image_path):
    image_base64 = get_image_base64(image_path)
    background_image_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}"); 
        background-size: cover;
        color: lime;
    }}
    </style>
    """
    st.markdown(background_image_css, unsafe_allow_html=True)


# Function to get the database connection using pyodbc
def get_database_connection():
    try:
        conn_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name}'
        connection = pyodbc.connect(conn_string)
        return connection
    except pyodbc.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_database_connection_2():
    try:
        conn_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name2}'
        connection = pyodbc.connect(conn_string)
        return connection
    except pyodbc.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get the database connection using the function
connection_variable = get_database_connection()
connection_variable2 = get_database_connection_2()

# Streamlit UI Layout
st.sidebar.title("Happy  Supermarket 🏪")

# Options for the user to select from the sidebar menu of the Streamlit app
options = ["Producer", "Customer", "Staff", "Product", "Warehouse", "Buy", "Sell"]
choice = st.sidebar.selectbox("Select Option", options)

# Main logic for the Streamlit app
if choice == "Producer":
    producer_option = st.sidebar.radio("Choose Action", ["Insert", "View", "Update", "Delete"])
    set_background_image("./images/producer.jpeg")

    if producer_option == "Insert":
        st.subheader("Insert Producer Data 🏭")
        id = st.text_input("ID")
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        company_name = st.text_input("Company Name")
        phone = st.text_input("Phone")

        if not id:
            st.warning("Please enter Producer ID")
        elif not name:
            st.warning("Please enter Producer Name")
        elif not surname:
            st.warning("Please enter Producer Surname")
        elif not company_name:
            st.warning("Please enter Producer Company Name")
        elif not phone:
            st.warning("Please enter Producer Phone Number")
        else:
            if st.button("Insert Producer"):
                cursor = connection_variable.cursor()
                cursor.execute("INSERT INTO producers (id, name, surname, company_name, phone) VALUES (?, ?, ?, ?, ?);",
                               (id, name, surname, company_name, phone))
                connection_variable.commit()
                st.success("Producer added successfully!")
                st.balloons()

    elif producer_option == "View":
        st.subheader("View Producers 🔍")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM producers;")
        producer_ids = cursor.fetchall()
        producer_ids = [item[0] for item in producer_ids]
        producer_ids.insert(0, '*')
        producer_id_selected = st.selectbox("Choose a Producer ID or '*' to View all", producer_ids)
        if st.button("Fetch Producer"):
            if producer_id_selected == '*':
                cursor.execute("SELECT * FROM producers;")
            else:
                cursor.execute("SELECT * FROM producers WHERE id = ?;", (producer_id_selected,))
            data = cursor.fetchall()
            if data:
                flattened_data = [tuple(item for item in row) for row in data]
                col_names = [column[0] for column in cursor.description]
                df = pd.DataFrame(flattened_data, columns=col_names)
                st.dataframe(df, width=1600)
            else:
                st.error("No data found for the selected option.")

    elif producer_option == "Update":
        st.subheader("Update Producer Data 🔄")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM producers;")
        producer_ids = [item[0] for item in cursor.fetchall()]
        producer_id_selected = st.selectbox("Choose a producer ID to Update", producer_ids)
        column = st.selectbox("Field to Update", ["name", "surname", "company_name", "phone"])
        new_value = st.text_input("New Value")
        if not producer_id_selected:
            st.warning("Please enter Producer ID")
        elif not new_value:
            st.warning("Please enter New Value")
        else:
            if st.button("Update Producer"):
                cursor = connection_variable.cursor()
                try:
                    cursor.execute(f"UPDATE producers SET {column} = ? WHERE id = ?;", (new_value, producer_id_selected))
                    affected_rows = cursor.rowcount
                    connection_variable.commit()
                    if affected_rows > 0:
                        st.success("Producer updated successfully!")
                    else:
                        st.error("No record found with the provided information to update.")
                except Exception as e:
                    connection_variable.rollback()  # Rollback the transaction in case of an error
                    st.error(f"Failed to update producer due to: {str(e)}")
                finally:
                    cursor.close()

    elif producer_option == "Delete":
        st.subheader("Delete Producer ❌")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM producers;")
        producer_ids = [item[0] for item in cursor.fetchall()]
        producer_id_selected = st.selectbox("Choose a producer ID to Delete", producer_ids)
        if not producer_id_selected:
            st.warning("Please enter Producer ID")
        else:
            if st.button("Delete Producer"):
                cursor = connection_variable.cursor()
                try:
                    # Execute the DELETE command
                    cursor.execute("DELETE FROM producers WHERE id = ?;", (producer_id_selected,))
                    affected_rows = cursor.rowcount  # This checks the number of affected rows
                    connection_variable.commit()

                    if affected_rows > 0:
                        st.success("Producer deleted successfully!")
                    else:
                        st.error("No producer found with the provided ID.")
                except Exception as e:
                    connection_variable.rollback()  # Rollback the transaction in case of an error
                    st.error(f"Failed to delete producer due to: {str(e)}")
                finally:
                    cursor.close()
    st.sidebar.markdown('<div style="margin-bottom: 200px;"></div>', unsafe_allow_html=True)
    st.sidebar.image("./images/producer_icon.webp", use_column_width=True, caption="Producer")

elif choice == "Customer":
    customer_option = st.sidebar.radio("Choose Action", ["Insert", "View", "Update", "Delete"])
    set_background_image("./images/Customer.jpg")

    if customer_option == "Insert":
        st.subheader("Insert Customer Data 🛒")
        id = st.text_input("ID")
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        phone = st.text_input("Phone")
        address = st.text_input("Address")

        if not id:
            st.warning("Please enter Customer ID")
        elif not name:
            st.warning("Please enter Customer Name")
        elif not surname:
            st.warning("Please enter Customer Surname")
        elif not phone:
            st.warning("Please enter Customer Phone Number")
        elif not address:
            st.warning("Please enter Customer Address")
        else:
            if st.button("Insert Customer"):
                cursor = connection_variable.cursor()
                cursor.execute("INSERT INTO customers (id, name, surname, phone, address) VALUES (?, ?, ?, ?, ?);",
                               (id, name, surname, phone, address))
                connection_variable.commit()
                st.success("Customer added successfully!")
                st.balloons()

    elif customer_option == "View":
        st.subheader("View Customers 🔍")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM customers;")
        customers_ids = cursor.fetchall()
        customer_ids = [item[0] for item in customers_ids]
        customer_ids.insert(0, '*')
        customer_id_selected = st.selectbox("Choose a Customer ID or '*' to View all", customer_ids)
        if st.button("Fetch Customer"):
            if customer_id_selected == '*':
                cursor.execute("SELECT * FROM customers;")
            else:
                cursor.execute("SELECT * FROM customers WHERE id = ?;", (customer_id_selected,))
            data = cursor.fetchall()
            if data:
                flattened_data = [tuple(item for item in row) for row in data]
                col_names = [column[0] for column in cursor.description]
                df = pd.DataFrame(flattened_data, columns=col_names)
                st.dataframe(df, width=1600)
            else:
                st.error("No data found for the selected option.")

    elif customer_option == "Update":
        st.subheader("Update Customer Data 🔄")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM customers;")
        customer_ids = [item[0] for item in cursor.fetchall()]
        id = st.selectbox("Choose a customer ID to Update", customer_ids)
        column = st.selectbox("Field to Update", ["name", "surname", "phone", "address"])
        new_value = st.text_input("New Value")
        if st.button("Update Customer"):
            cursor = connection_variable.cursor()
            cursor.execute(f"UPDATE customers SET {column} = ? WHERE id = ?;", (new_value, id))
            connection_variable.commit()
            st.success("Customer updated successfully!")

    elif customer_option == "Delete":
        st.subheader("Delete Customer ❌")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM customers;")
        customer_ids = [item[0] for item in cursor.fetchall()]
        id = st.selectbox("Choose a customer ID to Delete", customer_ids)
        if st.button("Delete Customer"):
            cursor = connection_variable.cursor()
            cursor.execute("DELETE FROM customers WHERE id = ?;", (id,))
            connection_variable.commit()
            st.success("Customer deleted successfully!")

    st.sidebar.markdown('<div style="margin-bottom: 200px;"></div>', unsafe_allow_html=True)
    st.sidebar.image("./images/customer_icon.png", use_column_width=True, caption="Customer")
elif choice == "Staff":
    staff_option = st.sidebar.radio("Choose Action", ["Insert", "View", "Update", "Delete"])
    set_background_image("./images/Staff.jpg")

    if staff_option == "Insert":
        st.subheader("Insert Staff Data 🧑‍🍳")
        id = st.text_input("ID")
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        position = st.text_input("Position")

        if not id:
            st.warning("Please enter Staff ID")
        elif not name:
            st.warning("Please enter Staff Name")
        elif not surname:
            st.warning("Please enter Staff Surname")
        elif not position:
            st.warning("Please enter Staff Position")
        else:
            if st.button("Insert Staff"):
                cursor = connection_variable.cursor()
                cursor.execute("INSERT INTO staff (id, name, surname, position) VALUES (?, ?, ?, ?);",
                               (id, name, surname, position))
                connection_variable.commit()
                st.success("Staff added successfully!")
                st.balloons()

    elif staff_option == "View":
        st.subheader("View Staff 🔍")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM staff;")
        staffs_ids = cursor.fetchall()
        staff_ids = [id[0] for id in staffs_ids]
        staff_ids.insert(0, '*')
        staff_id_selected = st.selectbox("Choose a Staff ID or '*' to View all", staff_ids)
        if st.button("Fetch Staff"):
            if staff_id_selected == '*':
                cursor.execute("SELECT * FROM staff;")
            else:
                cursor.execute("SELECT * FROM staff WHERE id = ?;", (staff_id_selected,))
            data = cursor.fetchall()
            if data:
                flattened_data = [tuple(item for item in row) for row in data]
                col_names = [column[0] for column in cursor.description]
                df = pd.DataFrame(flattened_data, columns=col_names)
                st.dataframe(df, width=1600)
            else:
                st.error("No data found for the selected option.")

    elif staff_option == "Update":
        st.subheader("Update Staff Data 🔄")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM staff;")
        staff_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a staff ID to Update", staff_ids)
        column = st.selectbox("Field to Update", ["name", "surname", "position"])
        new_value = st.text_input("New Value")
        if st.button("Update Staff"):
            cursor = connection_variable.cursor()
            cursor.execute(f"UPDATE staff SET {column} = ? WHERE id = ?;", (new_value, id))
            connection_variable.commit()
            st.success("Staff updated successfully!")

    elif staff_option == "Delete":
        st.subheader("Delete Staff ❌")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM staff;")
        staff_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a staff ID to Delete", staff_ids)
        if st.button("Delete Staff"):
            cursor = connection_variable.cursor()
            cursor.execute("DELETE FROM staff WHERE id = ?;", (id,))
            connection_variable.commit()
            st.success("Staff deleted successfully!")

    st.sidebar.markdown('<div style="margin-bottom: 200px;"></div>', unsafe_allow_html=True)
    st.sidebar.image("./images/staff_icon.png", use_column_width=True, caption="Staff")
elif choice == "Product":
    product_option = st.sidebar.radio("Choose Action", ["Insert", "View", "Update", "Delete", "Actions"])
    set_background_image("./images/Product.jpg")

    if product_option == "Insert":
        st.subheader("Insert Product Data 🛍️")
        id = st.text_input("ID")
        product_name = st.text_input("Product Name")
        product_price = st.number_input("Product Price", step=0.01)
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM producers;")
        producers_ids = [id[0] for id in cursor.fetchall()]
        producer_id = st.selectbox("Choose a producer ID", producers_ids)
        product_category = st.text_input("Product Category")

        if not id:
            st.warning("Please enter Product ID")
        elif not product_name:
            st.warning("Please enter Product Name")
        elif not product_price:
            st.warning("Please enter Product Price")
        elif not producer_id:
            st.warning("Please enter Producer ID")
        elif not product_category:
            st.warning("Please enter Product Category")
        else:
            if st.button("Insert Product"):
                cursor = connection_variable.cursor()
                cursor.execute("INSERT INTO products (id, product_name, product_price, producer_id, product_category) VALUES (?, ?, ?, ?, ?);",
                               (id, product_name, product_price, producer_id, product_category))

                cursor2 = connection_variable2.cursor()
                cursor2.execute("INSERT INTO actions (id, action, timestamp) VALUES (?, ?, ?);", (id, "Product Inserted", datetime.datetime.now()))
                connection_variable.commit()
                connection_variable2.commit()
                st.success("Product added successfully!")

    elif product_option == "View":
        st.subheader("View Product 🔍")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM products;")
        products_ids = cursor.fetchall()
        product_ids = [id[0] for id in products_ids]
        product_ids.insert(0, '*')
        product_id_selected = st.selectbox("Choose a product ID or '*' to View all", product_ids)
        if st.button("Fetch Product"):
            if product_id_selected == '*':
                cursor.execute("SELECT * FROM products;")
            else:
                cursor.execute("SELECT * FROM products WHERE id = ?;", (product_id_selected,))
            data = cursor.fetchall()
            if data:
                flattened_data = [tuple(item for item in row) for row in data]
                col_names = [column[0] for column in cursor.description]
                df = pd.DataFrame(flattened_data, columns=col_names)
                st.dataframe(df, width=1600)
            else:
                st.error("No data found for the selected option.")

    elif product_option == "Update":
        st.subheader("Update Product Data 🔄")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM products;")
        product_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a product ID to Update", product_ids)
        column = st.selectbox("Field to Update", ["product_name", "product_price", "producer_id", "product_category"])
        new_value = st.text_input("New Value")
        if st.button("Update Product"):
            cursor = connection_variable.cursor()
            cursor.execute(f"UPDATE products SET {column} = ? WHERE id = ?;", (new_value, id))
            cursor2 = connection_variable2.cursor()
            cursor2.execute("INSERT INTO actions (id, action, timestamp) VALUES (?, ?, ?);", (id, "Product Updated", datetime.datetime.now()))
            connection_variable.commit()
            connection_variable2.commit()
            st.success("Product updated successfully!")

    elif product_option == "Delete":
        st.subheader("Delete Product ❌")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM products;")
        product_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a product ID to Delete", product_ids)
        if st.button("Delete Product"):
            cursor = connection_variable.cursor()
            cursor2 = connection_variable2.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?;", (id,))
            cursor2.execute("INSERT INTO actions (id, action, timestamp) VALUES (?, ?, ?);", (id, "Product Deleted", datetime.datetime.now()))
            connection_variable.commit()
            connection_variable2.commit()
            st.success("Product deleted successfully!")

    elif product_option == "Actions":
        st.subheader("Actions")
        cursor = connection_variable2.cursor()
        cursor.execute("SELECT * FROM actions;")
        data = cursor.fetchall()
        if data:
            flattened_data = [tuple(item for item in row) for row in data]
            col_names = [column[0] for column in cursor.description]
            df = pd.DataFrame(flattened_data, columns=col_names)
            st.dataframe(df, width=1600)
        else:
            st.error("No data found.")

    st.sidebar.markdown('<div style="margin-bottom: 200px;"></div>', unsafe_allow_html=True)
    st.sidebar.image("./images/product_icon.png", use_column_width=True, caption="Product")

elif choice == "Warehouse":
    st.subheader("Warehouse Stock")
    set_background_image("./images/Warehouse.jpg")
    cursor = connection_variable.cursor()
    cursor.execute("SELECT * FROM warehouse;")
    data = cursor.fetchall()
    cursor2 = connection_variable.cursor()
    cursor2.execute("SELECT * FROM products;")
    data2 = cursor2.fetchall()
    if data2 and data:
        flattened_data_1 = [tuple(item for item in row) for row in data]
        flattened_data_2 = [tuple(item for item in row) for row in data2]
        final_data1 = pd.DataFrame(flattened_data_1, columns=[column[0] for column in cursor.description])
        final_data2 = pd.DataFrame(flattened_data_2, columns=[column[0] for column in cursor2.description])
        final_data = final_data1.merge(final_data2, left_on='product_id', right_on='id', how='left')
        final_data = final_data.drop(columns=['id'])
        st.dataframe(final_data, width=2500)
    else:
        st.markdown("There is not any product in the warehouse.")
    st.sidebar.markdown('<div style="margin-bottom: 350px;"></div>', unsafe_allow_html=True)
    st.sidebar.image("./images/warehouse_icon.jpg", use_column_width=True, caption="Warehouse")


elif choice == "Buy":
    buy_option = st.sidebar.radio("Choose Action", ["Insert", "View", "Update", "Delete"])
    set_background_image("./images/buy.jpg")

    if buy_option == "Insert":
        st.subheader("Insert Buy Record")
        id = st.text_input("Record ID")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM producers;")
        producers_ids = [id[0] for id in cursor.fetchall()]
        producer_id = st.selectbox("Choose a producer ID", producers_ids)
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM products;")
        products_ids = [id[0] for id in cursor.fetchall()]
        product_id = st.selectbox("Choose a product ID", products_ids)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        paid = st.selectbox("Payment By", ["Cash", "Credit Card", "Online Transfer"])
        if not id:
            st.warning("Please enter Record ID")
        elif not producer_id:
            st.warning("Please enter Producer ID")
        elif not product_id:
            st.warning("Please enter Product ID")
        elif not quantity:
            st.warning("Please enter Quantity")
        else:
            if st.button("Insert Buy Record"):
                cursor = connection_variable.cursor()
                try:
                    # Insert buy record
                    cursor.execute("""
                                        INSERT INTO buy (id, producer_id, product_id, quantity, paid) 
                                        VALUES (?, ?, ?, ?, ?);
                                    """, (id, producer_id, product_id, quantity, paid))

                    # Check if product exists in warehouse
                    cursor.execute("SELECT product_amount FROM warehouse WHERE product_id = ?;", (product_id,))
                    warehouse_data = cursor.fetchone()

                    if warehouse_data:
                        # Update warehouse quantity
                        cursor.execute("""
                                            UPDATE warehouse SET product_amount = product_amount + ? 
                                            WHERE product_id = ?;
                                        """, (quantity, product_id))
                    else:
                        # Insert new product into warehouse
                        cursor.execute("""
                                            INSERT INTO warehouse (product_id, product_amount) 
                                            VALUES (?, ?);
                                        """, (product_id, quantity))

                    connection_variable.commit()
                    st.success("Buy record inserted and warehouse updated successfully!")
                except Exception as e:
                    connection_variable.rollback()
                    st.error(f"Failed to insert buy record and update warehouse: {str(e)}")
                finally:
                    cursor.close()

    elif buy_option == "View":
        st.subheader("View Buy Records")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM buy;")
        buy_ids = [id[0] for id in cursor.fetchall()]
        buy_ids.insert(0, '*')
        buy_id_selected = st.selectbox("Choose a Buy Record ID or '*' to View all", buy_ids)
        if st.button("Fetch Buy Records"):
            if buy_id_selected == '*':
                cursor.execute("SELECT * FROM buy;")
            else:
                cursor.execute("SELECT * FROM buy WHERE id = ?;", (buy_id_selected,))
            data = cursor.fetchall()
            if data:
                flattened_data = [tuple(item for item in row) for row in data]
                col_names = [column[0] for column in cursor.description]
                df = pd.DataFrame(flattened_data, columns=col_names)
                st.dataframe(df, width=1600)
            else:
                st.error("No data found.")

    elif buy_option == "Update":
        st.subheader("Update Buy Record")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM buy;")
        buy_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a Buy ID to Update", buy_ids)
        column = st.selectbox("Field to Update", ["producer_id", "product_id", "paid"])
        if column == 'paid':
            new_value = st.selectbox("New Payment By", ["Cash", "Credit Card", "Online Transfer"])
        else:
            new_value = st.text_input("New Value")
        if st.button("Update Buy Record"):
            cursor = connection_variable.cursor()
            try:
                update_query = f"UPDATE buy SET {column} = ? WHERE id = ?;"
                cursor.execute(update_query, (new_value, id))
                connection_variable.commit()
                if cursor.rowcount > 0:
                    st.success("Buy record updated successfully!")
                else:
                    st.error("No record found to update.")
            except Exception as e:
                connection_variable.rollback()
                st.error(f"Failed to update buy record: {str(e)}")
            finally:
                cursor.close()

    elif buy_option == "Delete":
        st.subheader("Delete Buy Record")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM buy;")
        buy_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a Buy ID to Delete", buy_ids)
        if st.button("Delete Buy Record"):
            cursor = connection_variable.cursor()
            try:
                cursor.execute("DELETE FROM buy WHERE id = ?;", (id,))
                connection_variable.commit()
                st.success("Buy record deleted successfully!")
            except Exception as e:
                connection_variable.rollback()
                st.error(f"Failed to delete buy record: {str(e)}")
            finally:
                cursor.close()

    st.sidebar.markdown('<div style="margin-bottom: 200px;"></div>', unsafe_allow_html=True)
    st.sidebar.image("./images/buy_icon.png", use_column_width=True, caption="Buy")

elif choice == "Sell":
    sell_option = st.sidebar.radio("Choose Action", ["Insert", "View", "Update", "Delete"])
    set_background_image("./images/sell.jpg")

    if sell_option == "Insert":
        st.subheader("Insert Sell Record")
        id = st.text_input("Record ID")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM customers;")
        customers_ids = [id[0] for id in cursor.fetchall()]
        customer_id = st.selectbox("Choose a customer ID", customers_ids)
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM products;")
        products_ids = [id[0] for id in cursor.fetchall()]
        product_id = st.selectbox("Choose a product ID", products_ids)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        paid = st.selectbox("Payment By", ["Cash", "Credit Card", "Online Transfer"])
        if not id:
            st.warning("Please enter Record ID")
        elif not customer_id:
            st.warning("Please enter Customer ID")
        elif not product_id:
            st.warning("Please enter Product ID")
        elif not quantity:
            st.warning("Please enter Quantity")
        else:
            if st.button("Insert Sell Record"):
                cursor = connection_variable.cursor()
                try:
                    # Check if product exists in warehouse
                    cursor.execute("SELECT product_amount FROM warehouse WHERE product_id = ?;", (product_id,))
                    warehouse_data = cursor.fetchone()

                    if warehouse_data and warehouse_data[0] >= quantity:
                        # Insert sell record
                        cursor.execute("""
                                            INSERT INTO sell (id, customer_id, product_id, quantity, paid) 
                                            VALUES (?, ?, ?, ?, ?);
                                        """, (id, customer_id, product_id, quantity, paid))

                        # Update warehouse quantity
                        cursor.execute("""
                                            UPDATE warehouse SET product_amount = product_amount - ? 
                                            WHERE product_id = ?;
                                        """, (quantity, product_id))

                        connection_variable.commit()
                        st.success("Sell record inserted and warehouse updated successfully!")
                    else:
                        st.error("Not enough product in the warehouse or product does not exist.")

                except Exception as e:
                    connection_variable.rollback()
                    st.error(f"Failed to insert sell record and update warehouse: {str(e)}")
                finally:
                    cursor.close()

    elif sell_option == "View":
        st.subheader("View Sell Records")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM sell;")
        sell_ids = [id[0] for id in cursor.fetchall()]
        sell_ids.insert(0, '*')
        sell_id_selected = st.selectbox("Choose a Sell Record ID or '*' to View all", sell_ids)
        if st.button("Fetch Sell Records"):
            if sell_id_selected == '*':
                cursor.execute("SELECT * FROM sell;")
            else:
                cursor.execute("SELECT * FROM sell WHERE id = ?;", (sell_id_selected,))
            data = cursor.fetchall()
            if data:
                flattened_data = [tuple(item for item in row) for row in data]
                col_names = [column[0] for column in cursor.description]
                df = pd.DataFrame(flattened_data, columns=col_names)
                st.dataframe(df, width=1600)
            else:
                st.error("No data found.")

    elif sell_option == "Update":
        st.subheader("Update Sell Record")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM sell;")
        sell_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a Sell ID to Update", sell_ids)
        column = st.selectbox("Field to Update", ["customer_id", "product_id", "paid"])
        if column == 'paid':
            new_value = st.selectbox("New Payment By", ["Cash", "Credit Card", "Online Transfer"])
        else:
            new_value = st.text_input("New Value")
        if st.button("Update Sell Record"):
            cursor = connection_variable.cursor()
            try:
                update_query = f"UPDATE sell SET {column} = ? WHERE id = ?;"
                cursor.execute(update_query, (new_value, id))
                connection_variable.commit()
                if cursor.rowcount > 0:
                    st.success("Sell record updated successfully!")
                else:
                    st.error("No record found to update.")
            except Exception as e:
                connection_variable.rollback()
                st.error(f"Failed to update sell record: {str(e)}")
            finally:
                cursor.close()

    elif sell_option == "Delete":
        st.subheader("Delete Sell Record")
        cursor = connection_variable.cursor()
        cursor.execute("SELECT id FROM sell;")
        sell_ids = [id[0] for id in cursor.fetchall()]
        id = st.selectbox("Choose a Sell ID to Delete", sell_ids)
        if st.button("Delete Sell Record"):
            cursor = connection_variable.cursor()
            try:
                cursor.execute("DELETE FROM sell WHERE id = ?;", (id,))
                connection_variable.commit()
                st.success("Sell record deleted successfully!")
            except Exception as e:
                connection_variable.rollback()
                st.error(f"Failed to delete sell record: {str(e)}")
            finally:
                cursor.close()

    st.sidebar.markdown('<div style="margin-bottom: 200px;"></div>', unsafe_allow_html=True)
    st.sidebar.image("./images/sell_icon.png", use_column_width=True, caption="Sell")
