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


sentiments = [("positive",4,5), ("negative",1,3), ("neutral",2,4), ("positive",4,5)]
model = TextGenerationModel.from_pretrained("text-bison")

review_prompt_1 = """<Instructions>
The text below is a product title and description.
You are a customer of Cymbal and you need to write a {} review talking about your experience with the product. Be polite, informal and succinct.
</Instructions>
<ProductDescription>
Product title: {}
Product description: {}
</ProductDescription>
<Output>"""

review_prompt_2 = """The text below is a product title and description for a product you just bought.
Write a {} review for the website talking about your experience with the product. Use one sentence, be polite and formal.
Product title: {}
Product description: {}
output:"""

review_prompt_3 = """Create a {} review for Cymbal retailer website talking about your experience with the product below. Be polite, informal and succinct.
Write the review in one sentence.
Product title: {}
Product description: {}
output:"""

review_prompt_4 = """Write a {} review for a website talking about the product below.
Write the review in one sentence and use a formal tone.
Product title: {}
Product description: {}
output:"""

review_prompt_5 = """Create a short {} review for a website talking about the product below, in one sentence.
You are a long time customer and you already had many interactions with this website.
Product title: {}
Product description: {}
output:"""

review_prompt_6 = """Create a {} review for the product below in one sentence. Be succinct. Use an informal tone.
Product title: {}
Product description: {}
output:"""

review_prompt_7 = """Create a {} review in one sentence for a website talking about the product below. Be honest and use nice words.
Product title: {}
Product description: {}
output:"""

review_prompt_8 = """The text below is related to a product in a retailer website called Cymbal.
Create a {} review for a retail website talking about your experience with the product. Be succinct and use only once sentence.
Remember this is your first buy in this website and you are new to the platform.
Product title: {}
Product description: {}
output:"""

review_prompt_9 = """The text below is related to a product sold by Cymbal retailer website.
In one sentence, create a review in one sentence talking about your {} experience with the product. Use a formal tone.
Title: {}
Description: {}
output:"""

review_prompt_9 = """You are a long time customer of Cymbal retail online store.
Create a {} review of the product below talking about the experience with it, in one sentence.
Product title: {}
Product description: {}
output:"""

review_prompt_10 = """You are a customer who just bought a product. Create a review talking about your {} interaction with the product in one sentence.
Be nice, but honest.
Product title: {}
Product description: {}
output:"""

prompts = [review_prompt_1, review_prompt_2, review_prompt_3, review_prompt_4, review_prompt_5, review_prompt_6, review_prompt_7, review_prompt_8, review_prompt_9, review_prompt_10]


reviews = []

with open("./recommendation_products.jsonl", "r") as f:
    products = f.readlines()


with open("./product_reviews.jsonl", "a") as f:
    i=0
    for product in products:
        print(i)
        product = json.loads(product)
        title = product["title"]
        description = product["description"]
        category = product["categories"]
        id = product["id"]

        for prompt in prompts:
            sentiment = random.choice(sentiments)
            stars = random.randint(sentiment[1], sentiment[2])
            review = model.predict(
                prompt=prompt.format(
                    sentiment[0],
                    title,
                    description
                )
            ).text
            payload = {
                "id": id,
                "title": title,
                "description": description,
                "category": category,
                "review": review,
                "sentiment": sentiment[0],
                "stars": stars
            }
            f.write(json.dumps(payload) + "\n")
        sleep(3)
        i+=1