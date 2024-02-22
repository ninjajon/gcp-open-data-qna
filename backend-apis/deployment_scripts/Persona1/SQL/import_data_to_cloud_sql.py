# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import TypedDict
from google.cloud.sql.connector.connector import Connector
import sqlalchemy
import random

PROJECT_ID = "rl-llm-dev"
REGION = "us-central1"
INSTANCE_NAME = "csm-database"
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}" # i.e demo-project:us-central1:demo-instance
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "root"
DB_PASS = ''
DB_NAME = "csm"

# initialize Connector object
connector = Connector()

class InsertDict(TypedDict):
    id: int
    title: str
    description: str
    image: str
    features: str
    categories: str
    price: float
    quantity: int

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

create_sql = ""
insert_sql = ""
recommendations_products_jsonl = []
search_products_jsonl = []

with open("./create_tables.sql", "r") as f:
    create_sql = f.read()


with open("./insert.sql", "r") as f:
    insert_sql = f.read()

with open("./recommendation_products_full.jsonl", "r") as f:
    recommendations_products_jsonl = f.readlines() 

with open("./search_products.jsonl", "r") as f:
    search_products_jsonl = f.readlines() 

# connect to connection pool
with pool.connect() as db_conn:
    # create ratings table in our sandwiches database
    # db_conn.execute(sqlalchemy.text(create_sql))

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    # db_conn.commit()

    # insert data into our ratings table
    insert_stmt = sqlalchemy.text(insert_sql)
    
    for search_json, rec_json in zip(
        search_products_jsonl, recommendations_products_jsonl) :
        search_dict = json.loads(search_json)
        rec_dict = json.loads(rec_json)
        if (search_dict["id"] != rec_dict["id"]):
            raise Exception("different ids")
        id = int(search_dict["id"])
        if search_dict["id"] == 0:
            id = 1000

        print(search_dict["id"])
        
        search_data_dict = json.loads(search_dict["jsonData"])
        rec_data_dict = json.loads(rec_dict["jsonData"])
        insert_dict: InsertDict = {
            "id": id,
            "title": search_data_dict["title"],
            "description": search_data_dict["description"],
            "image": rec_data_dict["images"][0]["uri"],
            "features": "",
            "categories": str(rec_data_dict["categories"]),
            "price": 100.00,
            "quantity": 100
        }

        # insert entries into table
        db_conn.execute(insert_stmt, parameters=insert_dict)

    # commit transactions
    db_conn.commit()

