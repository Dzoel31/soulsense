# Controller for Mongo DB

from pymongo.mongo_client import MongoClient
from pymongo import errors
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import time

load_dotenv(verbose=True)

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

uri = f"mongodb+srv://{USER}:{PASSWORD}@soulsense.tebvzax.mongodb.net/?retryWrites=true&w=majority&appName=soulsense"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client['soulsense']
# get data from database
def get_data_sensor():
    collection = db['heart_rate']
    data = collection.find()
    data_list = []
    for d in data:
        d['_id'] = str(d['_id'])
        data_list.append(d)
    return data_list

# store data from sensor
def store_data(data):
    collection = db['heart_rate']
    data_sensor = {
        'value': '',
        'level': '',
        'time': '',
    }
    data['time'] = time.time()
    data_sensor['value'] = data['value']
    data_sensor['level'] = data['level']
    data_sensor['time'] = data['time']
    try:
        collection.insert_one(data_sensor)
    except errors.ServerSelectionTimeoutError as err:
        print(err)
    return True

def delete_all_data():
    '''
    Delete all data from the database to prevent storage overflow
    '''
    collection = db['heart_rate']
    collection.delete_many({})
    return True