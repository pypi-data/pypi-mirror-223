import shutil
import unittest
from unittest.mock import patch
from click.testing import CliRunner
from commands.init import init

class TestInitCommand(unittest.TestCase):
    def setUp(self):
        self.subsys_folder_created = False  # Initialize the flag

    def tearDown(self):
        if self.subsys_folder_created:
            shutil.rmtree(".subsys", ignore_errors=True)

    @patch("commands.init.is_initialized", return_value=False)
    @patch("commands.init.create_repository")
    def test_init_repository_not_initialized(self, mock_create_repository, mock_is_initialized):
        mock_is_initialized.return_value = True

        runner = CliRunner()
        result = runner.invoke(init)
        self.subsys_folder_created = True 

        self.assertEqual(result.exit_code, 0)

    @patch("commands.init.is_initialized", return_value=True)
    def test_init_repository_already_initialized(self, mock_is_initialized):
        # Set up the mock to indicate that the repository is already initialized
        mock_is_initialized.return_value = True

        # Run the init command
        runner = CliRunner()
        result = runner.invoke(init)
        self.subsys_folder_created = True 

        # Check if the command returns the expected output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error: subsys repository already initialized.", result.output)

if __name__ == '__main__':
    unittest.main()
