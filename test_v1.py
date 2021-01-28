import speech_recognition as sr
import time

r = sr.Recognizer()
start = time.time()
for t in range(100):
    with sr.AudioFile("sample2.wav") as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ja-JP')
    print(t)
    #print(text)
end_time = time.time() - start
print("end_time:{0}".format(end_time) + "[sec]")