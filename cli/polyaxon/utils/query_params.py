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
from typing import Dict


def get_query_params(
    limit: str = None, offset: str = None, query: str = None, sort: str = None
) -> Dict:
    params = {}
    if limit:
        params["limit"] = limit
    if offset:
        params["offset"] = offset
    if query:
        params["query"] = query
    if sort:
        params["sort"] = sort

    return params


def get_logs_params(last_time: str = None, last_file: str = None) -> Dict:
    params = {}
    if last_file:
        params["last_file"] = last_file
    if last_time:
        params["last_time"] = last_time

    return params
