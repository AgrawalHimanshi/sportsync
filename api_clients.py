# api_clients.py

import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import edge_tts
import asyncio
from openai import OpenAI # Import OpenAI's official client

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        # You can choose different models, e.g., 'gemini-1.5-flash', 'gemini-1.5-pro'
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_commentary(self, prompt: str) -> str:
        try:
            print("---------------------------------------------------------------")
            print(f"Generating Gemini commentary with prompt: {prompt}")
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


class QlooClient:
    """
    Client for interacting with the Qloo API.
    NOTE: The actual Qloo API endpoint and payload structure for fetching
    taste profiles will depend on your specific Qloo API access and documentation.
    This implementation provides a plausible structure and a placeholder for
    where you would integrate the real Qloo API call.
    """
    def __init__(self):
        self.api_key = os.getenv("QLOO_API_KEY")
        # Verify Qloo's actual API base URL from their documentation
        self.base_url = "https://hackathon.api.qloo.com" # This is a common pattern, but verify

    def get_user_taste_profile(self, user_data: dict) -> dict:
        """
        Fetches a user's taste profile from Qloo based on provided user data.
        For a hackathon PoC, `user_data` might be a simple identifier or
        a few example preferences.
        """
        if not self.api_key:
            print("QLOO_API_KEY not set. Returning a mocked taste profile.")
            # Mocked Qloo response for demonstration if API key is missing
            # In a real scenario, Qloo would analyze user data (e.g., content consumption, demographics)
            # to return a detailed taste profile.
            # We'll simulate mapping a simple 'preference_type' to a commentary style.
            preference_type = user_data.get("preference_type", "balanced")
            if preference_type == "analytical":
                return {"style": "analytical", "focus": ["stats", "tactics", "efficiency"]}
            elif preference_type == "emotional":
                return {"style": "emotional", "focus": ["passion", "drama", "player_narratives"]}
            elif preference_type == "humorous":
                return {"style": "humorous", "focus": ["jokes", "lighthearted", "sarcasm"]}
            else:
                return {"style": "balanced", "focus": ["general", "key_moments"]}


        # --- Placeholder for actual Qloo API call ---
        # You would replace this section with your actual Qloo API integration.
        # Example hypothetical API call (adjust based on Qloo's real documentation):
        # headers = {
        #     "Authorization": f"Bearer {self.api_key}", # Or 'X-API-Key' depending on Qloo
        #     "Content-Type": "application/json"
        # }
        headers = {
            "accept": "application/json",
            "X-Api-Key": "836jxA0OzDhGEY5gURAVZorV3RgnSFugkJ7EOV8L5JU"
        }
        # The payload structure will be defined by Qloo's API for taste profiles.
        # It might involve sending user IDs, historical consumption data, etc.
        payload = {
            "user_identifier": user_data.get("user_id"),
            "preferences": user_data.get("preferences", []) # e.g., [{"type": "movie", "value": "action"}]
        }
        
        try:
            print("---------------------------------------------------------------")
            print(f"Fetching taste profile for user: {user_data.get('user_id')}")
            response = requests.get(f"{self.base_url}/v2/audiences/types", headers=headers)
            
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            qloo_response = response.json()
            print("qloo reponse", qloo_response)
            # Process Qloo's response to extract a simplified taste profile for commentary
            # This logic will depend heavily on the structure of Qloo's actual response.
            # For this PoC, we'll map some hypothetical Qloo output to our styles.
            # Example: if Qloo returns high affinity for 'analytical content', map to 'analytical'
            # For now, we'll keep the mock-like mapping for the PoC for simplicity
            # once a real Qloo response is received.
            # This part needs to be tailored to actual Qloo output.
            if "affinity_scores" in qloo_response:
                # Example: Map Qloo's affinity scores to our commentary styles
                if qloo_response["affinity_scores"].get("analytical_content", 0) > 0.7:
                    return {"style": "analytical", "focus": ["stats", "tactics"]}
                elif qloo_response["affinity_scores"].get("drama_narratives", 0) > 0.7:
                    return {"style": "emotional", "focus": ["passion", "player_narratives"]}
                elif qloo_response["affinity_scores"].get("comedy_genres", 0) > 0.7:
                    return {"style": "humorous", "focus": ["jokes", "lighthearted"]}
            return {"style": "balanced", "focus": ["general", "key_moments"]} # Default if no strong affinity

        except requests.exceptions.RequestException as e:
            print(f"Error calling Qloo API: {e}. Returning a mocked taste profile.")
            # Fallback to mocked profile on API error
            preference_type = user_data.get("preference_type", "balanced")
            if preference_type == "analytical":
                return {"style": "analytical", "focus": ["stats", "tactics", "efficiency"]}
            elif preference_type == "emotional":
                return {"style": "emotional", "focus": ["passion", "drama", "player_narratives"]}
            elif preference_type == "humorous":
                return {"style": "humorous", "focus": ["jokes", "lighthearted", "sarcasm"]}
            else:
                return {"style": "balanced", "focus": ["general", "key_moments"]}


