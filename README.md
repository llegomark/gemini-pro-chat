## Gemini Pro Chat Application

This Python application utilizes the Gemini Pro API from `google.generativeai` to create an interactive chat interface. It allows users to have a conversation with the Gemini Pro AI model, with features like viewing chat history, restarting chats, and automatically saving chat sessions to a text file with timestamps.

## Installation

### Prerequisites

- Python 3.x
- Pip package manager
- An API key for Gemini Pro

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/llegomark/gemini-pro-chat.git
   cd gemini-pro-chat
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your Gemini Pro API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the application using Python:

```bash
python chat.py
```

### Commands

- Type your message and press Enter to chat with Gemini Pro.
- Type `history` to view the complete chat history.
- Type `restart` to start a new chat session while saving the current session to `chat_history.txt`.
- Type `exit` to exit the application and save the current session.

## Features

- Interactive chat with Gemini Pro AI.
- View chat history within the application.
- Automatically saves chat sessions with timestamps.
- Supports restarting chat sessions while preserving history.
- Streaming output for a more natural chat experience.

## Contributing

Contributions to the Gemini Pro Chat Application are welcome. Please feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google's Gemini API for providing the language model. More information about the Gemini API can be found in [Google's official announcement](https://blog.google/technology/ai/gemini-api-developers-cloud/).