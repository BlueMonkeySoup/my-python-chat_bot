from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import tkinter as tk

class ColorChatBot():
    def __init__(self, root):
        self.root = root
        self.geometry = self.root.geometry("800x600") 

        self.label1 = tk.Label(root, text="Hello, this is a rgb color bot!\n this does not contains all the colors")
        
        self.label1.pack()

        self.label2 = tk.Label(root, text="1.Enter a singular color example. Red .\n2.show rgb colors \n3.show primary rgb colors \n4.show hexadecimal colors \n5.python copy/paste color codes\n")
        
        self.label2.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()
        
        self.button = tk.Button(self.root, text="Ask color", command=self.ask_name)
        self.button.pack()

        
        self.label = tk.Label(self.root, text="", padx=10, pady=10, font=("Helvetica", 10))
        self.label.pack()

        self.file_path = ("color_code.json")
        self.chatbot = ChatBot('James')
        self.trainer = ListTrainer(self.chatbot)
        self.vectorizer = TfidfVectorizer()
        self.conversation = []
        self.X = None

    def load_files(self):
        with open(self.file_path, "r") as f:
            files = json.load(f)
        return files
    
    def train(self):
        color_data = self.load_files()
        for color in color_data["colors"]:
            self.conversation.append(color["name"])
            self.conversation.append(str(color["value"]))

        for color in color_data["hexadecimal"]:
            self.conversation.append(color["name"])
            self.conversation.append(str(color["value"]))

        self.conversation.append("show rgb")
        self.conversation.append('\n'.join([f"{color['value']}" for color in color_data["colors"]]))

        self.conversation.append("show primary rgb")
        self.conversation.append('\n'.join([f"{color['value']}" for color in color_data["primary"]]))

        self.conversation.append("show hexa")
        self.conversation.append('\n'.join([f"{color['value']}" for color in color_data["hexadecimal"]]))
        
        self.conversation.append("python")
        self.conversation.append('\n'.join([f"{color['value']}" for color in color_data["python_color"]]))
        
        self.conversation.append("python color")
        self.conversation.append('\n'.join([f"{color['value']}" for color in color_data["python_color"]]))

        self.trainer.train(self.conversation)
        self.X = self.vectorizer.fit_transform(self.conversation)

    def ask_name(self):
        user_input = self.entry.get()
        Y = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(Y, self.X)
        response_index = similarities.argmax()
        response = self.chatbot.get_response(self.conversation[response_index])
        response=str(response)
        if len(str(response))>50:
            response=self.split_text(response)
        self.label.config(text=str(response))

    def split_text(self,response:str):
        words = response.split(";")
        lines = []
        line = ""
        for word in words:
            lines.append(word)
        return "\n".join(lines)


root = tk.Tk()
 
app = ColorChatBot(root)
app.train()
root.mainloop()

