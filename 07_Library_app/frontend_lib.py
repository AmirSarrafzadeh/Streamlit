import streamlit as st
import requests
from datetime import datetime, time

# Backend API URL
backend_url = "http://localhost:8000"

def book_study_place():
    st.header("Book Study Place")

    # Inputs for booking a study place
    matricola = st.text_input("Matricola")
    name = st.text_input("Name")
    surname = st.text_input("Surname")
    date = st.date_input("Date")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")

    # Add functionality for booking the study place
    if st.button("Book"):
        # Validate inputs
        if matricola and name and surname and date and start_time and end_time:
            # Create booking payload
            booking_payload = {
                "matricola": int(matricola),
                "name": name,
                "surname": surname,
                "date": date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M:%S"),
                "end_time": end_time.strftime("%H:%M:%S")
            }

            # Make POST request to backend API
            response = requests.post(f"{backend_url}/book_study_place", json=booking_payload)

            if response.status_code == 200:
                st.success("Booking successful!")
            else:
                st.error(f"Failed to book study place: {response.json()['detail']}")
        else:
            st.error("Please fill in all the required information.")

# Sidebar for borrowing a book
def borrow_book():
    st.sidebar.header("Borrow a Book")
    # Add necessary inputs and functionality for borrowing a book

# Sidebar for checking if a book exists
def check_book_existence():
    st.sidebar.header("Check Book Existence")
    # Add necessary inputs and functionality for checking if a book exists

# Sidebar for checking the availability of study places
def check_study_place_availability():
    st.sidebar.header("Check Study Place Availability")
    # Add necessary inputs and functionality for checking the availability of study places

# Main function
def main():
    st.title("Library Web Application")

    # Render sidebars
    sidebar_option = st.sidebar.radio("Select Option",
                                      ("Book Study Place", "Borrow a Book",
                                       "Check Book Existence", "Check Study Place Availability"))

    if sidebar_option == "Book Study Place":
        book_study_place()
    elif sidebar_option == "Borrow a Book":
        borrow_book()
    elif sidebar_option == "Check Book Existence":
        check_book_existence()
    elif sidebar_option == "Check Study Place Availability":
        check_study_place_availability()


if __name__ == "__main__":
    main()
