import functools
import importlib
import os
from typing import List

from envguardian._coercers import *
from envguardian._utils import *
from envguardian._validators import *


def get_schema():
    return getattr(importlib.import_module('Env'), 'env_schema', None)


class Env:

    def __init__(self, validation_schema: Dict[str, Callable]):
        self.schema = validation_schema

    @staticmethod
    def string():
        """
        String Schema definition. Returns the string validator and coercer
        :return:
        """
        return string_validator, string_coercer

    @staticmethod
    def int():
        """
        Integer Schema definition. Returns the int validator and coercer
        :return:
        """
        return int_validator, int_coercer

    @staticmethod
    def float():
        """
        Float schema definition. Returns the float validator and coercer
        :return:
        """
        return float_validator, float_coercer

    @staticmethod
    def enum(choices: List[Any]):
        """
        Enum schema definition. Returns the enum validator and coercer. Coercer casts to string
        :return:
        """
        return functools.partial(enum_validator, choices=choices), enum_coercer

    @staticmethod
    def boolean():
        """
        Boolean schema definition. Returns the boolean validator and coercer.
        :return:
        """
        return boolean_validator, boolean_coercer

    @staticmethod
    def validate(validation_schema=None):
        """
        Validate environment variable against the validation schema
        :return:
        """

        imported_schema = get_schema()

        if not imported_schema and not validation_schema:
            print('Invalid Validation Schema')

            return

        schema = imported_schema or validation_schema

        candidate_dict = get_schema_key_value_pair_from_environment_variables(schema, dict(os.environ))

        validation_results = validate_dictionary_against_validation_schema(schema, candidate_dict)

        failed_validations: Dict[str, str] = {}

        for index, candidate in enumerate(candidate_dict):
            if validation_results[index] == True:
                continue

            failed_validations[candidate] = validation_results[index]

        if len(failed_validations):
            raise Exception(str(failed_validations))

    @staticmethod
    def get(environment_variable, validation_schema=None):
        imported_schema = get_schema()

        if not imported_schema and not validation_schema:
            print('Invalid Validation Schema')

            return

        schema = imported_schema or validation_schema

        val = os.environ.get(environment_variable, None)

        if not val:
            return None

        return schema.get(environment_variable)[1](val)
