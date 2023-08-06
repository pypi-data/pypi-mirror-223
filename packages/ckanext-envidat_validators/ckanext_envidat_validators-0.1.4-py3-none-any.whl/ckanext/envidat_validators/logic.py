"""Validator logic for IValidators."""

import logging

import ckan.lib.navl.dictization_functions as df
from ckantoolkit import _

from ckanext.scheming.validation import scheming_validator

log = logging.getLogger(__name__)


def envidat_shortname_validator(key, data, errors, context):
    """Prevent short package titles <80 char."""
    value = data.get(key)
    if not value or len(value) > 80:
        errors[key].append(_("text should be maximum 80 characters long"))
        raise df.StopOnError


def envidat_string_uppercase(key, data, errors, context):
    """Make string values uppercase.

    If the value is a string, make it uppercase, otherwise leave the value as it is.
    make all tags uppercase if possible.
    """
    # Plain value to uppercase
    tags = data[key]
    if isinstance(tags, str):
        data[key] = tags.upper()

    # tags to uppercase
    num = 0
    tag = data.get(("tags", num, "name"), "")
    while tag:
        data[("tags", num, "name")] = _safe_upper(tag)
        num += 1
        tag = data.get(("tags", num, "name"), "")


def envidat_minimum_tag_count(key, data, errors, context):
    """Count tags and raise an error if there are less than 5."""
    min_tags = 5
    # tags to count
    num = 0
    tag = data.get(("tags", num, "name"), "")
    while tag:
        num += 1
        tag = data.get(("tags", num, "name"), "")

    if num < min_tags:
        errors[key].append(_("at least " + str(min_tags) + " tags"))
        raise df.StopOnError


def envidat_minimum_description_length(key, data, errors, context):
    """Count description chars and raise an error if there are less than 100."""
    min_length = 100
    # tags to count
    description = data.get(key, "")
    description_length = len(description)

    if description_length < min_length:
        errors[key].append(
            _(
                "at least {0} characters, currently {1}".format(
                    min_length, description_length
                )
            )
        )
        raise df.StopOnError


@scheming_validator
def envidat_reorder(field, schema):
    """Reorder sub elements."""

    def validator(key, data, errors, context):
        """Logic for envidat_reorder."""
        elements = data.get(key, [])
        if not isinstance(elements, list):
            log.error(f"The field '{key}' must be a list.")
            return

        # Sort the elements based on the "order" key or by the element's position
        sorted_list = sorted(elements, key=lambda k: int(k.get("order", len(elements))))

        # Remove the "order" key from each element (if exists)
        for element in sorted_list:
            element.pop("order", None)

        data[key] = sorted_list

    return validator


@scheming_validator
def envidat_copy_type_general(field, schema):
    """Copy type general."""

    def validator(key, data, errors, context):
        """Logic for envidat_copy_type_general."""
        data[key] = data.get(("resource_type_general",), data[key])

    return validator


def _safe_upper(value):
    """Upper or same value if it is not a string."""
    try:
        return value.upper()
    except Exception:
        return value
