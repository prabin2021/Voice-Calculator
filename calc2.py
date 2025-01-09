import tkinter as tk
from tkinter import scrolledtext,ttk
import threading
import speech_recognition as sr
import pyttsx3
import math

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 160)
# Function to make the assistant speak
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen to user input
def listen():
    global stop_listening
    stop_listening = False
    with sr.Microphone() as source:
        while not stop_listening:
            try:
                root.after(0, status_label.config, {"text": "Listening..."})
                audio = recognizer.listen(source, timeout=9, phrase_time_limit=5)
                command = recognizer.recognize_google(audio)
                status_label.config(text=f"You said: {command}")
                result = calculate(command.lower())
                if result is not None:
                    display_text.insert(tk.END, f"You: {command}\n")
                    display_text.insert(tk.END, f"Result: {result}\n\n")
            except sr.WaitTimeoutError:
                status_label.config(text="Listening timed out. Please try again.")
            except sr.UnknownValueError:
                status_label.config(text="Sorry, I didn't understand that. PLease try again")
            except sr.RequestError:
                status_label.config(text="Check your internet connection.")

# Function to perform calculations based on voice commands
def calculate(command):
            # Split command into words and count the operators
        operators = [word for word in command if word in ['+', '-', '*', '/']]
            
            # Check if multiple operators exist
        if len(set(operators)) > 1:
            speak("I detected multiple operations in your command. Please use only one type of operation at a time.")
            result = "Unsupported operation"
            return result
        else:
            try:
                if 'add' in command or 'plus' in command or '+' in command:
                    numbers = [float(n) for n in command.split() if n.replace('.', '', 1).isdigit()]
                    result = sum(numbers)
                
                elif 'subtract' in command or 'minus' in command or '-' in command:
                    numbers = [float(n) for n in command.split() if n.replace('.', '', 1).isdigit()]
                    if 'subtract' in command:
                        result = numbers[1] - numbers[0]
                    else:
                        result = numbers[0] - numbers[1]
                        
                
                elif 'multiply' in command or 'times' in command or '*' in command or 'X' in command or 'x' in command:
                    numbers = [float(n) for n in command.split() if n.replace('.', '', 1).isdigit()]
                    result = numbers[0] * numbers[1]
                
                elif 'divide' in command:
                    numbers = [float(n) for n in command.split() if n.replace('.', '', 1).isdigit()]
                    result = numbers[0] / numbers[1]
                elif 'power' in command or 'raise to' in command:
                    numbers = [float(n) for n in command.split() if n.replace('.', '', 1).isdigit()]
                    result = math.pow(numbers[0], numbers[1])
                elif 'sin' in command:
                    number = float(command.split()[-1])
                    result = math.sin(math.radians(number))
                elif 'cos' in command:
                    number = float(command.split()[-1])
                    result = math.cos(math.radians(number))
                elif 'tan' in command:
                    number = float(command.split()[-1])
                    result = math.tan(math.radians(number))
                elif 'square root' in command:
                    number = float(command.split()[-1])
                    result = math.sqrt(number)
                elif 'square' in command:
                    number = float(command.split()[-1])
                    result = math.pow(number, 2)
                elif 'cube root' in command:
                    number = float(command.split()[-1])
                    result = math.pow(number, 1/3)
                elif 'cube' in command:
                    number = float(command.split()[-1])
                    result = math.pow(number, 3)
                elif 'even' in command or 'odd' in command:
                    numbers = [int(n) for n in command.split() if n.replace('.', '', 1).isdigit()]
                    if len(numbers) == 1:  # Ensure there's exactly one number in the command
                        number = numbers[0]  # Extract the number
                        if number % 2 == 0:
                            result = f" Number {number} is even."
                        else:
                            result = f" Number {number} is odd."
                    else:
                        speak("Please provide exactly one number to check for even or odd.")
                        result = "Invalid"

                elif 'prime' in command or 'composite' in command:
                    numbers = [int(n) for n in command.split() if n.replace('.', '', 1).isdigit()]
                    if len(numbers) == 1:  # Ensure there's exactly one number in the command
                        number = numbers[0]  # Extract the number
                        if number > 1 and all(number % i != 0 for i in range(2, int(math.sqrt(number)) + 1)):
                            result = f" Number {number} is prime."
                        else:
                            result = f" Number {number} is composite."
                    else:
                        speak("Please provide exactly one number to check for prime or composite.")
                        result = "Invalid"
                elif 'hcf' in command or 'HCF' in command or 'Highest Common Factor' in command or 'highest common factor' in command:
                    numbers = [int(n) for n in command.split() if n.isdigit()]
                    result = math.gcd(numbers[0], numbers[1])
                elif 'lcm' in command or 'LCM' in command or 'Lowest Common Multiple' in command or 'lowest common multiple' in command: 
                    numbers = [int(n) for n in command.split() if n.isdigit()]
                    result = (numbers[0] * numbers[1]) // math.gcd(numbers[0], numbers[1])
                
                elif 'percent' in command or 'percentage' in command or '%' in command:
                    try:
                        # Preprocess the command to handle attached '%' symbols
                        command = command.replace('percent', '%')  # Normalize 'percent' to '%'
                        command = command.replace('%', ' %')  # Add a space before '%'

                        # Extract numbers from the command
                        words = command.split()
                        numbers = [float(word.replace('%', '')) for word in words if word.replace('.', '', 1).replace('%', '').isdigit()]

                        if len(numbers) == 2:
                            percentage, total = numbers
                            result = (percentage / 100) * total
                        else:
                            speak("I couldn't understand the percentage calculation. Please try again with a command like '10 percent of 50'.")
                            result = "Invalid"
                    except Exception:
                        speak("There was an error in the percentage calculation.")
                        result = "Invalid"


                else:
                    speak("I can only perform basic calculations and trigonometric functions.")
                    return None
                speak(f"The result is {result}")
                return result
            except Exception as e:
                speak("There was an error with your calculation.")
                return None

def start_listening():
    threading.Thread(target=listen).start()

def stop_listening():
    global stop_listening
    stop_listening = True
    status_label.config(text="Listening Stopped.")

def clear_conversation():
    display_text.delete(1.0, tk.END)
    status_label.config(text="Conversation Cleared.")

# Create the main tkinter window
root = tk.Tk()
root.title("Voice Calculator")
root.geometry("700x600")
root.configure(bg="#1e1e2e")
# Display area for conversation
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 12, "bold"), background="YELLOW", foreground="BLACK", padding=10)
style.map("TButton", background=[("active", "RED")])
style.configure("TLabel", background="CYAN", foreground="BLACK", font=("Arial", 12))
style.configure("TScrolledText", font=("Arial", 12), background="#2e2e3e", foreground="white")

# Display area for conversation
display_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25, bg="WHITE", fg="BLACK", font=("Arial", 12))
display_text.pack(pady=10)

# Buttons to control the application
button_frame = ttk.Frame(root)
button_frame.pack()

start_button = ttk.Button(button_frame, text="Start Listening", command=start_listening)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(button_frame, text="Stop Listening", command=stop_listening)
stop_button.pack(side=tk.LEFT, padx=10)

clear_button = ttk.Button(button_frame, text="Clear Conversation", command=clear_conversation)
clear_button.pack(side=tk.LEFT, padx=10)

# Label to display status
status_label = ttk.Label(root, text="Welcome to Voice Calculator!")
status_label.pack(pady=20)
# Run the tkinter main loop
speak("Welcome to the voice calculator. Please say a command.")
root.mainloop()