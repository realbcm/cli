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
import sys

from typing import Tuple

from polyaxon.constants.globals import DEFAULT, DEFAULT_HUB
from polyaxon.env_vars.getters.user import get_local_owner
from polyaxon.exceptions import PolyaxonClientException, PolyaxonSchemaError
from polyaxon.utils.formatting import Printer


def get_versioned_entity_info(
    entity: str, entity_name: str, default_owner: str
) -> Tuple[str, str, str]:
    if not entity:
        raise PolyaxonSchemaError(
            "Received an invalid {} reference: `{}`".format(entity_name, entity)
        )
    entity_values = entity.split(":")
    if len(entity_values) > 2:
        raise PolyaxonSchemaError(
            "Received an invalid {} reference: `{}`".format(entity_name, entity)
        )
    if len(entity_values) == 2:
        entity_namespace, version = entity_values
    else:
        entity_namespace, version = entity_values[0], "latest"
    version = version or "latest"
    parts = entity_namespace.replace(".", "/").split("/")
    owner = default_owner
    if not parts or len(parts) > 2:
        raise PolyaxonSchemaError(
            "Received an invalid {} reference: `{}`".format(entity_name, entity)
        )
    if len(parts) == 2:
        owner, entity_namespace = parts
    return owner, entity_namespace, version


def get_component_info(hub: str, use_local_owner: bool = False) -> Tuple[str, str, str]:
    from polyaxon import settings

    if use_local_owner:
        try:
            owner = get_local_owner()
        except PolyaxonClientException:
            owner = None

        if not owner and (not settings.CLI_CONFIG or settings.CLI_CONFIG.is_community):
            owner = DEFAULT
    else:
        owner = DEFAULT_HUB
    return get_versioned_entity_info(
        entity=hub, entity_name="component", default_owner=owner
    )


def get_model_info(entity: str, entity_name: str, is_cli: bool = False):
    from polyaxon import settings

    if not entity:
        message = "Please provide a valid {}!".format(entity_name)
        if is_cli:
            Printer.print_error(message)
            sys.exit(1)
        else:
            raise PolyaxonClientException(message)

    try:
        owner = get_local_owner()
    except PolyaxonClientException:
        owner = None

    if not owner and (not settings.CLI_CONFIG or settings.CLI_CONFIG.is_community):
        owner = DEFAULT

    owner, entity_namespace, version = get_versioned_entity_info(
        entity=entity, entity_name=entity_name, default_owner=owner
    )

    owner = owner or settings.AUTH_CONFIG.username

    if not all([owner, entity_name]):
        message = "Please provide a valid {}.".format(entity_name)
        if is_cli:
            Printer.print_error(message)
            sys.exit(1)
        else:
            raise PolyaxonClientException(message)
    return owner, entity_namespace, version
