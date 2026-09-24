from pymongo.mongo_client import MongoClient
import pandas as pd

import json

uri="mongodb+srv://bhageshsharma777_db_user:oL05ETjp0HTDe6Bv@cluster0.t2vd1tm.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)

DATABASE_NAME = "pwskils"
COLLECTION_NAME = "waferfault"

df = pd.read_csv("C:\Users\hp\sensorproject1\notebooks\wafer_23012020_041211.csv")
df = df.drop("Unnamed: 0",axis=1)

json_record = list(json.loads(df.T.to_json()).values())
json_record

client[DATABASE_NAME][COLLECTION_NAME ].insert_many(json_record)