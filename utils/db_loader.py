import logging
import os
import sys
current_path = os.path.abspath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(root_path)
from handlers.MongoDBHandler import MongoDBHandler
from config import MONGODB_PROCESSED_COLLECTION


def load_to_mongodb(documents: list):
    '''
    Loads the data into the MongoDB database.
    :param documents: List of documents containing at least 'article_links' key.
    '''
    try:
        mongodb_handler = MongoDBHandler(MONGODB_PROCESSED_COLLECTION)
        
        if documents:
            mongodb_handler.insert_data(documents)

        mongodb_handler.close_connection()
        logging.info(f"Attempted to load {len(documents)} records into the database.")

    except Exception as ex:
        logging.error(f"Error while loading to MongoDB: {ex}")