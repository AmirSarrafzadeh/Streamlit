# Frontend with Streamlit
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
                try:
                    error_detail = response.json()["detail"]
                except Exception as e:
                    error_detail = str(e)
                st.error(f"Failed to book study place: {error_detail}")
        else:
            st.error("Please fill in all the required information.")

# Similar functions for borrowing books, checking book existence, and checking study place availability

def main():
    st.title("Library Web Application")

    # Render sidebars
    sidebar_option = st.sidebar.radio("Select Option",
                                      ("Book Study Place", "Borrow a Book",
                                       "Check Book Existence", "Check Study Place Availability"))

    if sidebar_option == "Book Study Place":
        book_study_place()
    # Add similar conditions for other options

if __name__ == "__main__":
    main()
