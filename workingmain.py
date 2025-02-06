import openai
import os
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import speech_recognition as sr
import keyboard  # To handle button press

load_dotenv()

# Set up OpenAI and ElevenLabs API keys 
openai.api_key = os.getenv("openaiAPIKey")
client = ElevenLabs(
    api_key= os.getenv("elevenlabsAPIKey")
)

# Initialize the speech recognizer
r = sr.Recognizer()

# Add context for the prompt
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

def main():
    """
    Main function to handle speech-to-text and text-to-speech chat interaction.
    """
    print("Welcome to the GPT chatbot!")
    print("Press and hold the 'M' key to activate the microphone.")
    print("Release the 'M' key when you finish speaking.")
    print("Type 'quit', 'exit', or 'bye' to end the chat.")

    listening = False  # To track whether we're in listening mode

    while True:
        try:
            # Wait for the user to press the 'M' key to start or stop the question asking
            print("Press 'm' to start asking a question, press 'm' again when done.")
            keyboard.wait("m")  # Wait until the 'M' key is pressed

            if not listening:
                print("You pressed 'm'. Ask a question now!")
                listening = True
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening... Speak now!")
                    audio = r.listen(source)

                # Recognize speech using Google Speech Recognition
                user_input = r.recognize_google(audio).lower()
                print(f"You: {user_input}")

                # Check for exit condition
                if user_input in ["quit", "exit", "bye"]:
                    print("Goodbye!")
                    break

                # Combine additional context with the user's input
                full_prompt = f"{additional_context}\n\nUser Input: {user_input}"

                # Get GPT response
                response = chat_with_gpt(full_prompt)
                print(f"GPT: {response}")

                # Convert GPT response to speech using ElevenLabs
                audio = client.generate(
                    text=response,
                    voice="Daniel",
                    model="eleven_multilingual_v2"
                )
                play(audio)

            else:
                # Once the user presses 'm' again, we stop listening
                print("You pressed 'm' again. Done asking!")
                listening = False

        except sr.UnknownValueError:
            print("Sorry, I could not understand your speech. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from the speech recognition service; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()