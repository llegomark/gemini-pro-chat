import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from chat import ChatHistoryManager, main


class TestChatHistoryManager(unittest.TestCase):

    def test_initialization(self):
        manager = ChatHistoryManager()
        self.assertEqual(manager.history, [])
        self.assertEqual(manager.filename, 'chat_history.txt')
        self.assertEqual(manager.max_file_size_mb, 5)

    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('os.rename')
    def test_add_and_save_message(self, mock_rename, mock_getsize, mock_exists):
        manager = ChatHistoryManager()
        manager.add_message('user', 'test message')
        self.assertEqual(len(manager.history), 1)

        mock_exists.return_value = True
        mock_getsize.return_value = 4 * 1024 * 1024
        m = mock_open()
        with patch('builtins.open', m):
            manager.save_to_file()
        m.assert_called_once_with('chat_history.txt', 'a', encoding='utf-8')
        self.assertEqual(manager.history, [])

        mock_getsize.return_value = 6 * 1024 * 1024
        manager.add_message('user', 'another message')
        with patch('builtins.open', m):
            manager.save_to_file()
        mock_rename.assert_called_once_with(
            'chat_history.txt', 'chat_history.txt.backup')

    @patch('builtins.print')
    def test_display(self, mock_print):
        manager = ChatHistoryManager()
        manager.add_message('user', 'display test')
        manager.display()
        mock_print.assert_called()


class TestMainFunction(unittest.TestCase):

    @patch('builtins.input', side_effect=['exit'])
    @patch('os.getenv', return_value='dummy_key')
    @patch('google.generativeai.GenerativeModel')
    @patch('chat.ChatHistoryManager')
    def test_main(self, mock_manager, mock_gen_model, mock_getenv, mock_input):
        main()
        mock_getenv.assert_called_with('GEMINI_API_KEY')
        mock_gen_model.assert_called()
        mock_manager.return_value.save_to_file.assert_called()

    @patch('builtins.input', side_effect=['history', 'exit'])
    def test_main_history_command(self, mock_input):
        with patch('chat.ChatHistoryManager') as mock_manager:
            main()
            mock_manager.return_value.display.assert_called()

    @patch('builtins.input', side_effect=['restart', 'exit'])
    def test_main_restart_command(self, mock_input):
        with patch('chat.ChatHistoryManager') as mock_manager:
            main()
            mock_manager.return_value.save_to_file.assert_called()
            mock_manager.return_value.add_message.assert_called_with(
                "system", "--- New Session ---")

    @patch('builtins.input', side_effect=['Hello', 'exit'])
    def test_main_user_message(self, mock_input):
        with patch('chat.ChatHistoryManager'), patch('google.generativeai.GenerativeModel') as mock_gen_model:
            chat_instance = MagicMock()
            mock_gen_model.return_value.start_chat.return_value = chat_instance
            main()
            chat_instance.send_message.assert_called_with('Hello', stream=True)

    @patch('builtins.input', side_effect=['Hello', 'exit'])
    @patch('builtins.print')
    def test_main_exception_handling(self, mock_print, mock_input):
        with patch('chat.ChatHistoryManager'), patch('google.generativeai.GenerativeModel') as mock_gen_model:
            chat_instance = MagicMock()
            chat_instance.send_message.side_effect = Exception(
                "Test Exception")
            mock_gen_model.return_value.start_chat.return_value = chat_instance
            main()
            mock_print.assert_called_with("An error occurred: Test Exception")


if __name__ == '__main__':
    unittest.main()
