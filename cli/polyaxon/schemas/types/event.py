#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from marshmallow import fields

import polyaxon_sdk

from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.types.base import BaseTypeConfig


class EventSchema(BaseCamelSchema):
    name = RefOrObject(fields.Str(allow_none=True))
    kind = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1EventType


class V1EventType(BaseTypeConfig, polyaxon_sdk.V1EventType):
    IDENTIFIER = "event"
    SCHEMA = EventSchema
    REDUCED_ATTRIBUTES = ["name", "kind"]
