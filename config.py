import os
import sys
sys.path.append('.')
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
MONGODB_SCRAPED_COLLECTION = os.getenv('MONGODB_SCRAPED_COLLECTION')
MONGODB_PROCESSED_COLLECTION = os.getenv('MONGODB_PROCESSED_COLLECTION')