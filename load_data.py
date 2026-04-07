#from MongoDB docs
import pandas as pd
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://dluzano2:nDspug5Gr3FE04TW@hw3.iukqnly.mongodb.net/?appName=hw3"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["ev_db"]
collection = db["vehicles"]

# Read CSV with pandas 
df = pd.read_csv("Electric_Vehicle_Population_Data.csv", dtype_backend="numpy_nullable")

# Convert date columns
# df["orderDate"] = pd.to_datetime(df["orderDate"], errors="coerce")

# Convert to list of dicts and insert
records = df.where(pd.notna(df), None).to_dict(orient="records")

BATCH_SIZE = 1000
for i in range(0, len(records), BATCH_SIZE):
    batch = records[i:i + BATCH_SIZE]
    result = collection.insert_many(batch, ordered=False)
    print(f"Inserted {len(result.inserted_ids)} records (batch {i // BATCH_SIZE + 1})")

print(f"Total records: {len(records)}")
client.close()
