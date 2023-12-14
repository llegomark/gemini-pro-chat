import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 4096,
    }

    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }

    global_history = []
    last_saved_index = 0

    while True:
        try:
            model = genai.GenerativeModel('gemini-pro',
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)
            chat = model.start_chat(history=[])

            last_saved_index = add_to_history_and_save(
                global_history, "Session started", "", last_saved_index, new_session=True)

            while True:
                user_input = input("User: ").strip().lower()

                if user_input == "history":
                    display_chat_history(global_history)
                    continue

                if user_input == "restart":
                    save_chat_to_file(
                        global_history[last_saved_index:], "chat_history.txt")
                    last_saved_index = len(global_history)
                    break

                if user_input == "exit":
                    save_chat_to_file(
                        global_history[last_saved_index:], "chat_history.txt")
                    return

                if user_input:
                    response = chat.send_message(user_input, stream=True)
                    response_text = ""
                    for chunk in response:
                        response_text += chunk.text
                        print(chunk.text)

                    last_saved_index = add_to_history_and_save(
                        global_history, user_input, response_text, last_saved_index)
                else:
                    print("Please enter some text.")

        except Exception as e:
            print(f"An error occurred: {e}")


def add_to_history_and_save(history, user_input, response_text, last_saved_index, new_session=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if new_session:
        history.append(
            {'role': 'system', 'text': "--- New Session ---", 'timestamp': timestamp})
    history.extend([
        {'role': 'user', 'text': user_input, 'timestamp': timestamp},
        {'role': 'gemini', 'text': response_text, 'timestamp': timestamp}
    ])
    save_chat_to_file(history[last_saved_index:], "chat_history.txt")
    return len(history)


def display_chat_history(history):
    print("\nComplete Chat History:")
    for message in history:
        sender = "User" if message['role'] == 'user' else "Gemini"
        print(f"{message['timestamp']} {sender}: {message['text']}")
    print("\n")


def save_chat_to_file(history, filename):
    with open(filename, "a", encoding="utf-8") as file:
        for message in history:
            sender = "User" if message['role'] == 'user' else "Gemini"
            file.write(f"{message['timestamp']} {sender}: {message['text']}\n")


if __name__ == "__main__":
    main()
