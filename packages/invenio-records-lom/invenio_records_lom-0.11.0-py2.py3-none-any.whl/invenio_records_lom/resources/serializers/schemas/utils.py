# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Common utilities for schemas."""


def get_text(value):
    """Get text from langstring object."""
    return value["langstring"]["#text"]


def get_lang(value):
    """Get lang from langstring object."""
    return value["langstring"]["lang"]


def get_related(obj: dict, relation_kind: str, catalog: str = "repo-pid") -> list:
    """Get dereferenced records that are `relation_kind`-related to `obj`."""
    results = []
    for relation in obj["metadata"].get("relation", []):
        if get_text(relation["kind"]["value"]) != relation_kind:
            continue

        for identifier in relation["resource"]["identifier"]:
            if identifier["catalog"] != catalog:
                continue

            results.append(identifier)

    return results


def get_newest_part(obj: dict):
    """Get newest dereferenced record that is "haspart"-related to `obj`."""
    parts = get_related(obj, relation_kind="haspart")
    return parts[-1]
