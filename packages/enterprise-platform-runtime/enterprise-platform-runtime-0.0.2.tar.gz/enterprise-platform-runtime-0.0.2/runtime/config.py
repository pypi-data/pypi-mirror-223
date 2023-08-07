import base64
import gzip
import json
import os
from typing import Any, Optional

import httpx
from cloudpickle import cloudpickle
from pydantic import BaseModel

from .package import Package
from .utils import render_for_platform


class Config(BaseModel):
    platform_core_private_api_host: str = os.environ.get(
        "PLATFORM_CORE_PRIVATE_API_HOST"
    )

    execution_id: str
    scope: str
    node_id: str
    index: Optional[int] = None
    package_object_id: str
    input_object_id: str
    output_object_id: str

    input: Optional[Any] = None
    method: Optional[Any] = None
    package: Optional[Package] = None

    @classmethod
    def from_environment(cls):
        instance = cls(
            scope=os.environ["SCOPE"],
            execution_id=os.environ["EXECUTION_ID"],
            node_id=os.environ["NODE_ID"],
            index=os.environ.get("INDEX"),
            package_object_id=os.environ["PACKAGE_OBJECT_ID"],
            input_object_id=os.environ["INPUT_OBJECT_ID"],
            output_object_id=os.environ["OUTPUT_OBJECT_ID"],
        )
        instance._download_package()
        instance._prepare_method()
        return instance

    def _execute(self, path: str, data: dict):
        response = httpx.post(
            f"{self.platform_core_private_api_host}/{path}",
            json={**data, "tenant_id": "compute"},
        )
        response.raise_for_status()
        return response.json()

    def _download_object(self, object_id: str):
        object_data = self._execute(
            "objects/get_object",
            {"object_id": object_id},
        )
        object_bytes = httpx.get(object_data["get_url"]).content
        return json.loads(gzip.decompress(object_bytes).decode("utf-8"))

    def _download_package(self):
        self.package = Package(**self._download_object(self.package_object_id))

    def download_input_data(self):
        try:
            return self._download_object(self.input_object_id)
        except gzip.BadGzipFile:
            return None

    def _prepare_method(self):
        method_base64 = self.package.get_node(self.node_id).method
        self.method = cloudpickle.loads(base64.b64decode(method_base64))

    def run(self, input_data: Any):
        return self.method(input_data) if callable(self.method) else self.method

    def upload_output_data(self, data: dict):
        try:
            # By calling `iter` on the data object we check to see
            # if it is iterable. If not a TypeError will be raised.
            iter(data)
            data_length = len(data)
        except TypeError:
            data_length = 1

        object_ = self._execute(
            "objects/get_object_for_upload",
            data={
                "object_id": self.output_object_id,
                "object_type": "JSON",
                "data_length": data_length,
            },
        )

        return httpx.post(
            object_["post_data"]["url"],
            data=object_["post_data"]["fields"],
            files={"file": gzip.compress(json.dumps(data).encode("utf-8"))},
        )

    def _submit_event(self, data: dict):
        self._execute(
            "events/submit_events",
            {"events": [data]},
        )

    def get_event_data(self):
        return self.dict(
            include={
                "execution_id",
                "scope",
                "node_id",
                "index",
                "package_object_id",
                "input_object_id",
                "output_object_id",
            }
        )

    def report_success(self):
        self._submit_event(
            {
                "name": "COMPUTE_EXECUTION_SUCCEEDED",
                "scopes": [self.scope],
                "channel": f"compute::execution::{self.execution_id}",
                "data": render_for_platform(self.get_event_data()),
            }
        )

    def report_failure(self, error: Exception):
        self._submit_event(
            {
                "name": "COMPUTE_EXECUTION_FAILED",
                "scopes": [self.scope],
                "channel": f"compute::execution::{self.execution_id}",
                "data": render_for_platform(
                    {
                        **self.get_event_data(),
                        "error": str(error),
                    }
                ),
            },
        )
