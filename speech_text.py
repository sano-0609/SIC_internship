import speech_recognition as sr
import time

r = sr.Recognizer()
start = time.time()
with sr.AudioFile("./hls/l_00002.ts") as source:
    audio = r.record(source)
text = r.recognize_google(audio, language='ja-JP')
print(text)
end_time = time.time() - start
print("end_time:{0}".format(end_time) + "[sec]")
