"""prompt_engine.py
"""

from enum import Enum


class PromptType(Enum):
    BASIC = "basic"
    STRICT_JSON = "strict_json"
    ROLE_CONSTRAINED = "role_constrained"
    FEW_SHOT = "few_shot"


class PromptEngine:
  
    BASE_SCHEMA_DESCRIPTION = (
        'The JSON must contain the following fields:\n'
        '- "name": string or null\n'
        '- "age": integer or null\n'
        '- "course": string or null\n'
    )

    @staticmethod
    def get_prompt(prompt_type: PromptType) -> str:

        if prompt_type == PromptType.BASIC:
            return (
                "Generate a student profile in valid JSON format "
                "with the following fields: name, age, and course. "
                "If a value is missing, use null."
            )

        elif prompt_type == PromptType.STRICT_JSON:
            # 🔹 Updated for static data compatibility: {user_input} optional
            return (
                "Extract structured data from the input below.\n\n"

                "⚠️ STRICT INSTRUCTIONS (FOLLOW EXACTLY):\n"
                "- Output ONLY a valid JSON object\n"
                "- Do NOT write explanations or extra text\n"
                "- Do NOT use markdown or comments\n\n"

                "Required JSON format:\n"
                '{\n'
                '  "name": "string or null",\n'
                '  "age": number or null,\n'
                '  "course": "string or null"\n'
                '}\n\n'

                "Rules:\n"
                "- Extract 'name', 'age', and 'course' exactly as given\n"
                "- If any field is missing → return null\n"
                "- Do NOT guess values\n"
                "- 'age' must be a number only\n"
                "- No extra fields are allowed\n\n"

                "Example:\n"
                "Input: my name is Rahul, I am 22 studying IT\n"
                'Output: {"name": "Rahul", "age": 22, "course": "IT"}\n\n'

                "Input (optional for static data):\n"
                "{user_input}\n\n"

                "Output:"
            )

        elif prompt_type == PromptType.ROLE_CONSTRAINED:
            return (
                "You are a backend API service.\n"
                "Your task is to extract structured data from input and return strictly valid JSON.\n"
                "Do NOT provide commentary, formatting text, or explanations.\n"
                f"{PromptEngine.BASE_SCHEMA_DESCRIPTION}"
                "Rules:\n"
                "- If any field is missing or unclear, return null\n"
                "- Do NOT guess missing values\n"
                "- Follow the schema strictly and do not add extra fields\n"
            )

        elif prompt_type == PromptType.FEW_SHOT:
            return (
                "You are a data extraction system.\n"
                "Return ONLY strictly valid JSON.\n\n"

                "Example 1:\n"
                "Input: John Doe is 21 years old and studies Computer Science\n"
                'Output: {"name": "John Doe", "age": 21, "course": "Computer Science"}\n\n'

                "Example 2:\n"
                "Input: Alice is 19 and enrolled in BCA\n"
                'Output: {"name": "Alice", "age": 19, "course": "BCA"}\n\n'

                "Example 3:\n"
                "Input: I am 20 and my name is Riya\n"
                'Output: {"name": "Riya", "age": 20, "course": null}\n\n'

                "Rules:\n"
                "- If a field is missing, return null\n"
                "- Do NOT guess missing values\n"
                "- Output must be strictly valid JSON\n"
                "- No extra text, formatting, or explanations\n\n"

                f"{PromptEngine.BASE_SCHEMA_DESCRIPTION}"
                "Now extract data from the given input:\n"
                "{user_input}"  
            )

        else:
            raise ValueError(f"Unsupported prompt type: {prompt_type}")
