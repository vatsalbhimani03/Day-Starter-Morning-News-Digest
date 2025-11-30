# check MongoDB Atlas connectivity & sample_mflix read test.
from pymongo import MongoClient
from config import MONGODB_CONN 

def main():
    if not MONGODB_CONN:
        raise RuntimeError("MONGODB_CONNECTION_STRING is empty. Please check it in your environment.")

    # Connect and ping
    client = MongoClient(MONGODB_CONN, serverSelectionTimeoutMS=5000)
    ping = client.admin.command("ping")
    print("Ping OK? (DB Connected)", ping.get("ok") == 1)

    # Use the sample dataset db (sample_mflix) and movies collection
    db = client["sample_mflix"]
    movies = db["movies"]

    # display a few collections
    print("Collections (first 5):", db.list_collection_names()[:5])

    # display few field of one movie
    one = movies.find_one({}, {"_id": 0, "title": 1, "year": 1, "imdb.rating": 1})
    print("One movie:", one)

    # display five movies by year
    print("Five recent movies:")
    for m in movies.find({}, {"_id": 0, "title": 1, "year": 1}).sort("year", -1).limit(5):
        print(f"   {m.get('year')}: {m.get('title')}")

if __name__ == "__main__":
    main()
