
# LemmyBot

LemmyBot is a professional livestream assistant designed to enhance your YouTube streaming experience. It intelligently interacts with your audience, responds to donation messages, and engages with random chat messages, all while synchronizing with your OBS PNGTuber for a dynamic and immersive presentation.

---

## ⚠️ Disclaimer
**LemmyBot uses unofficial APIs and external services.**
Please ensure you comply with all relevant platform terms of service. Use at your own risk, especially for public or sensitive streams.

---

## Features
- **Speech-to-Text Integration:** Seamlessly chat with your chosen Character AI using your voice.
- **Live Chat Engagement:** Respond to random or selected YouTube livestream chat messages in real time.
- **Donation Message Handling:** Automatically reply to donation messages for increased audience interaction.
- **Dynamic Character Modeling:** LemmyBot adapts its personality using CharacterAI and its voice using Microsoft Edge TTS.
- **OBS WebSocket Control:** Synchronizes Lemmy's speaking and idle states with your PNGTuber in OBS for lifelike reactions.

---

## Technology Stack
- **Microsoft Edge TTS:** High-quality text-to-speech for Lemmy's voice (Free).
- **YouTube Live Chat API (Unofficial):** Real-time chat message retrieval.
- **CharacterAI API (Unofficial):** Personality-driven AI chat responses.
- **OBS WebSockets:** Scene and PNGTuber control for visual feedback.
- **SpeechRecognition & PyAudio:** Converts spoken input to text for interactive conversations.

---

## Setup Instructions
1. **Credentials:**
	- Create a Python file (`Creds.py`) containing your YouTube Livestream ID, CharacterAI API key, and relevant character IDs.
2. **OBS & PNGTuber:**
	- Install and configure OBS WebSockets.
	- Set up your PNGTuber sources and ensure scene/item names match your configuration.
3. **Dependencies:**
	- Install required Python packages: `pytchat`, `obswebsocket`, `SpeechRecognition`, `pyaudio`, `requests`, `edge-tts`, etc.
4. **Run LemmyBot:**
	- Execute `Lemmy.py` to start the assistant and begin interacting with your livestream audience.

---

## Professional Notes
- LemmyBot is modular and extensible—customize character models, voice settings, and chat logic to fit your brand.
- All API usage is subject to change; monitor for updates and maintain your credentials securely.
- For best results, test in a private stream before deploying publicly.

---

## License & Credits
This project is for educational and entertainment purposes. All trademarks and API services are property of their respective owners.
