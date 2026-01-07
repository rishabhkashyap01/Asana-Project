import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

class LLMHelper:
    def __init__(self):
        # Read the key from the environment variable
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            print(" Warning: No API key found. Using fallback heuristics.")
            self.client = None
        else:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )

    def generate_task_description(self, task_name, project_type):
        if not self.client:
            return f"Standard SOP for {project_type} task: {task_name}"

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": f"Write a one-sentence Asana task description for: {task_name}"}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f" LLM Error: {e}")
            return "Task involves standard department protocols."