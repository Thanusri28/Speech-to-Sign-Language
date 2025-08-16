import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import os
import string

# Define the path to the folder containing GIFs
gif_folder_path = r'C:\Users\91964\OneDrive\Desktop\Automatic-Indian-Sign-Language-Translator-ISL-master\Automatic-Indian-Sign-Language-Translator-ISL-master\ISL_Gifs'

# Function to display the corresponding GIF for recognized sign language
def display_gif(word):
    class ImageLabel(tk.Label):
        def load(self, im):
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []

            try:
                for i in count(1):
                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(i)
            except EOFError:
                pass

            try:
                self.delay = im.info['duration']
            except:
                self.delay = 100

            if len(self.frames) == 1:
                self.config(image=self.frames[0])
            else:
                self.next_frame()

        def unload(self):
            self.config(image=None)
            self.frames = None

        def next_frame(self):
            if self.frames:
                self.loc += 1
                self.loc %= len(self.frames)
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)

    # Path to the GIF file in the specified folder
    gif_path = os.path.join(gif_folder_path, f'{word}.gif')

    print(f"Looking for GIF in: {gif_folder_path}")
    print(f"Files in directory: {os.listdir(gif_folder_path)}")

    if os.path.exists(gif_path):
        print(f"Found GIF: {gif_path}")
        root = tk.Toplevel()
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load(gif_path)
        root.mainloop()
    else:
        print(f"No matching GIF found for '{word}'")

# Function to recognize speech and display the matching GIF
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening...")
        audio = r.listen(source)

        try:
            recognized_text = r.recognize_google(audio).lower()
            print(f'You Said: {recognized_text}')

            # Remove punctuation from the recognized text
            for c in string.punctuation:
                recognized_text = recognized_text.replace(c, "")

            # Display the GIF if the filename matches recognized_text.gif
            display_gif(recognized_text)
                
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

# GUI setup for button interface
def setup_gui():
    root = tk.Tk()
    root.title("Hearing Impairment Assistant")

    # Create a button to activate speech recognition
    listen_button = tk.Button(root, text="Start Listening", command=recognize_speech, height=3, width=20, bg='lightblue')
    listen_button.pack(pady=20)

    # Exit button to close the program
    exit_button = tk.Button(root, text="Exit", command=root.quit, height=3, width=20, bg='lightgrey')
    exit_button.pack(pady=20)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    setup_gui()
