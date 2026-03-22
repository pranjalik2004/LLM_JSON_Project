"""
llm_client.py
"""

from typing import Optional
import ollama
import threading
import re   


class LLMClient:
   
    def __init__(self, model_name: str = "phi3:mini"):
        self.model_name = model_name

    def generate(self, prompt: str) -> Optional[str]:
      

        result = {"response": None}

        def call_model():
            try:
                print("📤 Sending request to Ollama...")

                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    options={
                        "temperature": 0,
                        "num_predict": 100
                    },
                    stream=False
                )

                print("📥 Response received!")

                if response and "message" in response:
                    content = response["message"].get("content", "").strip()
                else:
                    result["response"] = None
                    return

                if content.startswith("```"):
                    lines = content.splitlines()
                    if len(lines) >= 3:
                        content = "\n".join(lines[1:-1]).strip()

                match = re.search(r"\{.*\}", content, re.DOTALL)
                if match:
                    content = match.group(0)

                result["response"] = content

            except Exception as e:
                print(f"[LLM ERROR] {str(e)}")
                result["response"] = None

        thread = threading.Thread(target=call_model)
        thread.start()

        thread.join(timeout=120)

        if thread.is_alive():
            print("⏱️ Timeout! Skipping this request...")
            return None

        return result["response"]
