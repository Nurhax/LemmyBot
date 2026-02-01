
import asyncio
import edge_tts
import Creds
import os
import subprocess

class SuaraElevenLabs:
    def __init__(self) -> None:
        pass

    async def playSuaraLemmy(self, textCharAI):
        # Indonesian female voice (free, via Edge TTS)
        VOICE = "id-ID-GadisNeural"
        OUTPUT_FILE = "response.mp3"

        # Locate ffplay based on Creds.PathFFMPEG
        ffmpeg_invoker = "ffplay" # Default to system path
        if hasattr(Creds, 'PathFFMPEG') and Creds.PathFFMPEG:
            ffmpeg_path_file = Creds.PathFFMPEG
            # If it points to ffmpeg.exe, get the dir and point to ffplay.exe
            if os.path.isfile(ffmpeg_path_file):
                ffmpeg_dir = os.path.dirname(ffmpeg_path_file)
                candidate = os.path.join(ffmpeg_dir, "ffplay.exe")
                if os.path.exists(candidate):
                    ffmpeg_invoker = candidate
            elif os.path.isdir(ffmpeg_path_file):
                candidate = os.path.join(ffmpeg_path_file, "ffplay.exe")
                if os.path.exists(candidate):
                    ffmpeg_invoker = candidate

        # Generate audio
        try:
            communicate = edge_tts.Communicate(textCharAI, VOICE)
            await communicate.save(OUTPUT_FILE)
        except Exception as e:
            print(f"Error generating audio with edge-tts: {e}")
            return

        # Play audio (blocking)
        try:
            # -nodisp: No graphical window
            # -autoexit: Close after playing
            # -hide_banner: Less output
            subprocess.run([ffmpeg_invoker, "-nodisp", "-autoexit", "-hide_banner", OUTPUT_FILE], check=True)
        except Exception as e:
            print(f"Error playing audio: {e}")
            print(f"Make sure ffplay is available at or near {Creds.PathFFMPEG}")
        
        # Clean up
        if os.path.exists(OUTPUT_FILE):
            try:
                os.remove(OUTPUT_FILE)
            except:
                pass
