from pathlib import Path
import shutil
import unittest
from unittest.mock import patch
from click.testing import CliRunner
from commands.snap import snap

class TestSnapCommand(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.subsys_folder_created = False

    @classmethod
    def tearDown(self):
        # Clean up by removing the .subsys folder if it was created
        if self.subsys_folder_created:
            shutil.rmtree(".subsys", ignore_errors=True)

    @patch("commands.snap.is_initialized", return_value=False)
    @patch("click.echo")
    def test_snap_not_initialized(self, mock_echo, mock_is_initialized):
        # Set up the mocks
        mock_is_initialized.return_value = False

        runner = CliRunner()
        result = runner.invoke(snap, ["--name", "valid"])

        self.assertEqual(result.exit_code, 0)
        mock_is_initialized.assert_called_once()
        mock_echo.assert_called_once_with("Please initialize a repository.\nRun subsys init.")

    @patch("commands.snap.is_initialized", return_value=True)
    @patch("commands.snap.find_repository_folder", return_value='.subsys')
    @patch("commands.snap.snap_changes")
    @patch("commands.snap.add")
    @patch("click.echo")
    @patch("commands.snap.read_slug_file")
    def test_snap_valid_slug(self, mock_read_slug_file, mock_echo, mock_add, mock_snap_changes, mock_find_repository_folder, mock_is_initialized):
        # Set up the mocks
        mock_is_initialized.return_value = True
        find_repository_folder = Path(".subsys")
        find_repository_folder.mkdir(parents=True, exist_ok=True)

        runner = CliRunner()
        result = runner.invoke(snap, ["--name", "valid"])

        mock_is_initialized.assert_called_once()
        mock_find_repository_folder.assert_called_once()
        mock_echo.assert_not_called()
        self.assertNotEqual(result.exit_code, 0)
        shutil.rmtree(".subsys", ignore_errors=True)        

    @patch("commands.snap.is_initialized", return_value=True)
    def test_snap_invalid_slug(self, mock_is_initialized):
        # Set up the mocks
        mock_is_initialized.return_value = True

        runner = CliRunner()
        result = runner.invoke(snap, ["--name", "invalid*slug"])

        mock_is_initialized.assert_called_once()
        self.assertNotEqual(result.exit_code, 0)

    @patch("commands.snap.is_initialized", return_value=True)
    @patch("commands.snap.find_repository_folder", return_value="/path/to/repo")
    @patch("click.prompt")
    @patch("commands.snap.read_slug_file", return_value={"existing-slug": "123"})
    def test_snap_existing_slug(self, mock_read_slug_file, mock_prompt, mock_find_repository_folder, mock_is_initialized):
        # Set up the mocks
        mock_is_initialized.return_value = True
        mock_read_slug_file.return_value = ["existing-slug"]

        runner = CliRunner()
        result = runner.invoke(snap, ["--name", "123"])

        self.assertNotEqual(result.exit_code, 0)
        mock_is_initialized.assert_called_once()
        mock_find_repository_folder.assert_called_once()

if __name__ == '__main__':
    unittest.main()
