from utils.llm_helper import LLMHelper
import os
from dotenv import load_dotenv

load_dotenv()

def test():
    print(f"Checking API Key: {os.getenv('GROQ_API_KEY')[:10]}...") # Print first few chars
    helper = LLMHelper()
    
    test_task = "Patch security vulnerability in Auth-Service"
    print(f"Testing LLM with task: {test_task}")
    
    result = helper.generate_task_description(test_task, "Engineering")
    print(f"\n--- LLM RESPONSE ---\n{result}\n--------------------")

if __name__ == "__main__":
    test()