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
        self.schema ={self.name:{}}
        self.schema[self.name] = {
            "health": True,
            "last_updated": 0,
            "interval":0,
            "error": None
        }
        self.supported_types = ["string", "integer", "float", "boolean", "object", "array"]

    def add_field(self, field_name: str, field_type: str, default_value=None):
        """
        Add a field to the schema.

        Args:
        - field_name (str): The name of the field.
        - field_type (str): The type of the field.
        - default_value (any): The default value of the field.

        Raises:
        - ValueError: If the field type is not supported.
        - TypeError: If the default value does not match the field type.
        """
        if field_type not in self.supported_types:
            raise ValueError(f"Unsupported field type: {field_type}. Supported types are: {', '.join(self.supported_types)}")

        if default_value is not None:
            if field_type == "string" and not isinstance(default_value, str):
                raise TypeError(f"Default value for field '{field_name}' must be a string.")
            elif field_type == "integer" and not isinstance(default_value, int):
                raise TypeError(f"Default value for field '{field_name}' must be an integer.")
            elif field_type == "float" and not isinstance(default_value, (int, float)):
                raise TypeError(f"Default value for field '{field_name}' must be a float.")
            elif field_type == "boolean" and not isinstance(default_value, bool):
                raise TypeError(f"Default value for field '{field_name}' must be a boolean.")
            elif field_type == "object" and not isinstance(default_value, dict):
                raise TypeError(f"Default value for field '{field_name}' must be an object.")
            elif field_type == "array" and not isinstance(default_value, list):
                raise TypeError(f"Default value for field '{field_name}' must be an array.")

        self.schema[self.name][field_name] = {
            "type": field_type,
            "value": default_value
        }
    
    def update_field_value(self, field_name, value):
        """
        Update the value of a field in the schema.

        Args:
            field_name (str): The name of the field to update.
            value (any): The new value of the field.

        Raises:
            KeyError: If the field does not exist in the schema.
        """
        if field_name not in self.schema[self.name]:
            raise KeyError(f"Field '{field_name}' does not exist in the schema")

        self.schema[self.name][field_name]['value'] = value

    def get_schema(self):
        """
        Get the schema.

        Returns:
        - dict: The schema.
        """
        return self.schema

