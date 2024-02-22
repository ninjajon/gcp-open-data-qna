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
from time import sleep
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput

model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

with open("./vertexai_search_reviews.jsonl", "r") as f:
    lines = f.readlines()
    lines = [json.loads(i) for i in lines]

results = []

for i, line in enumerate(lines):
    print("processing " + str(i))
    text_input = TextEmbeddingInput(
        text=json.loads(line["jsonData"])["review"],
        task_type="CLUSTERING")

    embedding = model.get_embeddings(texts=[text_input])[0].values

    results.append({
        "id": line["id"],
        "embedding": embedding
    })

    if i%80 == 0: 
        print("sleeping 5 secs")
        sleep(10)


with open("vertexai_reviews_embeddings.jsonl", "a") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")
