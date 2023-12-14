import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
import re


class ChatHistoryManager:
    def __init__(self, filename="chat_history.txt", max_file_size_mb=5):
        self.history = []
        self.filename = filename
        self.max_file_size_mb = max_file_size_mb

    def add_message(self, role, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(
            {'role': role, 'text': text, 'timestamp': timestamp})

    def save_to_file(self):
        self._rotate_file_if_needed()
        with open(self.filename, "a", encoding="utf-8") as file:
            for message in self.history:
                file.write(
                    f"{message['timestamp']} {message['role']}: {message['text']}\n")
        self.history.clear()

    def display(self):
        for message in self.history:
            print(
                f"{message['timestamp']} {message['role']}: {message['text']}")

    def _rotate_file_if_needed(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "a", encoding="utf-8") as file:
                pass

        if os.path.getsize(self.filename) > self.max_file_size_mb * 1024 * 1024:
            os.rename(self.filename, self.filename + ".backup")


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set your GEMINI_API_KEY in the environment.")

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }

    history_manager = ChatHistoryManager()
    history_manager.add_message("system", "--- New Session ---")

    model = genai.GenerativeModel(
        'gemini-pro', generation_config=generation_config, safety_settings=safety_settings)
    chat = model.start_chat(history=[])

    while True:
        user_input = input("User: ").strip()
        if not user_input:
            print("Please enter some text.")
            continue

        if user_input.lower() == "history":
            history_manager.display()
            continue

        if user_input.lower() == "restart":
            history_manager.save_to_file()
            os.system('cls' if os.name == 'nt' else 'clear')
            history_manager.add_message("system", "--- New Session ---")
            chat = model.start_chat(history=[])
            continue

        if user_input.lower() == "exit":
            history_manager.save_to_file()
            break

        try:
            response = chat.send_message(user_input, stream=True)
            response_text = ""
            for chunk in response:
                if chunk.text.endswith("."):
                    response_text += chunk.text
                else:
                    response_text += re.sub(r'\s*$', '.', chunk.text)
                print(chunk.text)

            history_manager.add_message("user", user_input)
            history_manager.add_message("gemini", response_text)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
