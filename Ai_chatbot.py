from tkinter import *
import tkinter as tk
import speech_recognition as sr
import pyttsx3
from tkinter import messagebox
import re
from PyDictionary import PyDictionary

# Initialize text-to-speech engine and dictionary API
engine = pyttsx3.init()
dictionary = PyDictionary()
chat = []  # Stores the conversation history

# Function to recognize speech and convert it to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Listen for audio with a timeout
            text = recognizer.recognize_google(audio)  # Use Google API for speech recognition
            print(f"Recognized Speech: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return "Error: Unrecognized speech"
        except sr.RequestError:
            print("Error connecting to the speech recognition service.")
            return "Error: API connection issue"

# Function to check if the input text is a mathematical question
def is_math_question(text):
    return re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', text.strip()) is not None

# Function to solve a basic math question using eval (note: be cautious with eval for security)
def solve_math_question(expression):
    try:
        result = eval(expression)
        return f"The answer is: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to fetch the meaning of a word using the dictionary API
def get_word_meaning(word):
    meaning = dictionary.meaning(word)
    if meaning:
        result = ""
        for key, definitions in meaning.items():
            result += f"{key}:\n"
            for i, definition in enumerate(definitions[:3], 1):  # Limiting to 3 definitions
                result += f"  {i}. {definition}\n"
        return result
    else:
        return "Sorry, I couldn't find the meaning of that word."

# Function to generate appropriate responses based on input text
def ai_greeting(text):
    if "hello" in text.lower():
        return "Hello! How can I assist you today?"
    elif "hey" in text.lower():
        return "Hey! How can I assist you?"
    elif "name" in text.lower():
        return "I'm an AI system here to help you! My name is Jarvis."
    elif "how are you" in text.lower():
        return "I'm Good, thanks for asking, How can I help?"
    elif is_math_question(text):  # Checks if the text is a math question
        return solve_math_question(text)
    elif "define" in text.lower() or "meaning of" in text.lower():  # Checks if a word meaning is requested
        word = text.lower().replace("define", "").replace("meaning of", "").strip()
        return get_word_meaning(word)
    else:
        return "I don't understand that. Can you ask something else?"

# Wrapper function to get AI response
def ai_response(text):
    return ai_greeting(text)

# Function to convert AI text response to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle the send button action and add user input to chat
def send(event=None):
    user_input = search_text_bar.get("1.0", END).strip()  # Get user input from text bar
    if user_input:
        search_text_bar.delete("1.0", END)  # Clear text bar after input
        chat.append(f"You: {user_input}")
        response = ai_response(user_input)  # Get response from AI
        chat.append(f"AI: {response}\n")
        update_chat_history()  # Update chat display
        speak_text(response)  # Speak out the response

# Function to update the chat display with the current conversation history
def update_chat_history():
    chat_display.delete("1.0", END)
    for line in chat:
        chat_display.insert(END, f"{line}\n")

# Function to activate voice recognition for user input
def run_voice_recognition():
    speak_text("Hi, I'm Jarvis. What can I help you with?")
    recognized_text = recognize_speech()  # Capture speech input
    if recognized_text and "Error" not in recognized_text:
        result_label.config(text=f"Recognized: {recognized_text}")
        chat.append(f"You (Voice): {recognized_text}")
        response = ai_response(recognized_text)  # Get AI response
        chat.append(f"AI: {response}\n")
        update_chat_history()
        speak_text(response)
    else:
        messagebox.showerror("Error", "Failed to recognize speech or connect to the API")

# Function to clear the chat history
def clear_chat():
    chat.clear()
    chat_display.delete("1.0", END)

# Main window setup
window = Tk()
window.geometry("500x500+700+250")  # Set window size and position
window.title("AI Chatbot")
window.config(bg="#011627")

# Header label setup
header_label = Label(window, text="AI CHATBOT", font=("Arial", 20, "bold"), fg="white", bg="#011627")
header_label.pack(side='top', pady=10)

# Middle frame setup for displaying chat history
middle_frame = Frame(window, width=470, height=300, bg="#011627")
chat_display = Text(middle_frame, wrap=WORD, width=50, height=14, font=("Arial", 12))
chat_display.pack(side=LEFT, pady=5)

# Scrollbar setup for chat display
chat_display_scroll = Scrollbar(middle_frame, command=chat_display.yview)
chat_display_scroll.pack(side=RIGHT, fill=Y)
chat_display.config(yscrollcommand=chat_display_scroll.set)
middle_frame.pack(pady=10)

# Result label for voice recognition
result_label = tk.Label(window, text="", font=("Arial", 12), bg="#011627", fg="white")
result_label.pack(pady=10)

# Bottom frame setup with input and control buttons
bottom_frame = Frame(window, width=490, height=65, bg="#011627")
search_text_bar = Text(bottom_frame, width=33, height=1, font=("Arial", 12), bg="#EFEFEF")
search_text_bar.place(x=7, y=8)
search_text_bar.bind("<Return>", send)  # Binds the Enter key to send

# Send button setup
send_button = Button(bottom_frame, text="Send", font=("Arial", 12, "bold"), width=6, height=1, bg="#15b097", fg="white", command=send)
send_button.place(x=330, y=8)

# Voice button for activating voice recognition
voice_button = Button(bottom_frame, text="🎙️", font=("Arial", 12, "bold"), width=6, height=1, bg="#15b097", fg="white", command=run_voice_recognition)
voice_button.place(x=410, y=8)
bottom_frame.pack(side='bottom', pady=10)

# Clear chat button
clear_button = Button(window, text="Clear Chat", font=("Arial", 10), bg="#15b097", fg="white", command=clear_chat)
clear_button.pack()

# Start the main loop for the Tkinter window
window.mainloop()
