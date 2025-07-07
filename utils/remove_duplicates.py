from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
current_path = os.path.abspath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(root_path)
from config import MONGODB_URI, MONGODB_DATABASE

def remove_duplicates(collection_name, unique_key='article_links'):
    client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    db = client[MONGODB_DATABASE]
    collection = db[collection_name]

    seen_links = set()
    duplicates_to_delete = []

    for idx, doc in enumerate(list(collection.find({}, {unique_key: 1}))):
        print(idx)
        link = doc.get(unique_key)
        if link is None:
            continue

        if link in seen_links:
            duplicates_to_delete.append(doc['_id'])
        else:
            seen_links.add(link)

    if duplicates_to_delete:
        result = collection.delete_many({'_id': {'$in': duplicates_to_delete}})
        print(f"Deleted {result.deleted_count} duplicate documents.")
    else:
        print("No duplicates found.")

    client.close()

if __name__ == "__main__":
    remove_duplicates('processed_data')