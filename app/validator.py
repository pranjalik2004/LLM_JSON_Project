"""
validator.py
"""

import json
from app.schema import EXPECTED_SCHEMA


class JSONValidator:

    def validate_output(self, raw_output: str) -> dict:
        """

        Returns:
            {
                "is_valid": bool,
                "error_type": str | None,
                "parsed_output": dict | None
            }
        """

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError:
            return {
                "is_valid": False,
                "error_type": "JSONDecodeError"
            }

        if "age" in data and isinstance(data["age"], str):
            words_to_numbers = {
                "twenty one": 21,
                "twenty two": 22,
                "twenty three": 23,
                "twenty": 20
            }
            data["age"] = words_to_numbers.get(data["age"].lower(), data["age"])

        for key in EXPECTED_SCHEMA:
            if key not in data:
                return {
                    "is_valid": False,
                    "error_type": "SchemaValidationError"
                }

        for key in data:
            if key not in EXPECTED_SCHEMA:
                return {
                    "is_valid": False,
                    "error_type": "SchemaValidationError"
                }

        for key, expected_type in EXPECTED_SCHEMA.items():

            value = data[key]

            if key == "age":
                if not isinstance(value, int):
                    return {
                        "is_valid": False,
                        "error_type": "SchemaValidationError"
                    }

            else:
                if not isinstance(value, expected_type) or str(value).strip() == "":
                    return {
                        "is_valid": False,
                        "error_type": "SchemaValidationError"
                    }

        return {
            "is_valid": True,
            "error_type": None,
            "parsed_output": data
        }
