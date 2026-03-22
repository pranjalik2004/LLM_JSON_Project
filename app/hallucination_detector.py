"""
hallucination_detector.py
"""

import re
from typing import Dict


class HallucinationDetector:
 

    @staticmethod
    def analyze(raw_output: str) -> Dict:
        """
        Analyzes raw model output for hallucination signals.

        Returns:
            {
                "has_hallucination": bool,
                "reason": str | None
            }
        """

        if not raw_output or not raw_output.strip():
            return {
                "has_hallucination": True,
                "reason": "Empty response"
            }

        content = raw_output.strip()

        # Detect JSON object(s)
        json_blocks = re.findall(r"\{.*?\}", content, re.DOTALL)

        if len(json_blocks) == 0:
            return {
                "has_hallucination": True,
                "reason": "No JSON object detected"
            }

        if len(json_blocks) > 1:
            return {
                "has_hallucination": True,
                "reason": "Multiple JSON objects detected"
            }

        extracted_json = json_blocks[0].strip()

        # Check if entire response is exactly the JSON block
        if content != extracted_json:
            return {
                "has_hallucination": True,
                "reason": "Extra text outside JSON object"
            }

        return {
            "has_hallucination": False,
            "reason": None
        }
