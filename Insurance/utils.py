import pandas as pd
import numpy as np
import os
import sys
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
from Insurance.logger import logging



def get_collection_as_dataframe(database_name: str, collection_name :str)->pd.DataFrame:
    
    try:
        logging.info(f"Reading data from database : {database_name} and collection :{collection_name}")
        #mong_obj = list(mongo_client[database_name][collection_name].find())
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f'Columns in df are :{df.columns}')
        if '_id' in df.columns :
            logging.info('Dropping column _id')
            df =df.drop('_id',axis=1)
        logging.info(f'Number of rows and columns in df : {df.shape}')
        return df
        
        
    except Exception as e:
        raise InsuranceException(e,sys)
        