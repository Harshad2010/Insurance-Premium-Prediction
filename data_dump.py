import pymongo
import pandas as pd
import json


client = pymongo.MongoClient("mongodb+srv://harsh:ghalwa1%40@cluster0.uvzkent.mongodb.net/?retryWrites=true&w=majority")
db = client.test
DATA_FILE_PATH = "D:\DS from PC\pc-20230117T113640Z-001\pc\Projects\Insurance premium prediction\Insurance-Premium-Prediction\insurance.csv"
DATABASE_NAME = "INSURANCE"
COLLECTION_NAME = "INSURANCE PROJECT"

if __name__ == '__main__':
    df = pd.read_csv(DATA_FILE_PATH)
    print(f'Rows and Columns: {df.shape}')
    
    df.reset_index(drop=True, inplace=True) #drop the index column
    
    #Mongo Db takes data in key value pair
    #We transpose the data for that
    json_record = list(json.loads(df.T.to_json()).values()) #-----check
    print(json_record[0])
    
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record) #data is inserted in MongoDB 