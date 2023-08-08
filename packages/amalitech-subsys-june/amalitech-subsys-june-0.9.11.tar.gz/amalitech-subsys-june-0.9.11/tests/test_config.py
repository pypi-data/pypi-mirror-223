import configparser
import unittest
import shutil
from unittest.mock import patch
from click.testing import CliRunner
from commands.config import config

class TestConfigCommand(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.subsys_folder_created = False  # Initialize the flag

    @classmethod
    def tearDown(self):
        if self.subsys_folder_created:
            shutil.rmtree(".subsys", ignore_errors=True)

    @patch("commands.config.is_initialized")
    def test_config_not_initialized(self, mock_is_initialized):
        mock_is_initialized.return_value = False

        runner = CliRunner()
        result = runner.invoke(config, ["--code", "GHS00012", "--student_id", "12345"])

        self.assertIn("Please initialize a repository.\nRun subsys init.", result.output)
        self.assertEqual(result.exit_code, 0)

    @patch("commands.config.is_initialized", return_value=True)
    @patch("commands.config.read_config")
    @patch("click.prompt")
    def test_config_interactive_mode(self, mock_prompt, mock_read_config, mock_is_initialized):
        # Set up the mocks
        mock_is_initialized.return_value = True
        mock_prompt.side_effect = ["test_code", "test_student_id"]
        
        mock_config_data = {
            "DEFAULT": {
                "Code": "GHS00012",
                "StudentID": "12345"
            }
        }
        
        mock_config_parser = configparser.ConfigParser()
        mock_config_parser.read_dict(mock_config_data)
        mock_read_config.return_value = mock_config_parser

        runner = CliRunner()
        result = runner.invoke(config, ["-i"])

        mock_prompt.assert_called_with("Enter the student ID:")
        self.assertNotEqual(result.exit_code, 0)

    @patch("commands.config.is_initialized", return_value=True)
    @patch("commands.config.read_config")
    @patch("commands.config.write_config")
    def test_config_non_interactive_mode(self, mock_write_config, mock_read_config, mock_is_initialized):
        # Set up the mocks
        mock_is_initialized.return_value = True
        
        mock_config_data = {
            "DEFAULT": {
                "Code": "GHS00012",
                "StudentID": "12345"
            }
        }
        
        mock_config_parser = configparser.ConfigParser()
        mock_config_parser.read_dict(mock_config_data)
        mock_read_config.return_value = mock_config_parser

        runner = CliRunner()
        result = runner.invoke(config, ["--code", "test_code", "--student_id", "test_student_id"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configuration saved successfully.\nCode: GHS00012\nStudent ID: 12345\n", result.output)

    @patch("commands.config.is_initialized")
    def test_config_missing_arguments(self, mock_is_initialized):
        mock_is_initialized.return_value = True

        runner = CliRunner()
        result = runner.invoke(config)

        self.assertIn("Assignment code and student ID are required.", result.output)
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()
