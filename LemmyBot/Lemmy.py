#Project name LemmyBot
#Text To Speech Pake API ElevenLabs
#Buat AI modelnya sementara pake API unofficial di github: https://github.com/Xtr4F/PyCharacterAI
#Kemungkinan pakai websockets OBS biar lemmy gerak sesuai suaranya
#Pakai API Saweria/Trakteer Buat Dapetin Messagenya -> Lemmy/Hanekawa Jawab Sesuai Context (Text) -> Suara Pakai Elevenlabs -> Play Audio -> Delete Audio
import CharAi
import asyncio

#Mulai Virtual Assistantnya
testing = CharAi.CharAI()
asyncio.run(testing.startCharAIDefault())
