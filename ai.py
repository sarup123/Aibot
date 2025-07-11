import os
import openai
import speech_recognition as sr
from gtts import gTTS
import playsound
import tempfile
from flask import Flask, jsonify

openai.api_key = "your-openai-api-key"

app = Flask(__name__)

def listen_to_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        print("🧠 Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand you."
    except sr.RequestError:
        return "Speech recognition service is down."

def talk_to_openai(prompt):
    print("🧠 Talking to OpenAI...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    reply = response.choices[0].message.content
    print(f"🤖 GPT says: {reply}")
    return reply

def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        playsound.playsound(fp.name)

@app.route("/ask", methods=["GET"])
def ask_assistant():
    user_input = listen_to_microphone()
    gpt_reply = talk_to_openai(user_input)
    speak_text(gpt_reply)
    return jsonify({"question": user_input, "answer": gpt_reply})

if __name__ == "__main__":
    app.run(debug=True)
