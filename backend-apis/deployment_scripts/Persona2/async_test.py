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

import asyncio
import aiohttp
import requests
from vertexai.vision_models import ImageCaptioningModel, Image
imagen_model = ImageCaptioningModel.from_pretrained("imagetext")

from dataclasses import dataclass
import functools

@dataclass
class ProductCategories:
    images_uri: list

data = ProductCategories(
    images_uri=[
        "https://storage.googleapis.com/csm-dataset/website-search/image_00.jpg",
    ]
)


async def get_image_captions(uri: str) -> str:
    loop = asyncio.get_running_loop()
    captions = await loop.run_in_executor(
        None,
        functools.partial(
            imagen_model.get_captions,
                image=Image(image_bytes=requests.get(uri).content),
                number_of_results=1,
                language="en")
        )
    return captions


async def run_image_captions():
    tasks = [get_image_captions(uri) for uri in data.images_uri]
    results = await asyncio.gather(*tasks)
    return results


results = asyncio.run(run_image_captions())
print(results)




