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
Upload reviews to Firestore

pip install google-cloud-firestore
"""

import asyncio
import json
from typing import Literal, TypedDict

from google.cloud import firestore

firestore_client = firestore.AsyncClient()


class ReviewDoc(TypedDict):
    """A dict representing a review document for Firestore"""

    review: str
    sentiment: Literal["positive", "negative", "neutral"]
    stars: int


async def review_upload(product_id: str, review: ReviewDoc):
    """Uploads a single review

    Args:
        product_id:
        review:
    """
    await firestore_client.collection("website_reviews").document(
        product_id
    ).collection("reviews").document().set(review)


async def upload_reviews(review_docs: dict[str, list[ReviewDoc]]):
    """Upload reviews"""
    await asyncio.gather(
        *(
            review_upload(product_id, review)
            for product_id, reviews in review_docs.items()
            for review in reviews
        )
    )


async def main():
    """Main Function"""
    with open("dataset/product_reviews.jsonl", "r", encoding="utf-8") as f:
        reviews_jsonl = f.readlines()
    review_docs: dict[str, list[ReviewDoc]] = {}
    for review_json in reviews_jsonl:
        review_dict = json.loads(review_json)
        review_doc: ReviewDoc = {
            "review": review_dict["review"],
            "sentiment": review_dict["sentiment"],
            "stars": review_dict["stars"],
        }
        if review_dict["id"] not in review_docs:
            review_docs[review_dict["id"]] = []
        review_docs[review_dict["id"]].append(review_doc)

    await upload_reviews(review_docs)


if __name__ == "__main__":
    asyncio.run(main())
