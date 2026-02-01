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

    def get_speaking_item_id(self):
        """Helper to get the item ID of the speaking avatar for animation."""
        if not self.ws: return None
        try:
            resp = self.ws.call(requests.GetSceneItemId(
                sceneName=self.sceneName, sourceName=self.Speaking_Lemmy
            ))
            return resp.getSceneItemId()
        except Exception:
            return None

    def set_speaking_bounce(self, item_id, base_transform, bounce_offset):
        """
        Sets the positionY to base_transform['positionY'] - bounce_offset
        """
        if not self.ws or not item_id: return
        
        try:
            # Ensure we use standard Python float for JSON serialization
            new_y = float(base_transform['positionY'] - bounce_offset)
            
            self.ws.call(requests.SetSceneItemTransform(
                sceneName=self.sceneName, 
                sceneItemId=item_id,
                sceneItemTransform={
                    'positionX': base_transform['positionX'],
                    'positionY': new_y
                }
            ))
        except Exception as e:
            print(f"DEBUG: Error setting bounce: {e}")

    def get_transform(self, item_id):
        if not self.ws or not item_id: return None
        try:
            resp = self.ws.call(requests.GetSceneItemTransform(
                sceneName=self.sceneName, sceneItemId=item_id
            ))
            return resp.getSceneItemTransform()
        except Exception as e:
            print(f"DEBUG: Error getting transform: {e}")
            return None

    def set_speaking_contrast(self, contrast_val):
        """
        Sets the 'contrast' filter setting for the speaking source.
        Assumes a filter named 'Color Correction' exists on the source.
        """
        if not self.ws: return
        
        try:
            # Note: The filter name must match EXACTLY what is in OBS.
            # Standard name is "Color Correction".
            self.ws.call(requests.SetSourceFilterSettings(
                sourceName=self.Speaking_Lemmy,
                filterName="Color Correction", 
                filterSettings={
                    "contrast": float(contrast_val)
                },
                overlay=True # overlay=True updates only the keys provided
            ))
        except Exception as e:
            # Use a quieter error since filter might not exist
            # print(f"DEBUG: Error setting contrast: {e}") 
            pass
