import google.generativeai as genai
import os

# Make sure to set your API key as an environment variable (e.g., GOOGLE_API_KEY)
# Or load it from your .env file
# from dotenv import load_dotenv
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # You can choose different models, e.g., 'gemini-1.5-flash', 'gemini-1.5-pro'
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_commentary(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            # Check if response.text exists and is not empty
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                print(f"Warning: Gemini response had no text content for prompt: {prompt}")
                return "No commentary generated."
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            # You might get errors if content is blocked or rate limited
            return "Error generating commentary."

# Integration into your app.py:
# from api_clients import GeminiClient # Assuming you put it here
# import os
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Ensure this is in your .env
# llm_client = GeminiClient(api_key=GOOGLE_API_KEY)
# commentary_text = llm_client.generate_commentary(prompt)