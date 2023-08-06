# Copyright 2022 Google LLC
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

from typing import Any, Dict, List, Optional, Set, Sequence, Iterator
from dataclasses import dataclass

import json

from google.ads.googleads.client import GoogleAdsClient  # type: ignore
from importlib import import_module
import re
from proto.primitives import ProtoType


@dataclass
class Field:
    name: str
    type: str
    values: Set[str]


def clean_resource(resource: str) -> str:
    return resource.title().replace('_', '')


class BaseClient:

    def __init__(self, version: str = "v14"):
        self.api_version = version
        self.google_ads_row = self._get_google_ads_row(version)

    def get_response_batch(self, customer_id: str, query: str) -> Iterator[dict]:
        ...

    def _get_google_ads_row(self, api_version: str) -> "GoogleAdsRow":
        base_module = f"google.ads.googleads.{api_version}"
        google_ads_service = import_module(
            f"{base_module}.services.types.google_ads_service")
        return google_ads_service.GoogleAdsRow()

    def infer_types(self, fields: Sequence[str]) -> List[Any]:
        """Maps API fields to Python primitives."""

        base_module = f"google.ads.googleads.{self.api_version}"
        common_types_module = f"{base_module}.common.types"
        segments = import_module(f"{common_types_module}.segments")
        metrics = import_module(f"{common_types_module}.metrics")

        mapping = {"INT64": int, "FLOAT": float, "DOUBLE": float, "BOOL": bool}
        output = []
        for field in fields:
            try:
                resource, *sub_resource, base_field = field.split(".")
                base_field = "type_" if base_field == "type" else base_field
                values = set()
                if resource == "metrics":
                    target_resource = metrics.Metrics
                elif resource == "segments":
                    # If segment has name segments.something.something
                    if sub_resource:
                        target_resource = getattr(
                            segments, f"{clean_resource(sub_resource[-1])}")
                    else:
                        target_resource = getattr(segments,
                                                  f"{clean_resource(resource)}")
                else:
                    resource_module = import_module(
                        f"{base_module}.resources.types.{resource}")

                    target_resource = getattr(resource_module,
                                              f"{clean_resource(resource)}")
                    try:
                        # If resource has name resource.something.something
                        if sub_resource:
                            target_resource = getattr(
                                target_resource,
                                f"{clean_resource(sub_resource[-1])}")
                    except AttributeError:
                        resource_module = import_module(
                            f"{base_module}.resources.types.{sub_resource[0]}")
                        if len(sub_resource) > 1:
                            if hasattr(resource_module,
                                       f"{clean_resource(sub_resource[1])}"):
                                target_resource = getattr(
                                    resource_module,
                                    f"{clean_resource(sub_resource[-1])}")
                            else:
                                resource_module = import_module(
                                    f"{common_types_module}.ad_type_infos")

                                target_resource = getattr(
                                    resource_module,
                                    f"{clean_resource(sub_resource[1])}Info")
                        else:
                            target_resource = getattr(
                                resource_module,
                                f"{clean_resource(sub_resource[-1])}")
                descriptor = target_resource.meta.fields.get(
                    base_field).descriptor
                result = descriptor.type

                if result == 14:  # 14 stands for ENUM
                    enum_class, enum = descriptor.type_name.split(".")[-2:]
                    file_name = re.sub(r'(?<!^)(?=[A-Z])', '_', enum).lower()
                    enum_resource = import_module(
                        f"{base_module}.enums.types.{file_name}")
                    values = set([
                        p.name
                        for p in getattr(getattr(enum_resource, enum_class), enum)
                    ])

                field_type = mapping.get(ProtoType(result).name, str)
                if result != 14:
                    if field_type == str:
                        values = {
                            "",
                        }
                    if field_type == int:
                        values = {
                            0,
                        }
                    if field_type == float:
                        values = {
                            0.0,
                        }
                    if field_type == bool:
                        values = {
                            False,
                        }
                field = Field(name=field, type=field_type, values=values)
            except (AttributeError, ModuleNotFoundError):
                field = Field(name=field, type=str, values={
                    "",
                })
            output.append(field)
        return output
