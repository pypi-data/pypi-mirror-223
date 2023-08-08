"""Init plugin with CKAN interfaces."""

import logging

from ckan.plugins import SingletonPlugin, implements, interfaces

from ckanext.envidat_validators.logic import (
    envidat_copy_type_general,
    envidat_minimum_description_length,
    envidat_minimum_tag_count,
    envidat_reorder,
    envidat_shortname_validator,
    envidat_string_uppercase,
)

log = logging.getLogger(__name__)


class EnviDatValidatorsPlugin(SingletonPlugin):
    """EnviDatValidatorsPlugin.

    Plugin to add additional validation to CKAN.
    """

    implements(interfaces.IValidators)
    implements(interfaces.IPackageController, inherit=True)

    # IValidators
    def get_validators(self):
        """Assemble validators for IValidators interface."""
        return {
            "envidat_string_uppercase": envidat_string_uppercase,
            "envidat_shortname_validator": envidat_shortname_validator,
            "envidat_minimum_tag_count": envidat_minimum_tag_count,
            "envidat_reorder": envidat_reorder,
            "envidat_copy_type_general": envidat_copy_type_general,
            "envidat_minimum_description_length": envidat_minimum_description_length,
        }

    # # IPackageController
    # def before_dataset_index(self, data_dict):
    #     """Tasks to run prior to Solr re-indexing."""
    #     # TODO fix Solr indexing once repeating fields enabled
    #     # https://ckan.org/blog/scheming-subfields
    #     # https://github.com/ckan/ckanext-scheming#repeating_subfields
    #     return data_dict
