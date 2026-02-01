
import asyncio
import edge_tts
import Creds
import os
import subprocess
import numpy as np
from pydub import AudioSegment
import pyaudio
import time

# Helper: Configure pydub to use the ffmpeg path from Creds
if hasattr(Creds, 'PathFFMPEG') and Creds.PathFFMPEG:
    if os.path.isfile(Creds.PathFFMPEG):
        AudioSegment.converter = Creds.PathFFMPEG
    elif os.path.isdir(Creds.PathFFMPEG):
        AudioSegment.converter = os.path.join(Creds.PathFFMPEG, "ffmpeg.exe")

class SuaraElevenLabs:
    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()

    def __del__(self):
        self.p.terminate()

    async def playSuaraLemmy(self, textCharAI, obs_client=None):
        # Indonesian female voice (free, via Edge TTS)
        VOICE = "id-ID-GadisNeural"
        OUTPUT_FILE = "response.mp3"

        # Generate audio
        try:
            communicate = edge_tts.Communicate(textCharAI, VOICE)
            await communicate.save(OUTPUT_FILE)
        except Exception as e:
            print(f"Error generating audio with edge-tts: {e}")
            return

        # Prepare for playback and animation
        try:
            # Load audio with pydub
            audio_segment = AudioSegment.from_mp3(OUTPUT_FILE)
            
            # Ensure 16-bit PCM for simple processing
            audio_segment = audio_segment.set_sample_width(2)
            # audio_segment = audio_segment.set_frame_rate(44100) # Optional: force rate
            
            # Setup PyAudio stream
            stream = self.p.open(format=self.p.get_format_from_width(audio_segment.sample_width),
                                 channels=audio_segment.channels,
                                 rate=audio_segment.frame_rate,
                                 output=True)

            # Setup Animation Data
            chunk_length_ms = 50 # 50ms chunks = 20 update per second
            chunks = make_chunks(audio_segment, chunk_length_ms)
            
            # Prepare OBS
            speaking_item_id = None
            base_transform = None
            if obs_client:
                speaking_item_id = obs_client.get_speaking_item_id()
                if speaking_item_id:
                    base_transform = obs_client.get_transform(speaking_item_id)

            # Playback Loop
            max_offset = 60 # Pixels to pop up
            
            for chunk in chunks:
                # 1. Write audio to stream (blocking-ish, but fast enough for small chunks)
                data = chunk.raw_data
                stream.write(data)

                # 2. Analyze loudness (RMS)
                # Convert raw bytes to numpy array of int16
                audio_data = np.frombuffer(data, dtype=np.int16)
                if len(audio_data) == 0: continue
                
                # Use float32 to avoid int16 overflow during squaring
                rms = np.sqrt(np.mean(audio_data.astype(np.float32)**2))
                
                # Normalize. 16-bit max is 32768.
                # Silence is usually < 100 or so. Speech is 500-10000 range.
                # Let's simple clamp/scale
                max_val = 5000 
                ratio = min(rms / max_val, 1.0)
                
                # Apply non-linear curve (so small sounds don't jitters too much)
                # "not too high" -> Reduced max_offset from 60 to 15
                max_offset = 15
                
                # Logic: Standard Pop-up for bounce (or can do the flip if requested, but "not too high" 
                # usually implies standard direction but constrained).
                # Let's go with standard UP bounce for now, as it's safer.
                bounce_val = (ratio ** 1.2) * max_offset

                # Contrast logic:
                # "talking loudly then the contrast should be near 0" -> Ratio 1.0 => 0
                # "speaks quietly then it should be near -2"         -> Ratio 0.0 => -2
                # Formula: contrast = -2 + (ratio * 2) = -2 * (1 - ratio)
                contrast_val = -2.0 * (1.0 - ratio)

                # 3. Update OBS
                if obs_client:
                    if speaking_item_id and base_transform:
                         obs_client.set_speaking_bounce(speaking_item_id, base_transform, bounce_val)
                    
                    obs_client.set_speaking_contrast(contrast_val)

            # Cleanup Stream
            stream.stop_stream()
            stream.close()

            # Reset OBS position and contrast
            if obs_client:
                if speaking_item_id and base_transform:
                    obs_client.set_speaking_bounce(speaking_item_id, base_transform, 0)
                obs_client.set_speaking_contrast(0) # Reset to normal? Or -2? 
                # Usually reset to 'normal' (0) or the 'idle' state. 
                # If she stops speaking, she goes to Idle Image anyway, so this affects the Talking source.
                # Resetting to 0 ensures if we reuse the source it starts normal.
                 
        except Exception as e:
            print(f"Error play/animating audio: {e}")
        
        # Clean up file
        if os.path.exists(OUTPUT_FILE):
            try:
                os.remove(OUTPUT_FILE)
            except:
                pass

def make_chunks(audio_segment, chunk_length):
    """
    Breaks an AudioSegment into chunks that are <chunk_length> milliseconds long.
    if chunk_length is 50 then you'll get a list of 50 millisecond long audio
    segments.
    """
    number_of_chunks = len(audio_segment) // chunk_length
    chunks = [audio_segment[i * chunk_length:(i + 1) * chunk_length]
              for i in range(number_of_chunks)]
    # Add the remainder
    if len(audio_segment) % chunk_length > 0:
        chunks.append(audio_segment[number_of_chunks * chunk_length:])
    return chunks
