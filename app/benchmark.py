"""
benchmark.py
"""

import os
import time
import random
import pandas as pd
from typing import Dict, List, Optional

from app.llm_client import LLMClient
from app.prompt_engine import PromptEngine, PromptType
from app.validator import JSONValidator
from app.hallucination_detector import HallucinationDetector


class LLMBenchmark:
    """
    Runs reliability evaluation experiments on structured LLM output.
    Silent: no console output.
    """

   
    # Dynamic input generator lists
   
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Riya", "Rahul", "Sneha", "Karan", "Amit"]
    courses = ["Computer Science", "Information Technology", "Artificial Intelligence", "Data Science", "MBA", "Engineering"]

    def __init__(self, model_name: str = "phi3"):
        self.client = LLMClient(model_name=model_name)
        self.validator = JSONValidator()

   
    # Retry helper

    def _generate_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        delay: float = 1.5,
        static_output: Optional[str] = None
    ):
        """
        Retry mechanism for handling timeouts or invalid responses.
        Returns static_output directly if provided.
        Silent mode: no prints.
        """
        if static_output is not None:
            return static_output

        for _ in range(max_retries):
            try:
                output = self.client.generate(prompt)
                if output:
                    cleaned = output.strip()
                    if cleaned.startswith("{") and cleaned.endswith("}"):
                        return cleaned
            except Exception:
                pass
            time.sleep(delay)
        return None

    # Generate dynamic input
    def _generate_dynamic_input(self) -> str:
        """
        Returns a random user input string for dynamic benchmarking
        """
        name = random.choice(self.names)
        age = random.randint(18, 30)
        course = random.choice(self.courses)
        return f"My name is {name}, I am {age} years old, studying {course}"

   
    # Run benchmark
  
    def run(
        self,
        prompt_type: PromptType,
        runs: int = 20,
        inputs: Optional[List] = None,
        use_static_data: bool = False,
        dynamic_input: bool = False
    ) -> Dict:
        """
        Executes multiple LLM calls and evaluates reliability.
        Silent: no console output during runs.
        """

        prompt = PromptEngine.get_prompt(prompt_type)

        # Default static inputs if none provided
        if inputs is None:
            inputs = [
                "hey my name is pranjali, im 22 studying mca",
                "rahul here, age is 23, doing IT",
                "I study CS and I'm Amit",
                "age 19, course BBA",
                "myself sneha, studying mba, 21 yrs",
                "Name: Karan | Age: twenty two | course: engineering",
                "I'm 20 and my name is Riya",
                "just random text without proper info"
            ]

        records = []
        valid_count = 0
        json_error_count = 0
        schema_error_count = 0
        hallucination_count = 0
        sample_output = None

        for i in range(runs):

          
            # Choose input: static or dynamic
        
            if dynamic_input:
                user_input = self._generate_dynamic_input()
            else:
                user_input = inputs[i % len(inputs)]

            start_time = time.time()

            if use_static_data:
                if isinstance(user_input, dict):
                    raw_output = str(user_input).replace("'", '"')
                else:
                    raw_output = str(user_input)
                raw_output = self._generate_with_retry(prompt="", static_output=raw_output)
            else:
                user_input_str = str(user_input).lower().strip()
                final_prompt = prompt + "\n\nInput:\n" + user_input_str
                raw_output = self._generate_with_retry(final_prompt)

            response_time = round(time.time() - start_time, 4)

            if raw_output is None:
                records.append({
                    "run_id": i + 1,
                    "valid": False,
                    "error_type": "Timeout/InvalidFormat",
                    "hallucination": False,
                    "response_time_sec": response_time
                })
                continue

            validation_result = self.validator.validate_output(raw_output)
            is_valid = validation_result["is_valid"]
            error_type = validation_result["error_type"]

            has_hallucination = False
            if not use_static_data and error_type is None:
                hallucination_result = HallucinationDetector.analyze(raw_output)
                has_hallucination = hallucination_result["has_hallucination"]
                if has_hallucination:
                    hallucination_count += 1

            if is_valid:
                valid_count += 1
                if sample_output is None:
                    sample_output = validation_result.get("parsed_output", raw_output)
            else:
                if error_type == "JSONDecodeError":
                    json_error_count += 1
                elif error_type == "SchemaValidationError":
                    schema_error_count += 1

            records.append({
                "run_id": i + 1,
                "valid": is_valid,
                "error_type": error_type,
                "hallucination": has_hallucination,
                "response_time_sec": response_time
            })

            time.sleep(1 if use_static_data else 2)

        # Save report silently
        df = pd.DataFrame(records)
        os.makedirs("reports", exist_ok=True)
        report_path = f"reports/{prompt_type.value}_benchmark.csv"
        df.to_csv(report_path, index=False)

        reliability_score = round((valid_count / runs) * 100, 2)

        summary = {
            "model": self.client.model_name,
            "prompt_type": prompt_type.value,
            "total_runs": runs,
            "valid_outputs": valid_count,
            "json_errors": json_error_count,
            "schema_errors": schema_error_count,
            "hallucinations": hallucination_count,
            "reliability_score_percent": reliability_score,
            "report_file": report_path,
            "sample_output": sample_output
        }

        return summary
