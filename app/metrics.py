"""metrics.py
"""

from typing import Dict
import pandas as pd


class MetricsCalculator:

    @staticmethod
    def compute(df: pd.DataFrame) -> Dict:
        
        total_runs = len(df)

        valid_outputs = df["valid"].sum()

        json_errors = (df["error_type"] == "JSONDecodeError").sum()
        schema_errors = (df["error_type"] == "SchemaValidationError").sum()
        hallucinations = df["hallucination"].sum()

        reliability_score = round((valid_outputs / total_runs) * 100, 2) if total_runs > 0 else 0.0

        return {
            "total_runs": total_runs,
            "valid_outputs": int(valid_outputs),
            "json_errors": int(json_errors),
            "schema_errors": int(schema_errors),
            "hallucinations": int(hallucinations),
            "reliability_score_percent": reliability_score
        }
