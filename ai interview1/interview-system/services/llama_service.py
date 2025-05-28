import requests
import json

class LlamaService:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"

    def generate_question(self, resume_text):
        payload = {
            "model": "llama2",
            "prompt": f"Based on this resume: {resume_text}\nGenerate a relevant interview question.",
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            print(f"Error generating question: {e}")
            return None

    def evaluate_answer(self, question, answer):
        payload = {
            "model": "llama2",
            "prompt": f"Evaluate this interview answer for the question '{question}': '{answer}'. Provide a score from 0-100 and brief feedback.",
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return None