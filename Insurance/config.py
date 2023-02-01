import pymongo
import pandas as pd
import numpy as np
import json
import os
import sys
from dataclasses import dataclass



@dataclass
class EnvironmentVariable:
    #MONGO_DB_URL = "mongodb+srv://harsh:ghalwa1%40@cluster0.uvzkent.mongodb.net/?retryWrites=true&w=majority"
    mongo_db_url = os.getenv('MONGO_DB_URL')
    
 #Define Mongo variable and client   
env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = 'expenses'
print(mongo_client)
print('env_var, mongo_db_url')





