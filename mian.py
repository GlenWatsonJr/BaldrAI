import openai
import os
import speech_recognition as sr
from gtts import gTTS
import playsound
import tempfile
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
openai.api_key = os.getenv("openaiAPIKey")

# Initialize speech recognizer
r = sr.Recognizer()

# Additional context for AI responses
additional_context = "You are a helpful assistant called BaldrAI. Please provide concise and clear answers, but also be funny. Use as few words as possible, but be meaningful. Act as real as possible even though you are an AI."

def chat_with_gpt(prompt):
    """
    Function to interact with GPT-3.5-turbo model using OpenAI API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": additional_context},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

def speak(text):
    """
    Converts text to speech using gTTS and plays the audio.
    """
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
            temp_audio_path = temp_audio.name
            tts.save(temp_audio_path)
            playsound.playsound(temp_audio_path)
    except Exception as e:
        print(f"Speech synthesis error: {e}")

def main():
    """
    Continuously listens for "prompt" and responds using GPT.
    """
    print("BaldrAI is now listening... Say 'prompt' to activate.")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise
        while True:
            try:
                print("Listening...")
                audio = r.listen(source)
                user_input = r.recognize_google(audio).lower()
                print(f"You said: {user_input}")

                if "prompt" in user_input:
                    print("Keyword detected. Please speak your question.")
                    audio = r.listen(source)  # Capture next speech input
                    user_query = r.recognize_google(audio).lower()
                    print(f"You: {user_query}")

                    if user_query in ["quit", "exit", "bye"]:
                        print("Goodbye!")
                        break

                    # Get GPT response
                    response = chat_with_gpt(user_query)
                    print(f"GPT: {response}")

                    # Speak the response
                    speak(response)

            except sr.UnknownValueError:
                print("Could not understand audio, please try again.")
            except sr.RequestError as e:
                print(f"Speech recognition service error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()