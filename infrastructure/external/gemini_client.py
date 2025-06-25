import os
import requests

class GeminiClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    def ask(self, prompt: str):
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(self.api_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        gemini_response = response.json()
        # Extract the model's text response (may need to adjust depending on Gemini's actual response format)
        try:
            text = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            text = gemini_response
        return text