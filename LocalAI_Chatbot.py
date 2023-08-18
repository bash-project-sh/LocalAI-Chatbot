import os, requests, json
import pyaudio, wave
import sounddevice as sd

SoundPath = os.getcwd() + "\Audio\TempAudio.wav"

def TextBot(Message):
    LocalAI = "http://127.0.0.1:8080/v1/chat/completions"
    Headers = {"Content-Type": "application/json"}
    Message = json.dumps({'model': 'ggml-gpt4all-j', 'messages': [{"role": "user", "content": "" + Message}], 'temperature': 0.9}, indent=4, separators=(',', ': '))
    Response = requests.post(url=LocalAI, headers=Headers, data=Message)
    Response = json.loads(Response.text)
    print(Response['choices'][0]['message']['content'])
    return Response['choices'][0]['message']['content']

def TTS(Text):
    LocalAI = "http://127.0.0.1:8080/tts"
    Headers = {"Content-Type": "application/json"}
    Message = json.dumps({"model":"en-us-amy-low.onnx", "input": "" + Text})
    Media = requests.post(url=LocalAI, headers=Headers, data=Message)
    with open(SoundPath, 'wb') as Sound:
        Sound.write(Media.content)
    Sound.close()
    
    with wave.open(SoundPath, 'rb') as WaveFile:
        PlayAduio = pyaudio.PyAudio()
        Stream = PlayAduio.open(format=PlayAduio.get_format_from_width(WaveFile.getsampwidth()), channels=WaveFile.getnchannels(), rate=WaveFile.getframerate(), output=True, output_device_index=None)
        while len(data := WaveFile.readframes(1024)):
            Stream.write(data)
        Stream.close
        PlayAduio.terminate()

def SoundDevicesIndex():
    print(sd.query_devices())

if __name__ == "__main__":
    while True:
        Message = str(input("Enter your prompt: "))
        Text = TextBot(Message)
        TTS(Text)
