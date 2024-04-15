from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time
import uvicorn

app = FastAPI()

# Database to store booked study places
booked_study_places = {}

# Database to store borrowed books
borrowed_books = {}

# Dummy database of available books
available_books = {"Book1": True, "Book2": False, "Book3": True}


class StudyPlaceBooking(BaseModel):
    matricola: int = Field(..., description="Matricola of the student")
    name: str = Field(..., description="Name of the student")
    surname: str = Field(..., description="Surname of the student")
    date: datetime = Field(..., description="Date of the booking")
    start_time: time = Field(..., description="Start time of the booking")
    end_time: time = Field(..., description="End time of the booking")


class BookBorrowing(BaseModel):
    book_name: str = Field(..., description="Name of the book to borrow")


@app.post("/book_study_place")
def book_study_place(booking: StudyPlaceBooking):
    # Check if the study place is already booked for the given time slot
    for place in booked_study_places.values():
        if (booking.date == place.date and
                ((booking.start_time >= place.start_time and booking.start_time < place.end_time) or
                 (booking.end_time > place.start_time and booking.end_time <= place.end_time))):
            raise HTTPException(status_code=400, detail="Study place already booked for this time slot")

    # Add the booking to the database
    booking_info = booking.dict()
    booked_study_places[booking_info["matricola"]] = booking_info
    return {"message": "Study place booked successfully"}


@app.post("/borrow_book")
def borrow_book(borrowing: BookBorrowing):
    # Check if the book is available
    if borrowing.book_name not in available_books or not available_books[borrowing.book_name]:
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")

    # Borrow the book
    available_books[borrowing.book_name] = False
    borrowed_books[borrowing.book_name] = datetime.now()
    return {"message": f"Book '{borrowing.book_name}' borrowed successfully"}


@app.get("/check_book_existence")
def check_book_existence(book_name: str):
    if book_name in available_books:
        return {"message": f"Book '{book_name}' {'is' if available_books[book_name] else 'is not'} available"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get("/check_study_place_availability")
def check_study_place_availability(date: datetime, start_time: time, end_time: time):
    # Check if the study place is available for the given time slot
    for place in booked_study_places.values():
        if (date == place["date"] and
                ((start_time >= place["start_time"] and start_time < place["end_time"]) or
                 (end_time > place["start_time"] and end_time <= place["end_time"]))):
            return {"message": "Study place is not available"}

    return {"message": "Study place is available"}


# Dummy function to reset the databases
@app.post("/reset_databases")
def reset_databases():
    global booked_study_places, borrowed_books, available_books
    booked_study_places = {}
    borrowed_books = {}
    available_books = {"Book1": True, "Book2": False, "Book3": True}
    return {"message": "Databases reset successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
