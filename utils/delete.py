from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
current_path = os.path.abspath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(root_path)
from config import MONGODB_URI, MONGODB_DATABASE, CONTENT_UNAVAILABLE_MESSAGE


def delete_unavailable_content(collection_name):
    client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    db = client[MONGODB_DATABASE]
    collection = db[collection_name]

    query = {
        'title': CONTENT_UNAVAILABLE_MESSAGE,
        'text': CONTENT_UNAVAILABLE_MESSAGE
    }

    result = collection.delete_many(query)

    print(f"Deleted {result.deleted_count} documents where title and text are '{CONTENT_UNAVAILABLE_MESSAGE}'.")

    client.close()

if __name__ == "__main__":
    delete_unavailable_content('scraped_data')