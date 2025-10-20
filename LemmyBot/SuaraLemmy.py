
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import Creds
import os
import requests

class SuaraElevenLabs:
    def __init__(self) -> None:
        pass

    def playSuaraLemmy(self, textCharAI):
        os.environ['PATH'] += os.pathsep + Creds.PathFFMPEG
        client = ElevenLabs(api_key=Creds.APIKeyEleven)

        # Check credits using ElevenLabs REST API
        try:
            response = requests.get(
                "https://api.elevenlabs.io/v1/user",
                headers={"xi-api-key": Creds.APIKeyEleven}
            )
            response.raise_for_status()
            user_info = response.json()
            used = user_info.get("subscription", {}).get("character_count", 0)
            maxChar = user_info.get("subscription", {}).get("character_limit", 10000)
            if maxChar - used < 1000:
                print(f"WARNING: ElevenLabs credits are low ({maxChar - used} remaining)")
            else:
                print(f"ElevenLabs credits: {maxChar - used} characters remaining")
        except Exception as e:
            print(f"Could not check ElevenLabs credits: {e}")

        # Suara lemmy, yang bisa diganti sesuai kebutuhan
        audioLemmy = client.generate(
            text=textCharAI,
            voice=Creds.SuaraLemmyID,
            model="eleven_multilingual_v2"
        )
        play(audioLemmy)
