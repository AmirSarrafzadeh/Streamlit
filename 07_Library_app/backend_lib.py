# Backend API with FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["library"]
study_places_collection = db["study_places"]
books_collection = db["books"]

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
    existing_booking = study_places_collection.find_one({
        "date": booking.date,
        "$or": [
            {"start_time": {"$lt": booking.start_time}, "end_time": {"$gt": booking.start_time}},
            {"start_time": {"$lt": booking.end_time}, "end_time": {"$gt": booking.end_time}}
        ]
    })

    if existing_booking:
        raise HTTPException(status_code=400, detail="Study place already booked for this time slot")

    # Add the booking to the database
    booking_data = booking.dict()
    study_places_collection.insert_one(booking_data)
    return {"message": "Study place booked successfully"}


@app.post("/borrow_book")
def borrow_book(borrowing: BookBorrowing):
    # Check if the book is available
    book_status = books_collection.find_one({"name": borrowing.book_name})
    if not book_status or not book_status["available"]:
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")

    # Borrow the book
    books_collection.update_one({"name": borrowing.book_name}, {"$set": {"available": False}})
    return {"message": f"Book '{borrowing.book_name}' borrowed successfully"}


@app.get("/check_book_existence")
def check_book_existence(book_name: str):
    book_status = books_collection.find_one({"name": book_name})
    if book_status:
        return {"message": f"Book '{book_name}' {'is' if book_status['available'] else 'is not'} available"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get("/check_study_place_availability")
def check_study_place_availability(date: datetime, start_time: time, end_time: time):
    # Check if the study place is available for the given time slot
    existing_booking = study_places_collection.find_one({
        "date": date,
        "$or": [
            {"start_time": {"$lt": start_time}, "end_time": {"$gt": start_time}},
            {"start_time": {"$lt": end_time}, "end_time": {"$gt": end_time}}
        ]
    })

    if existing_booking:
        return {"message": "Study place is not available"}

    return {"message": "Study place is available"}


# Dummy function to reset the databases
@app.post("/reset_databases")
def reset_databases():
    study_places_collection.drop()
    books_collection.drop()
    study_places_collection.insert_many([])
    books_collection.insert_many([
        {"name": "Book1", "available": True},
        {"name": "Book2", "available": False},
        {"name": "Book3", "available": True}
    ])
    return {"message": "Databases reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
