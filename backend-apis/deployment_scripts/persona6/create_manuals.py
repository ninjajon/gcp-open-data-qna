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
with open("./new_search_conversations.jsonl") as f:
    conversations = f.readlines()
    conversations = [json.loads(i) for i in conversations]

conversations_set = set()
products = []

for i in conversations:
    data = json.loads(i["jsonData"])
    if data["product_id"] in conversations_set:
        continue

    conversations_set.add(data["product_id"])
    products.append(
        {
            "id":data["product_id"],
            "jsonData": data
        }
    )

for i, _ in enumerate(products):
    del products[i]["jsonData"]["sentiment"]
    del products[i]["jsonData"]["status"]
    del products[i]["jsonData"]["customer_id"]
    del products[i]["jsonData"]["customer_email"]
    del products[i]["jsonData"]["agent_id"]
    del products[i]["jsonData"]["agent_email"]
    del products[i]["jsonData"]["product_id"]
    del products[i]["jsonData"]["conversation"]
    del products[i]["jsonData"]["rating"]

prompt = """Using the product title and description below, write a product manual (user guide) that includes the following sections and chapters.
product title: {}
product description: {}

Sections of the manual:
 - Introduction: Briefly introduce the product, its intended audience, and what it can do.
 - Table of contents: This will help users navigate the manual and find the information they need quickly.
 - Safety precautions and warnings: Clearly outline any potential hazards associated with the product and how to avoid them.
 - Getting started (setup and how to use): This section should provide step-by-step instructions on how to set up and use the product for the first time.
 - Product features: Explain the different features of the product in detail, including how to use them and what they are for.
 - Troubleshooting: Provide solutions to common problems that users might encounter.
 - Maintenance and care: Explain how to clean and care for the product to extend its lifespan.
 - Appendix: Include any additional information that users might find helpful, such as warranty information, contact information for customer support, or a glossary of terms.

Additional sections:
 - Assembly instructions: If the product requires assembly, provide clear and concise instructions with diagrams.
 - Technical specifications: List the technical specifications of the product, such as its dimensions, weight, power requirements, etc.
 - Compliance information: If the product needs to comply with any specific regulations, include information about that in the manual.

Tips for writing a comprehensive product manual:
 - Use clear and concise language that is easy for your target audience to understand.
 - Chunk the information into small, easy-to-read sections with headings and subheadings.
 - Use a table of contents and index to make it easy for users to find the information they need.
By following these guidelines, you can create a comprehensive and user-friendly product manual that will help your users get the most out of your product.

output:"""


from vertexai.preview.generative_models import GenerativeModel

def generate(input_text: str):
  model = GenerativeModel("gemini-pro")
  responses = model.generate_content(
    contents=input_text,
    generation_config={
        "max_output_tokens": 8192,
        "temperature": 0.8,
        "top_p": 1,
        "top_k": 40
    }
  )
  return responses


for i,product in enumerate(products):
    print(i)
    manual = generate(
        input_text=prompt.format(product["jsonData"]["title"], product["jsonData"]["description"])
    )
    try:
        manual = manual.candidates[0].content.parts[0].text # type: ignore
    except:
        manual = "No manual provided by the manufacturer."
        print(product["id"])
    
    products[i]["jsonData"]["manual"] = manual


with open("./manuals_dataset.jsonl", "a") as f:
    for i in products:
        f.write(json.dumps(i) + "\n")
