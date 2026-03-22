"""main.py"""
from app.benchmark import LLMBenchmark
from app.prompt_engine import PromptType
import json

def print_sample_output(sample_output: dict) -> None:
    print("\n🔹 1. Sample Model Output\n")
    print(json.dumps(sample_output, indent=2))


def print_summary(summary: dict) -> None:
    print("\n🔹 2. Benchmark Results\n")
    print(f"Model Used              : {summary['model']}")
    print(f"Prompt Strategy         : {summary['prompt_type']}")
    print(f"Total Runs              : {summary['total_runs']}")
    print(f"Valid Outputs           : {summary['valid_outputs']}")
    print(f"JSON Parsing Errors     : {summary['json_errors']}")
    print(f"Schema Validation Errors: {summary['schema_errors']}")
    print(f"Hallucinations Detected : {summary['hallucinations']}")
    print(f"Reliability Score (%)   : {summary['reliability_score_percent']}")
    print(f"Report Saved At         : {summary['report_file']}")




if __name__ == "__main__":

    MODEL_NAME = "phi3:mini"
    PROMPT_STRATEGY = PromptType.STRICT_JSON
    NUMBER_OF_RUNS = 15

   
    benchmark_inputs = [
        {"name": "Pranjali", "age": 22, "course": "MCA"},
        {"name": "Rahul", "age": 23, "course": "IT"},
        {"name": "Amit", "age": 20, "course": "CS"},
        {"name": "Kiran", "age": 19, "course": "BBA"},
        {"name": "Sneha", "age": 21, "course": "MBA"},
        {"name": "Riya", "age": 20, "course": "Engineering"},
        {"name": "Aditi", "age": 22, "course": "BCA"}
    ]

  
    benchmark = LLMBenchmark(model_name=MODEL_NAME)

 
    summary_results = benchmark.run(
        prompt_type=PROMPT_STRATEGY,
        runs=NUMBER_OF_RUNS,
        inputs=benchmark_inputs,
        use_static_data=True
    )

    # Sample output for display
    sample_output = {
        "name": "John Doe",
        "age": 21,
        "course": "Computer Science"
    }

   
    print_sample_output(sample_output)
    print_summary(summary_results)
  
