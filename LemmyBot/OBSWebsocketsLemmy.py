import Creds
from obswebsocket import obsws, requests

#Class OBSWebsocketsLemmy untuk manage obs websocket dan juga toggle scene
class OBSWebsocketsLemmy:
    #inisiasi OBSWebsocketsLemmy dengan memastikan scenename dan asset sesuai
    def __init__(self):
        self.sceneName = "Art Livestream"
        self.Idle_Lemmy = "Lemmy Axioma Idle"
        self.Speaking_Lemmy = "Lemmy Axioma Talking"

        try:
            # `legacy=False` by default (v5 API). If connecting to old server use legacy=True.
            self.ws = obsws(Creds.OBSWebsocketHost, Creds.OBSWebsocketPort, Creds.OBSWebsocketPassword)
            self.ws.connect()
            print("✅ Connected to OBS WebSocket")
        except Exception as e:
            print(f"❌ Failed to connect to OBS WebSocket: {e}")
            self.ws = None

    def disconnect(self):
        if self.ws:
            try:
                self.ws.disconnect()
                print("🔌 Disconnected from OBS WebSocket")
            except Exception as e:
                print(f"⚠️ Error during disconnect: {e}")

    def set_speaking_state(self, speaking: bool):
        if not self.ws:
            print("⚠️ OBS WebSocket not connected.")
            return

        try:
            # Request GetSceneItemId for idle and speaking sources
            resp_idle = self.ws.call(requests.GetSceneItemId(
                sceneName=self.sceneName, sourceName=self.Idle_Lemmy
            ))
            idle_item = resp_idle.getSceneItemId()

            resp_speak = self.ws.call(requests.GetSceneItemId(
                sceneName=self.sceneName, sourceName=self.Speaking_Lemmy
            ))
            speaking_item = resp_speak.getSceneItemId()

            if idle_item is None or speaking_item is None:
                print("⚠️ Could not find scene items.")
                return

            if speaking:
                # Disable idle, enable speaking
                self.ws.call(requests.SetSceneItemEnabled(
                    sceneName=self.sceneName,
                    sceneItemId=idle_item,
                    sceneItemEnabled=False
                ))
                self.ws.call(requests.SetSceneItemEnabled(
                    sceneName=self.sceneName,
                    sceneItemId=speaking_item,
                    sceneItemEnabled=True
                ))
            else:
                # Reverse: disable speaking, enable idle
                self.ws.call(requests.SetSceneItemEnabled(
                    sceneName=self.sceneName,
                    sceneItemId=speaking_item,
                    sceneItemEnabled=False
                ))
                self.ws.call(requests.SetSceneItemEnabled(
                    sceneName=self.sceneName,
                    sceneItemId=idle_item,
                    sceneItemEnabled=True
                ))

        except Exception as e:
            print(f"⚠️ Error while toggling speaking state: {e}")
