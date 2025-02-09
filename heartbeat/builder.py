import os
import json
from typing import Dict


class SchemaBuilder:
    def __init__(self, name: str):
        """
        Initialize the SchemaBuilder class.

        Args:
        - name (str): The name of the schema.
        """
        self.name = name
        self.schema = {
            "health": True,
            "last_updated": 0,
            "error": None
        }

    def add_field(self, field_name: str, field_type: str, default_value=None):
        """
        Add a field to the schema.

        Args:
        - field_name (str): The name of the field.
        - field_type (str): The type of the field.
        - default_value (any): The default value of the field.
        """
        self.schema[field_name] = default_value

    def get_schema(self):
        """
        Get the schema.

        Returns:
        - dict: The schema.
        """
        return self.schema

