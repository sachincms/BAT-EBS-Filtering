import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pymongo
import logging
import os
import sys
current_path = os.path.abspath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(root_path)
from handlers.MongoDBHandler import MongoDBHandler
from config import MONGODB_SCRAPED_COLLECTION, MONGODB_PROCESSED_COLLECTION


def retrieve():
    '''
    Accesses the MongoDB database and returns a list of existing documents.
    '''

    try:
        mongodb_handler_scraped = MongoDBHandler(MONGODB_SCRAPED_COLLECTION)
        mongodb_handler_processed = MongoDBHandler(MONGODB_PROCESSED_COLLECTION)
        
        latest_date_doc = mongodb_handler_processed.read_data(query={}, sort=[('scraped_date', pymongo.DESCENDING)], limit=1)
        start_date = latest_date_doc[0]['scraped_date']
        #start_date = datetime.strptime("01/01/2023", "%d/%m/%Y")        
        end_date = datetime.today()
        

        query = {
            'scraped_date': {
                '$gt': start_date,
                '$lte': end_date
            }
        }

        scraped_documents = mongodb_handler_scraped.read_data(query)

        mongodb_handler_scraped.close_connection()
        mongodb_handler_processed.close_connection()

    except Exception as ex:
        logging.error(ex)
    
    return scraped_documents
