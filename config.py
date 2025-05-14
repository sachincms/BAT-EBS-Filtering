import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
sys.path.append(parent_directory)
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
MONGODB_SCRAPED_COLLECTION = os.getenv('MONGODB_SCRAPED_COLLECTION')
MONGODB_PROCESSED_COLLECTION = os.getenv('MONGODB_PROCESSED_COLLECTION')
MONGODB_UNIQUE_KEY = os.getenv('MONGODB_UNIQUE_KEY')

CONTENT_UNAVAILABLE_MESSAGE = "Content unavailable"