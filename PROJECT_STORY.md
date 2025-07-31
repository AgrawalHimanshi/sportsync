# QlooSport Sync: Personalized Live Sports Commentary

## Inspiration

The inspiration for QlooSport Sync came from the desire to make live sports commentary more engaging and tailored to individual fans. Traditional broadcasts offer a one-size-fits-all experience, but every fan has unique preferences—some love deep tactical analysis, others crave emotional highs, and some just want a good laugh. I wanted to harness the power of AI and user taste profiles to deliver commentary that feels like it was made just for you.

## What I Learned

- **Integrating LLMs for Real-Time Tasks:** I learned how to use large language models (LLMs) to generate natural, context-aware sports commentary on the fly, adapting to different user styles.
- **Streaming Data with Flask & SSE:** Implementing Server-Sent Events (SSE) in Flask taught us about real-time data streaming and the challenges of keeping the UI in sync with backend events.
- **Prompt Engineering:** Crafting prompts that reliably produce specific, non-generic outputs from LLMs is both an art and a science. I iterated on our prompts to ensure the AI used real player and team names, not placeholders.
- **User Experience:** I explored how to make the UI intuitive, visually appealing, and responsive to live updates.

## How I Built It

- **Backend:**
  - Built with Python and Flask, simulating a live football match with a sequence of events.
  - Commentary is generated for each event using an LLM (e.g., OpenAI, Gemini), with prompts tailored to the user's selected style (analytical, emotional, humorous, or balanced).
  - Commentary is streamed to the frontend in real time using SSE.
  - Text-to-speech (TTS) integration (EdgeTTS, gTTS, or ElevenLabs) can convert commentary to audio.
- **Frontend:**
  - A modern, responsive web UI built with HTML, CSS, and vanilla JavaScript.
  - Users select their preferred commentary style and start the game simulation.
  - Commentary appears live in the UI as soon as it is generated.
- **Personalization:**
  - User taste profiles are simulated via a mock Qloo API, influencing the style and focus of the commentary.

## Challenges I Faced

- **Real-Time Streaming in Flask:** Flask's built-in server isn't optimized for SSE, so I had to carefully manage streaming responses and UI updates.
- **Prompt Specificity:** Early LLM outputs were generic and filled with placeholders. I refined our prompts to force the use of actual event data, which greatly improved realism.
- **Synchronizing Audio and Text:** Ensuring that audio playback matched the live commentary stream required careful timing and error handling.
- **Simulating Realistic Events:** Creating a believable sequence of football events with enough metadata for rich commentary was a challenge.
- **User Experience:** Making the UI both beautiful and functional, with instant feedback and no lag, took several iterations.


## Conclusion

QlooSport Sync demonstrates how AI and personalization can transform the sports viewing experience. By combining real-time event simulation, LLM-powered commentary, and user taste profiles, I created a prototype that brings fans closer to the action—on their own terms.

---

