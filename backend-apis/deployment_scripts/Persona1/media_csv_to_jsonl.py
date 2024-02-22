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

import csv
import json

with open("media-dataset.csv", "r") as csv_file:
    with open("media-dataset.jsonl", "w") as jsonl_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        head = []

        for row in csv_reader:
            if not head:
                head = row
            else:
                row_dict = dict(zip(head, row))
                data = {}
                data["id"] = row_dict["id"]
                data["schemaId"] = row_dict["schemaId"]
                del row_dict["id"]
                del row_dict["schemaId"]
                row_dict["images"] = [{
                    "uri": row_dict["images.uri"],
                    "name": row_dict["images.uri"].split("/")[-1]}]
                row_dict["categories"] = [row_dict["categories"]]
                del row_dict["images.uri"]
                data["jsonData"] = json.dumps(row_dict)
                jsonl_file.write(json.dumps(data) + "\n")


