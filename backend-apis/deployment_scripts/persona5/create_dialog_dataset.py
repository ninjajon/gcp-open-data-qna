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

from time import sleep
import random
import json
from vertexai.preview.language_models import TextGenerationModel

model = TextGenerationModel.from_pretrained("text-bison")

sentiments = [("positive",4,5), ("negative",1,3), ("neutral",2,4), ("positive",4,5)]
resolved = ["was resolved", "was not resolved"]

customer_wants = [
    "ask simple questions about products or services",
    "get help with troubleshooting",
    "get updates on their order status",
    "track returns",
    "submit complaints or feedback",
    "cancel subscriptions",
    "attach documents or screenshots to help explain their issue",
    "get updates on orders and promotions",
    "download manuals and other documents about the product",
    "request a return of the product",
    "request an exchange of the product"
]

prompt = """Create a simulated conversation (dialog) between a support agent and a customer of Cymbal Furniture online store. Use the product title and description below to help create the conversation.
The conversation must be natural and use informal tone.
The customer wants to {} and the agent must help the customer. The dialog have at least 5 interactions.
At the end of conversation the case {} and the overall sentiment of the customer is {}.
Product title: {}
Product description: {}

Output:"""

with open("./recommendation_products.jsonl", "r") as f:
    products = f.readlines()


def generate_dialog(
        customer_wants,
        resolved,
        sentiment,
        title,
        description
):
    return model.predict(
        prompt=prompt.format(
            i,
            resolved,
            sentiment[0],
            title,
            description
        ),
        max_output_tokens=1024
    ).text


with open("./service_conversations.jsonl", "a") as f:
    count = 0
    for product in products:
        print(count)
        product = json.loads(product)
        title = product["title"]
        description = product["description"]
        category = product["categories"]
        id = product["id"]

        for i in customer_wants:
            for resolved in ["was resolved", "was not resolved"]:
                sentiment = random.choice(sentiments)
                stars = random.randint(sentiment[1], sentiment[2])
                
                passou = False
                while not passou:
                    try:
                        dialog = generate_dialog(
                                i,
                                resolved,
                                sentiment[0],
                                title,
                                description
                        )
                    except Exception as e:
                        print(e)
                        print("Retrying in 5 seconds ...")
                        sleep(5)
                    else:
                        passou = True
                payload = {
                    "id": id,
                    "title": title,
                    "description": description,
                    "category": category,
                    "dialog": dialog,
                    "sentiment": sentiment[0],
                    "stars": stars
                }
                f.write(json.dumps(payload) + "\n")
        sleep(6)
        count += 1

