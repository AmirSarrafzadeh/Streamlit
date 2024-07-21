from pymongo import MongoClient

# Data to insert
data = [
    {"Rank": 1, "Nation": "Soviet Union", "Gold": 253, "Silver": 93, "Bronze": 69, "Total": 415},
    {"Rank": 2, "Nation": "Japan", "Gold": 135, "Silver": 74, "Bronze": 87, "Total": 296},
    {"Rank": 3, "Nation": "Russia", "Gold": 111, "Silver": 68, "Bronze": 96, "Total": 275},
    {"Rank": 4, "Nation": "United States", "Gold": 86, "Silver": 105, "Bronze": 109, "Total": 300},
    {"Rank": 5, "Nation": "Iran", "Gold": 70, "Silver": 66, "Bronze": 79, "Total": 215},
    {"Rank": 6, "Nation": "Bulgaria", "Gold": 63, "Silver": 95, "Bronze": 103, "Total": 261},
    {"Rank": 7, "Nation": "Turkey", "Gold": 60, "Silver": 62, "Bronze": 83, "Total": 205},
    {"Rank": 8, "Nation": "Hungary", "Gold": 33, "Silver": 53, "Bronze": 53, "Total": 139},
    {"Rank": 9, "Nation": "Cuba", "Gold": 32, "Silver": 28, "Bronze": 49, "Total": 109},
    {"Rank": 10, "Nation": "Sweden", "Gold": 31, "Silver": 40, "Bronze": 48, "Total": 119},
    {"Rank": 11, "Nation": "China", "Gold": 28, "Silver": 21, "Bronze": 39, "Total": 88},
    {"Rank": 12, "Nation": "France", "Gold": 27, "Silver": 22, "Bronze": 24, "Total": 73},
    {"Rank": 13, "Nation": "Germany", "Gold": 22, "Silver": 28, "Bronze": 47, "Total": 97},
    {"Rank": 14, "Nation": "Finland", "Gold": 22, "Silver": 26, "Bronze": 25, "Total": 73},
    {"Rank": 15, "Nation": "Azerbaijan", "Gold": 19, "Silver": 34, "Bronze": 39, "Total": 92},
    {"Rank": 16, "Nation": "Ukraine", "Gold": 19, "Silver": 21, "Bronze": 61, "Total": 101},
    {"Rank": 17, "Nation": "Georgia", "Gold": 16, "Silver": 20, "Bronze": 42, "Total": 78},
    {"Rank": 18, "Nation": "Poland", "Gold": 15, "Silver": 38, "Bronze": 39, "Total": 92},
    {"Rank": 19, "Nation": "Romania", "Gold": 15, "Silver": 32, "Bronze": 37, "Total": 84},
    {"Rank": 20, "Nation": "South Korea", "Gold": 14, "Silver": 23, "Bronze": 25, "Total": 62},
    {"Rank": 21, "Nation": "Canada", "Gold": 14, "Silver": 18, "Bronze": 32, "Total": 64},
    {"Rank": 22, "Nation": "Armenia", "Gold": 14, "Silver": 10, "Bronze": 21, "Total": 45},
    {"Rank": 23, "Nation": "Norway", "Gold": 12, "Silver": 17, "Bronze": 29, "Total": 58},
    {"Rank": 24, "Nation": "Austria", "Gold": 11, "Silver": 9, "Bronze": 8, "Total": 28},
    {"Rank": 25, "Nation": "North Korea", "Gold": 10, "Silver": 5, "Bronze": 10, "Total": 25},
    {"Rank": 26, "Nation": "West Germany", "Gold": 9, "Silver": 13, "Bronze": 19, "Total": 41},
    {"Rank": 27, "Nation": "East Germany", "Gold": 8, "Silver": 23, "Bronze": 23, "Total": 54},
    {"Rank": 28, "Nation": "Kyrgyzstan", "Gold": 8, "Silver": 5, "Bronze": 13, "Total": 26},
    {"Rank": 29, "Nation": "Serbia", "Gold": 8, "Silver": 1, "Bronze": 11, "Total": 20},
    {"Rank": 30, "Nation": "Mongolia", "Gold": 7, "Silver": 27, "Bronze": 43, "Total": 77},
    {"Rank": 31, "Nation": "Kazakhstan", "Gold": 6, "Silver": 19, "Bronze": 35, "Total": 60},
    {"Rank": 32, "Nation": "Belarus", "Gold": 6, "Silver": 17, "Bronze": 27, "Total": 50},
    {"Rank": 33, "Nation": "Uzbekistan", "Gold": 6, "Silver": 11, "Bronze": 22, "Total": 39},
    {"Rank": 34, "Nation": "Yugoslavia", "Gold": 5, "Silver": 19, "Bronze": 17, "Total": 41},
    {"Rank": 35, "Nation": "Denmark", "Gold": 5, "Silver": 8, "Bronze": 10, "Total": 23},
    {"Rank": 36, "Nation": "Moldova", "Gold": 4, "Silver": 8, "Bronze": 4, "Total": 16},
    {"Rank": 37, "Nation": "Russian Wrestling Federation[a]", "Gold": 4, "Silver": 5, "Bronze": 9, "Total": 18},
    {"Rank": 38, "Nation": "Italy", "Gold": 3, "Silver": 8, "Bronze": 12, "Total": 23},
    {"Rank": 39, "Nation": "Czechoslovakia", "Gold": 3, "Silver": 6, "Bronze": 11, "Total": 20},
    {"Rank": 40, "Nation": "Venezuela", "Gold": 3, "Silver": 4, "Bronze": 5, "Total": 12},
    {"Rank": 41, "Nation": "Egypt", "Gold": 3, "Silver": 3, "Bronze": 6, "Total": 12},
    {"Rank": 42, "Nation": "Estonia", "Gold": 2, "Silver": 3, "Bronze": 5, "Total": 10},
    {"Rank": 43, "Nation": "Individual Neutral Athletes[b]", "Gold": 2, "Silver": 2, "Bronze": 2, "Total": 6},
    {"Rank": 44, "Nation": "India", "Gold": 1, "Silver": 5, "Bronze": 16, "Total": 22},
    {"Rank": 45, "Nation": "Chinese Taipei", "Gold": 1, "Silver": 5, "Bronze": 6, "Total": 12},
    {"Rank": 46, "Nation": "Greece", "Gold": 1, "Silver": 3, "Bronze": 12, "Total": 16},
    {"Rank": 47, "Nation": "Israel", "Gold": 1, "Silver": 1, "Bronze": 4, "Total": 6},
    {"Rank": 48, "Nation": "Bahrain", "Gold": 1, "Silver": 1, "Bronze": 0, "Total": 2},
    {"Rank": 49, "Nation": "Albania", "Gold": 1, "Silver": 0, "Bronze": 2, "Total": 3},
    {"Rank": 50, "Nation": "Belgium", "Gold": 1, "Silver": 0, "Bronze": 1, "Total": 2},
    {"Rank": 51, "Nation": "Slovakia", "Gold": 0, "Silver": 4, "Bronze": 3, "Total": 7},
    {"Rank": 52, "Nation": "Czech Republic", "Gold": 0, "Silver": 2, "Bronze": 4, "Total": 6},
    {"Rank": 53, "Nation": "Puerto Rico", "Gold": 0, "Silver": 2, "Bronze": 1, "Total": 3},
    {"Rank": 54, "Nation": "Nigeria", "Gold": 0, "Silver": 1, "Bronze": 5, "Total": 6},
    {"Rank": 55, "Nation": "Lithuania", "Gold": 0, "Silver": 1, "Bronze": 4, "Total": 5},
    {"Rank": 56, "Nation": "Latvia", "Gold": 0, "Silver": 1, "Bronze": 3, "Total": 4},
    {"Rank": 57, "Nation": "Netherlands", "Gold": 0, "Silver": 1, "Bronze": 3, "Total": 4},
    {"Rank": 58, "Nation": "Croatia", "Gold": 0, "Silver": 1, "Bronze": 2, "Total": 3},
    {"Rank": 59, "Nation": "Lebanon", "Gold": 0, "Silver": 1, "Bronze": 1, "Total": 2},
    {"Rank": 60, "Nation": "North Macedonia", "Gold": 0, "Silver": 1, "Bronze": 1, "Total": 2},
    {"Rank": 61, "Nation": "Brazil", "Gold": 0, "Silver": 1, "Bronze": 0, "Total": 1},
    {"Rank": 62, "Nation": "Tajikistan", "Gold": 0, "Silver": 1, "Bronze": 0, "Total": 1},
    {"Rank": 63, "Nation": "Tunisia", "Gold": 0, "Silver": 1, "Bronze": 0, "Total": 1},
    {"Rank": 64, "Nation": "Turkmenistan", "Gold": 0, "Silver": 1, "Bronze": 0, "Total": 1},
    {"Rank": 65, "Nation": "Spain", "Gold": 0, "Silver": 0, "Bronze": 3, "Total": 3},
    {"Rank": 66, "Nation": "Switzerland", "Gold": 0, "Silver": 0, "Bronze": 3, "Total": 3},
    {"Rank": 67, "Nation": "Bohemia", "Gold": 0, "Silver": 0, "Bronze": 2, "Total": 2},
    {"Rank": 68, "Nation": "Colombia", "Gold": 0, "Silver": 0, "Bronze": 2, "Total": 2},
    {"Rank": 69, "Nation": "Pakistan", "Gold": 0, "Silver": 0, "Bronze": 2, "Total": 2},
    {"Rank": 70, "Nation": "Argentina", "Gold": 0, "Silver": 0, "Bronze": 1, "Total": 1},
    {"Rank": 71, "Nation": "Chile", "Gold": 0, "Silver": 0, "Bronze": 1, "Total": 1},
    {"Rank": 72, "Nation": "Ecuador", "Gold": 0, "Silver": 0, "Bronze": 1, "Total": 1},
    {"Rank": 73, "Nation": "Great Britain", "Gold": 0, "Silver": 0, "Bronze": 1, "Total": 1},
    {"Rank": 74, "Nation": "San Marino", "Gold": 0, "Silver": 0, "Bronze": 1, "Total": 1},
    {"Rank": 75, "Nation": "Syria", "Gold": 0, "Silver": 0, "Bronze": 1, "Total": 1},
    {"Rank": 76, "Nation": "United World Wrestling[c]", "Gold": 0, "Silver": 0, "Bronze": 1, "Total": 1}
]

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.olympics
collection = db.medal_tally

# Clear the collection before inserting new data
collection.delete_many({})

# Insert data
collection.insert_many(data)

# Verify the data insertion
for doc in collection.find():
    print(doc)
