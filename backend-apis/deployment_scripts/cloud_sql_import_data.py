# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Upload data to Cloud Sql

pip install sqlalchemy google-cloud-sql
"""

import json
import random
from typing import TypedDict

import sqlalchemy
from google.cloud.sql.connector.connector import Connector

PROJECT_ID = "rl-llm-dev"
REGION = "us-central1"
INSTANCE_NAME = "csm-database"
# i.e demo-project:us-central1:demo-instance
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "root"
DB_PASS = ""
DB_NAME = "csm"

# initialize Connector object
connector = Connector()


class ProductDict(TypedDict):
    """A dict representing a product"""

    id: int
    title: str
    description: str
    image: str
    features: str
    categories: str
    price: float
    quantity: int
    owner: str
    featured: bytes


# function to return the database connection object
def getconn():
    """Funtion to return the dabase connection Object.

    Returns:
        Cloud Sql connection object

    """
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )
    return conn


# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

recommendations_products_jsonl = []

with open("./create_tables.sql", "r", encoding="utf-8") as f:
    create_sql = f.read()


with open("./dataset/insert.sql", "r", encoding="utf-8") as f:
    insert_sql = f.read()

with open(
    "./dataset/recommendation_products.jsonl", "r", encoding="utf-8"
) as f:
    recommendations_products_jsonl = f.readlines()

# connect to connection pool
with pool.connect() as db_conn:
    # create ratings table in our sandwiches database
    # db_conn.execute(sqlalchemy.text(create_sql))

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    # db_conn.commit()

    # insert data into our ratings table
    insert_stmt = sqlalchemy.text(insert_sql)

    for rec_json in recommendations_products_jsonl:
        rec_dict = json.loads(rec_json)

        print(rec_dict["id"])
        insert_dict: ProductDict = {
            "id": int(rec_dict["id"]),
            "title": rec_dict["title"],
            "description": rec_dict["description"],
            "image": rec_dict["images"][0]["uri"],
            "features": "",
            "categories": rec_dict["categories"],
            "price": rec_dict["priceInfo"]["price"],
            "quantity": rec_dict["availableQuantity"],
            "owner": "system",
            "featured": b"1" if random.random() > 0.95 else b"0",
        }

        # insert entries into table
        db_conn.execute(insert_stmt, parameters=insert_dict)

    # commit transactions
    db_conn.commit()
