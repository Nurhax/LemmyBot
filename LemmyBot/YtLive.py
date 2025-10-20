import pytchat
import Creds
import random
import time

#Retrieve live chat from YouTube using pytchat
#Ambil menggunakan livestream id
#Video_ID = Creds.LivestreamID

class YoutubeLiveChat:
    def __init__(self) -> None:
        pass

    # Ambil live chat dari youtube per 15 detik
    # Return random message dari chat yang diambil
    def getLiveChat(self):
        chat = pytchat.create(video_id=Creds.LivestreamID)
        collected_messages = []
        start_time = time.time()
        while time.time() - start_time < 15:  # Collect messages for 15 seconds
            messages = [c for c in chat.get().sync_items()]
            collected_messages.extend(messages)
            time.sleep(1)
        if collected_messages:
            msg = random.choice(collected_messages)
            return msg
        else:
            return None
