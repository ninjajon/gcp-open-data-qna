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

import functions_framework

@functions_framework.http
def cleanup_salesforce(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request)
    Returns:
        200 if success
    """
    from simple_salesforce import Salesforce

    security_token = "jxjXKDnPToPysPf3Eh61TKg7q"
    username = "support@cymbal.services"
    password = "GoogleCloud2024!"
    instance_url = "google-17b-dev-ed.develop.lightning.force.com"

    sf = Salesforce(
        username=username,
        password=password,
        security_token=security_token,
        instance_url=instance_url
    )

    # delete cases
    cases = sf.query("SELECT Id FROM Case")
    cases_ids = []
    for i in dict(cases)["records"]:
        cases_ids.append({"Id":dict(i)["Id"]})

    if cases_ids:
        sf.bulk.Case.hard_delete(cases_ids)

    # delete files
    documents = sf.query("SELECT Id FROM ContentDocument")
    documents_ids = []
    for i in dict(documents)["records"]:
        documents_ids.append({"Id":dict(i)["Id"]})

    if documents_ids:
        sf.bulk.ContentDocument.hard_delete(documents_ids)

    return "200"