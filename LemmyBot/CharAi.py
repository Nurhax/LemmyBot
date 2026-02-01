from PyCharacterAI import Client
from PyCharacterAI.exceptions import SessionClosedError
import Creds
import SuaraLemmy
import keyboard
import YtLive
import OBSWebsocketsLemmy
import speech_recognition as sr

#Class utama untuk CharAI dalam menjalankan loop chat
class CharAI:
    def __init__(self) -> None:
        pass

    # Inisiasi CharAI Default
    # CharID = CharID Lemmy
    # TokenID = TokenIDCharAI
    async def startCharAIDefault(self):
        #Inisiasi semua class yang dibutuhkan
        ElevenLemmy = SuaraLemmy.SuaraElevenLabs()
        yt_chat = YtLive.YoutubeLiveChat()
        OBSClient = OBSWebsocketsLemmy.OBSWebsocketsLemmy()
        char_id = Creds.CharIDLemmy

        client = Client()
        try:
            # start a chat session (so we have chat_id)
            await client.authenticate(Creds.TokenIDCharAI)
            me = await client.account.fetch_me()
            chat, greeting_Message = await client.chat.create_chat(char_id)
            beginPrompt = "Kamu adalah Lemmy Axioma, seorang virtual assistant yang ceria dan membantu. Kamu berbicara dalam bahasa Indonesia. Jawab dengan singkat dan jelas. Kamu sangat suka matematika dan teknologi. Kamu juga suka bermain game dan membaca buku fiksi ilmiah."
            await client.chat.send_message(char_id, chat.chat_id, beginPrompt)

            #Main loop chat
            while True:
                print("[Nurhax]: ", end="", flush=True)
                message = None

                # F for speech-to-text, L for manual text, else YouTube chat
                print("Press 1 for Speech-to-Text, 2 for Manual Input, or wait for YouTube Chat (Press Q to quit):")
                
                pressed_key = keyboard.read_key()
                
                if pressed_key == '1':
                    print("[Speech-to-Text mode]")
                    recognizer = sr.Recognizer()
                    with sr.Microphone() as source:
                        print("Silakan bicara...")
                        audio = recognizer.listen(source)
                    try:
                        message = recognizer.recognize_google(audio, language="id-ID")
                        print(f"[Nurhax]: {message}")
                    except Exception as e:
                        print(f"Speech recognition error: {e}")
                        continue
                elif pressed_key == '2':
                    print("Enter message manually:")
                    message = input()
                elif pressed_key == '3':
                    print("[Mengambil pesan dari YouTube Live Chat]")
                    yt_msg = yt_chat.getLiveChat()
                    if yt_msg:
                        message = yt_msg.message
                        print(f"[{yt_msg.author.name}]: {message}")
                    else:
                        print("Tidak ada pesan YouTube yang tersedia.")
                        continue
                elif pressed_key.lower() == 'q':
                    raise SessionClosedError()
                else:
                    continue
                # keluar dari loop jika pesan adalah "\" atau mengandung kata perpisahan

                # kirim pesan ke CharacterAI dan dapatkan balasannya
                answer = await client.chat.send_message(char_id, chat.chat_id, message)
                reply_text = answer.get_primary_candidate().text

                print(f"[Lemmy Axioma]: {reply_text}")
                OBSClient.set_speaking_state(True)
                await ElevenLemmy.playSuaraLemmy(reply_text, obs_client=OBSClient)
                OBSClient.set_speaking_state(False)

        except SessionClosedError:
            print(f"[Lemmy]: session closed. Sampai Nanti!")
            await ElevenLemmy.playSuaraLemmy("session closed. Sampai Nanti!", obs_client=OBSClient)

        finally:
            # Tutup session client sama websocket OBS
            await client.close_session()
            OBSClient.disconnect()
