"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import yaml
from typing import Tuple
import os
from vhcs.ctxp.data_util import load_data_file, strict_dict_to_class, process_variables


class PlanException(Exception):
    pass


class PluginException(Exception):
    pass


class Blueprint:
    vars: dict
    defaults: dict
    providers: dict
    resources: dict

    def __init__(self):
        self.vars = {}
        self.defaults = {}
        self.providers = {}
        self.resources = {}

    def __repr__(self):
        return f"Blueprint"


def load_files(files: list[str]) -> dict:
    ret = {}
    for file in files:
        data = load_data_file(file)
        if data == None or isinstance(data, str):
            raise FileNotFoundError("Fail loading file: " + file)
        ret = _merge_dict_fail_on_dup(ret, _smart_load_file(file))
    return ret


def process_template(template) -> Tuple[dict, dict]:

    # Ensure default sections are not None
    if "vars" not in template:
        template["vars"] = {}
    if "defaults" not in template:
        template["defaults"] = {}
    if "resources" not in template:
        template["resources"] = {}
    if "runtimes" not in template:
        template["runtimes"] = {}
    if "providers" not in template:
        template["providers"] = {}

    _validate_blueprint(template)
    bp, pending = _materialize_blueprint(template)
    return bp, pending


def _validate_blueprint(blueprint: dict):
    _validate_resource_schema(blueprint)
    _validate_resource_id_not_conflict_to_reserved_names(blueprint)
    _validate_no_conflict_resource_id_provider_types_runtime_id(blueprint)
    _validate_statement_after(blueprint)


def _validate_resource_schema(blueprint: dict):
    resources = blueprint["resources"]
    if not resources:
        return
    required_keys = set(["kind"])
    optional_keys = set(["eta", "data", "conditions", "for", "after"])
    for k, v in resources.items():

        def _raise(reason):
            raise PlanException(f"Invalid blueprint: {reason}. Resource: {k}")

        actual_keys = set(v.keys())
        missed_keys = required_keys - actual_keys
        if missed_keys:
            _raise(f"Missing required keys: {missed_keys}")
        extra_keys = actual_keys - required_keys - optional_keys
        if extra_keys:
            _raise(f"Unknown extra keys: {extra_keys}")


def _get_duplicates(lst):
    return [item for item in set(lst) if lst.count(item) > 1]


def _validate_statement_after(blueprint: dict):
    def _raise(owner, reason):
        raise PlanException(f"Invalid statement: after. Owner={owner}, reason={reason}.")

    items = {}
    items |= blueprint['resources']
    items |= blueprint['runtimes']

    def _validate_after(target_name, owner_resource_name):
        if not isinstance(target_name, str):
            _raise(owner_resource_name, f"Invalid value type: {type(target_name).__name__}")

        if target_name not in items:
            _raise(owner_resource_name, "Target not found: " + target_name)

    for k, v in items.items():
        after = v.get("after")
        if after:
            if isinstance(after, list):
                for a in after:
                    _validate_after(a, k)

                dup = _get_duplicates(after)
                if dup:
                    _raise(k, "Duplicated keys: " + dup)
            elif isinstance(after, str):
                _validate_after(after, k)
            else:
                _raise(k, "Invalid type, expect str or list, got: " + type(after).__name__)


def _validate_no_conflict_resource_id_provider_types_runtime_id(blueprint: dict):
    provider_names = set()
    runtime_names = set(blueprint["runtimes"].keys())
    for v in blueprint["resources"].values():
        name, _ = v["kind"].split("/")
        provider_names.add(name)

    declared_provider_names = set(blueprint["providers"].keys())
    excessive = declared_provider_names - provider_names
    if excessive:
        raise PlanException(
            f"Invalid blueprint. Unused provider definition: {excessive}."
        )
    resource_names = set(blueprint["resources"].keys())
    conflict = provider_names & resource_names
    if conflict:
        raise PlanException(
            f"Invalid blueprint. Provider ID and resource ID conflict: {conflict}."
        )
    conflict = runtime_names & resource_names
    if conflict:
        raise PlanException(
            f"Invalid blueprint. Runtime ID and resource ID conflict: {conflict}."
        )
    conflict = provider_names & runtime_names
    if conflict:
        raise PlanException(
            f"Invalid blueprint. Provider ID and runtime ID conflict: {conflict}."
        )


def _validate_resource_id_not_conflict_to_reserved_names(blueprint: dict):
    reserved_names_for_state = ["result", "pending", "log", "destroy_output"]
    reserved_names_for_blueprint = ["defaults", "vars", "providers", "resources", "runtimes"]
    reserved_names_for_function = ["profile", "context"]
    existing_names_top_level = blueprint.keys()
    reserved_names = set(
        [
            *existing_names_top_level,
            *reserved_names_for_blueprint,
            *reserved_names_for_state,
            *reserved_names_for_function,
        ]
    )
    for name in blueprint["resources"]:
        if name in reserved_names:
            raise PlanException("Invalid blueprint. Resource name conflicts to a reserved name: " + name)
    for name in blueprint["runtimes"]:
        if name in reserved_names:
            raise PlanException("Invalid blueprint. Runtime name conflicts to a reserved name: " + name)
    for name in blueprint["providers"]:
        if name in reserved_names:
            raise PlanException("Invalid blueprint. Provider name conflicts to a reserved name: " + name)


def _smart_load_file(file: str):
    if not os.path.exists(file):
        raise Exception("File not found: " + file)
    if not os.path.isfile(file):
        raise Exception("Not a file: " + file)
    if file.endswith(".json"):
        with open(file, "r") as f:
            return json.load(f)
    elif file.endswith(".yaml") or file.endswith(".yml"):
        with open(file, "r") as f:
            return yaml.safe_load(f)
    else:
        raise Exception("Unknown file extention: " + file)


def _merge_dict_fail_on_dup(o1: dict, o2: dict) -> dict:
    ret = dict(o1)
    for k, v in o2.items():
        if k in o1:
            raise Exception("Fail processing file. Duplicated key found: " + k)
        ret[k] = v
    return ret


def _materialize_blueprint(template: dict) -> Tuple[dict, dict]:
    ret = process_variables(template)
    return template, ret["pending"]
