import os
import openai
import pyttsx3
import speech_recognition as sr

# --- API sozlamalari ---
openai.api_key = "YOUR_OPENAI_API_KEY"  # <<< Bu yerga o'zingizning API kalitingizni yozing

# --- Ovoz chiqaruvchi sozlamalari ---
engine = pyttsx3.init()
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# --- Ovoz eshitish funksiyasi ---
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Gapiring...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='ru-RU')  # yoki 'uz-UZ' agar ishlasa
        print("🧑 Siz dedingiz:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("❌ Tushunmadim, iltimos qaytaring.")
        return ""
    except sr.RequestError:
        speak("❌ Ovoz xizmatida xatolik yuz berdi.")
        return ""

# --- GPT bilan javob olish ---
def get_gpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # yoki gpt-4 agar sizda ruxsat bo‘lsa
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xatolik: {str(e)}"

# --- Asosiy jarayon ---
def main():
    speak("Salom! Men Jarvis. Gapiring.")
    while True:
        command = listen()
        if not command:
            continue
        if "to'xta" in command or "chiq" in command or "stop" in command:
            speak("Xayr!")
            break
        javob = get_gpt_response(command)
        speak(javob)

if __name__ == "__main__":
    main()
