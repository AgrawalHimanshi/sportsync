# app.py

import time
import json
from flask import Flask, render_template, request, jsonify
import io
import wave
import simpleaudio as sa # For playing audio directly
# from pydub import AudioSegment # For converting raw audio to WAV format for simpleaudio

from api_clients import QlooClient, OpenAIClient, ElevenLabsClient, GTTSClient, GeminiClient, EdgeTTSClient
from commentary_generator import CommentaryGenerator

app = Flask(__name__)

# Initialize API Clients
qloo_client = QlooClient()
openai_client = GeminiClient()
# elevenlabs_client = ElevenLabsClient()
gtts_client = EdgeTTSClient() # If you want to use gTTS instead of ElevenLabs
commentary_generator = CommentaryGenerator(openai_client)

# --- Simulated Game Events (for PoC) ---
# Each event has a 'time' (in seconds from start) and details for commentary.
GAME_EVENTS = [
    {"time": 0, "sport": "Football", "event_type": "kick_off", "score": "0-0"},
    {"time": 10, "sport": "Football", "event_type": "shot_on_goal", "player": "Ronaldo", "team": "Al Nassr", "outcome": "scored", "metadata": {"shot_type": "header"}, "score": "1-0"},
    {"time": 25, "sport": "Football", "event_type": "foul", "player": "Messi", "team": "Inter Miami", "fouled_player": "opponent", "outcome": "yellow_card", "score": "1-0"},
    {"time": 40, "sport": "Football", "event_type": "possession_change", "team": "Inter Miami", "score": "1-0"},
    {"time": 50, "sport": "Football", "event_type": "save", "player": "Goalkeeper", "team": "Al Nassr", "score": "1-0"},
    {"time": 60, "sport": "Football", "event_type": "halftime", "score": "1-0"},
    {"time": 75, "sport": "Football", "event_type": "penalty", "player": "Ronaldo", "team": "Al Nassr", "score": "1-0"},
    {"time": 80, "sport": "Football", "event_type": "shot_on_goal", "player": "Ronaldo", "team": "Al Nassr", "outcome": "scored", "metadata": {"shot_type": "penalty_kick"}, "score": "2-0"},
    {"time": 95, "sport": "Football", "event_type": "substitution", "team": "Inter Miami", "metadata": {"player_out": "Busquets", "player_in": "New Midfielder"}, "score": "2-0"},
    {"time": 110, "sport": "Football", "event_type": "shot_on_goal", "player": "Messi", "team": "Inter Miami", "outcome": "scored", "metadata": {"shot_type": "finesse"}, "score": "2-1"},
    {"time": 120, "sport": "Football", "event_type": "end_game", "score": "2-1", "winning_team": "Al Nassr"},
]

# --- Global variable to store selected user taste profile ---
current_user_taste = {}

@app.route('/')
def index():
    """Renders the main HTML page for the application."""
    return render_template('index.html')

@app.route('/select_profile', methods=['POST'])
def select_profile():
    """
    Handles the selection of a commentary profile.
    Simulates sending user data to Qloo to get a taste profile.
    """
    global current_user_taste
    selected_profile_type = request.form['profile']

    # Simulate user data that Qloo might process.
    # In a real app, this would come from user's actual behavior/preferences.
    user_data_for_qloo = {"user_id": "demo_user_123", "preference_type": selected_profile_type}

    # Get taste profile from Qloo (or its mock/fallback)
    current_user_taste = qloo_client.get_user_taste_profile(user_data_for_qloo)

    return jsonify({
        "message": f"Profile set to {selected_profile_type}",
        "profile_style": current_user_taste.get("style", "balanced")
    })

@app.route('/start_game', methods=['POST'])
def start_game():
    """
    Simulates a game by iterating through events, generating commentary,
    and playing the audio based on the selected taste profile.
    """
    if not current_user_taste:
        return jsonify({"error": "Please select a commentary profile first."}), 400

    results = []
    start_time_sim = time.time()

    for event in GAME_EVENTS:
        elapsed_time_sim = time.time() - start_time_sim
        time_to_wait = event["time"] - elapsed_time_sim

        # Pause to simulate real-time game progression
        if time_to_wait > 0:
            time.sleep(time_to_wait)

        print(f"\n--- Simulating Event at {event['time']}s ---")
        print(f"Event: {event.get('event_type', 'N/A')} by {event.get('player', 'N/A')}")
        print(f"User Taste Style: {current_user_taste.get('style', 'N/A')}")

        # Generate commentary text using LLM
        commentary_text = commentary_generator.get_commentary(event, current_user_taste)
        print(f"Generated Commentary: {commentary_text}")

        # Convert commentary text to speech audio
        audio_content_wav = gtts_client.text_to_speech(commentary_text)
    
        if audio_content_wav:
            try:
                # Use Python's built-in 'wave' module to open the BytesIO object as a WAV file.
                # This creates the 'wave.Wave_read' object that simpleaudio expects.
                with io.BytesIO(audio_content_wav) as wav_buffer: # Use a context manager for the BytesIO object
                    with wave.open(wav_buffer, 'rb') as wave_file: # Open the BytesIO as a wave file
                        wave_obj = sa.WaveObject.from_wave_read(wave_file)
                        play_obj = wave_obj.play()
                        play_obj.wait_done() # Wait for playback to finish
                        print("Audio played successfully.")
            except Exception as e:
                print(f"Error playing audio: {e}")
                # You might want to log the error to a file or provide more details for debugging
                # For example, check if audio_content_wav is empty or corrupted
                if not audio_content_wav:
                    print("Error: audio_content_wav was empty.")
                else:
                    print(f"Length of audio_content_wav: {len(audio_content_wav)} bytes.")
        
        else:
            print("No audio content generated by Edge TTS.")

        results.append({
            "time": event["time"],
            "event_type": event["event_type"],
            "commentary": commentary_text,
            "profile_style": current_user_taste.get('style', 'N/A')
        })

    return jsonify(results)

if __name__ == '__main__':
    # Ensure you have your virtual environment activated before running
    # python app.py
    app.run(debug=True) # debug=True enables auto-reloading and better error messages