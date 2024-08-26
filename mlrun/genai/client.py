# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Union

import requests

from mlrun.genai.config import config, logger
from mlrun.genai.schemas import ChatSession, Project, Workflow
from mlrun.utils.helpers import dict_to_json


class Client:
    def __init__(self, base_url, username=None, token=None):
        self.base_url = base_url
        self.username = username or "guest"
        self.token = token

    def post_request(
        self, path, data=None, params=None, method="GET", files=None, json=None
    ):
        # Construct the URL
        url = f"{self.base_url}/api/{path}"
        kw = {
            key: value
            for key, value in (
                ("params", params),
                ("data", data),
                ("json", json),
                ("files", files),
            )
            if value is not None
        }
        if data is not None:
            kw["data"] = dict_to_json(kw["data"])
        if params is not None:
            kw["params"] = (
                {k: v for k, v in params.items() if v is not None} if params else None
            )
        # Make the request
        logger.debug(
            f"Sending {method} request to {url}, params: {params}, data: {data}"
        )
        response = requests.request(
            method,
            url,
            headers={"x_username": self.username},
            **kw,
        )

        # Check the response
        if response.status_code == 200:
            # If the request was successful, return the JSON response
            return response.json()
        else:
            # If the request failed, raise an exception
            response.raise_for_status()

    def get_collection(self, name):
        response = self.post_request(f"collection/{name}")
        return response["data"]

    def get_session(self, uid: str, user_name: str):
        response = self.post_request(f"users/{user_name}/sessions/{uid}")
        return response["data"]

    def get_user(self, username: str = "", email: str = None):
        params = {}
        if email:
            params["email"] = email
        response = self.post_request(f"users/{username}", params=params)
        return response["data"]

    def create_session(
        self,
        name,
        user_id,
        username=None,
        workflow_id=None,
        history=None,
    ):
        chat_session = {
            "name": name,
            "owner_id": user_id,
            "workflow_id": workflow_id,
            "history": history or [],
        }
        response = self.post_request(
            f"users/{username}/sessions", data=chat_session, method="POST"
        )
        return response

    def update_session(
        self,
        chat_session: ChatSession,
        username: str,
        history=None,
    ):
        chat_session.history = history or []
        response = self.post_request(
            f"users/{username}/sessions/{chat_session.name}",
            data=chat_session.to_dict(),
            method="PUT",
        )
        return response["success"]

    def get_project(self, project_name: str):
        response = self.post_request(f"projects/{project_name}")
        return Project(**response["data"])

    def create_workflow(self, project_name: str, workflow: Union[Workflow, dict]):
        project_id = client.get_project(project_name=project_name).uid
        if isinstance(workflow, dict):
            workflow["project_id"] = project_id
            graph = workflow.pop("graph", None)
            workflow = Workflow(**workflow)
            workflow.add_graph(graph)
        response = self.post_request(
            f"projects/{project_name}/workflows", method="POST", data=workflow.to_dict()
        )
        return Workflow(**response["data"])

    def get_workflow(
        self, project_name: str, workflow_name: str = None, workflow_id: str = None
    ):
        if workflow_id:
            response = self.post_request(
                f"projects/{project_name}/workflows/{workflow_id}"
            )["data"]
        else:
            response = self.post_request(
                f"projects/{project_name}/workflows", params={"name": workflow_name}
            )
            if not response["data"]:
                return None
            response = response["data"][0]
        return Workflow(**response)

    def update_workflow(self, project_name: str, workflow: Workflow):
        print(workflow.to_dict())
        response = self.post_request(
            f"projects/{project_name}/workflows/{workflow.uid}",
            data=workflow.to_dict(),
            method="PUT",
        )
        return Workflow(**response["data"])


client = Client(base_url=config.api_url)
