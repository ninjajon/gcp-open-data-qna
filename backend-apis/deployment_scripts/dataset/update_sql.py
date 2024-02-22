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
import random
from typing import TypedDict

import sqlalchemy
from google.cloud.sql.connector.connector import Connector

PROJECT_ID = "genai-for-csm"
REGION = "us-central1"
INSTANCE_NAME = "csm-instance"
# i.e demo-project:us-central1:demo-instance
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "root"
DB_PASS = 'GoogleCloud2024!'
DB_NAME = "csm"

# initialize Connector object
connector = Connector()

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

sql_statement = "UPDATE products SET price = :price, quantity = :quantity WHERE id = :id"

with open("./recommendation_products.jsonl") as f:
    lines = f.readlines()
    lines = [json.loads(i) for i in lines]

# connect to connection pool
with pool.connect() as db_conn:
    # create ratings table in our sandwiches database
    # db_conn.execute(sqlalchemy.text(create_sql))

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    # db_conn.commit()
    # insert data into our ratings table
    update_stmt = sqlalchemy.text(sql_statement)

    for i in lines:
        update_dict = {
            "price": float(i["priceInfo"]["price"]),
            "quantity": i["availableQuantity"],
            "id": int(i["id"])
        }

        # insert entries into table
        db_conn.execute(update_stmt, parameters=update_dict)

    # commit transactions
    db_conn.commit()  