class OpenAIClient:
    """
    Client for interacting with the OpenAI API (LLM for text generation).
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=self.api_key)

    def generate_commentary(self, prompt: str) -> str:
        """
        Generates commentary text using an OpenAI LLM.
        """
        try:
            print("---------------------------------------------------------------")
            print(f"Generating OpenAI commentary with prompt: {prompt}")
            chat_completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # You can try "gpt-4o" for higher quality if desired
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7 # Adjust for more/less creativity
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "Commentary AI is temporarily unavailable."


from gtts import gTTS
import io
from pydub import AudioSegment # You'll need pydub and ffmpeg for this!

class GTTSClient:
    def text_to_speech(self, text: str) -> bytes:
        """
        Converts text to speech using gTTS and returns WAV bytes.
        Requires pydub and ffmpeg for MP3 to WAV conversion.
        """
        print("---------------------------------------------------------------")
        print("Converting text to speech using gTTS...")
        print("Text:", text)
        tts = gTTS(text=text, lang='en', slow=False) # 'en' for English
        mp3_io = io.BytesIO()
        tts.write_to_fp(mp3_io)
        mp3_io.seek(0) # Rewind to the beginning

        # Convert MP3 (from gTTS) to WAV (for simpleaudio) in memory
        audio_segment = AudioSegment.from_file(mp3_io, format="mp3")
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0) # Rewind to the beginning

        return wav_io.getvalue()


# --- TTS Client (Edge TTS) ---
DEFAULT_EDGE_VOICE = "en-US-JennyNeural"


class EdgeTTSClient:
    def __init__(self, voice: str = DEFAULT_EDGE_VOICE):
        self.voice = voice
        self.i = 0

    async def _text_to_speech_async(self, text: str) -> bytes:
        """Internal async method to generate speech."""
        try:
            filename = "output.wav"
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(filename)
            with open(filename, "rb") as f:
                wav_data = f.read()
            os.remove(filename)  # Clean up the file
            return wav_data
        except Exception as e:
            print(f"Error in Edge TTS async generation: {e}")
            return b""

    def text_to_speech(self, text: str) -> bytes:
        """
        Converts text to speech using edge-tts and returns WAV bytes.
        Runs the async method in an event loop.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            wav_data = loop.run_until_complete(self._text_to_speech_async(text))
            return wav_data
        finally:
            loop.close()
            asyncio.set_event_loop(None)


# If you use gTTS, you'll need pydub again, and thus ffmpeg.
# So, the "no ffmpeg" benefit from the ElevenLabs WAV trick is lost here.
# You would replace elevenlabs_client with gtts_client.

class ElevenLabsClient:
    """
    Client for interacting with the ElevenLabs API (Text-to-Speech).
    """
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
        self.base_url = "https://api.elevenlabs.io/v1"
        # Default voice ID (e.g., 'Rachel'). Find more in your ElevenLabs dashboard.
        self.default_voice_id = "21m00Tzpb8IMy8lnFpwa"

    def text_to_speech(self, text: str, voice_id: str = None) -> bytes:
        """
        Converts text to speech audio data using ElevenLabs.
        Returns raw audio bytes.
        """
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg" # Requesting MP3 audio
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1", # Or "eleven_multilingual_v2" for more languages
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }
        selected_voice_id = voice_id if voice_id else self.default_voice_id
        url = f"{self.base_url}/text-to-speech/{selected_voice_id}"

        try:
            response = requests.post(url, json=payload, headers=headers, stream=True)
            response.raise_for_status()
            # Read the audio content in chunks
            audio_content = b''
            for chunk in response.iter_content(chunk_size=1024):
                audio_content += chunk
            return audio_content
        except requests.exceptions.RequestException as e:
            print(f"Error calling ElevenLabs API: {e}")
            return None