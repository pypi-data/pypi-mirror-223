import requests
from ovos_plugin_manager.stt import STT


class OVOSAzureSTT(STT):
    def __init__(self, config=None):
        super().__init__(config)
        self.key = self.config.get("key")
        self.region = self.config.get("region", "westeurope")

    def execute(self, audio, language=None):
        lang = language or self.lang
        headers = {
            'Content-type': 'audio/wav;codec="audio/pcm";',
            'Ocp-Apim-Subscription-Key': self.key
        }
        url = f"https://{self.region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        response = requests.request("POST", url, headers=headers,
                                    data=audio.get_wav_data(),
                                    params={"language": lang}).json()
        return response["DisplayText"]


if __name__ == "__main__":
    from speech_recognition import Recognizer, AudioFile
    import os

    engine = OVOSAzureSTT({"key": 'XXX'})

    # inference
    jfk = f"{os.path.dirname(__file__)}/jfk.wav"
    with AudioFile(jfk) as source:
        audio = Recognizer().record(source)

    pred = engine.execute(audio, language="en-us")
    print(pred)
