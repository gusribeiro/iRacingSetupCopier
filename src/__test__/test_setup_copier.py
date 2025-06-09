import unittest
from pathlib import Path
import shutil
import tempfile
import os
import sys
from unittest.mock import patch

# Adiciona o diretório src ao sys.path para garantir que o import funcione
sys.path.insert(0, str(Path(__file__).parent.parent))

from setupCopier import get_iracing_setup_folders, get_current_setup_files, copy_setup_files

class TestSetupCopier(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.iracing_dir = Path(self.test_dir) / "Documents" / "iRacing" / "setups"
        self.iracing_dir.mkdir(parents=True)

        # Create test car folders
        self.car_folders = {
            "porsche992gt3": self.iracing_dir / "porsche992gt3",
            "ferrarigt3": self.iracing_dir / "ferrarigt3",
        }
        for folder in self.car_folders.values():
            folder.mkdir()

        # Create test setup files
        self.setup_files = {
            "VRS_25S1DS_porsche992gt3_test.sto": "Test content for Porsche",
            "VRS_25S1DS_ferrarigt3_test.sto": "Test content for Ferrari",
            "invalid_format.txt": "Invalid file",
        }

        # Create setup files in current directory
        self.current_dir = Path.cwd()
        for filename, content in self.setup_files.items():
            with open(self.current_dir / filename, 'w') as f:
                f.write(content)

    def tearDown(self):
        # Clean up temporary directories and files
        shutil.rmtree(self.test_dir)
        for filename in self.setup_files.keys():
            try:
                os.remove(self.current_dir / filename)
            except FileNotFoundError:
                pass

    @patch('pathlib.Path.home')
    def test_get_iracing_setup_folders(self, mock_home):
        # Mock the home directory to point to our test directory
        mock_home.return_value = Path(self.test_dir)

        # Test with valid directory
        folders = get_iracing_setup_folders()
        self.assertIsInstance(folders, list)
        self.assertTrue(all(isinstance(f, Path) for f in folders))
        self.assertEqual(len(folders), 2)  # We created 2 car folders

        # Test with non-existent directory
        shutil.rmtree(self.iracing_dir)
        with self.assertRaises(FileNotFoundError):
            get_iracing_setup_folders()

    def test_get_current_setup_files(self):
        files = get_current_setup_files()
        self.assertIsInstance(files, list)
        self.assertTrue(all(isinstance(f, Path) for f in files))
        self.assertTrue(all(f.suffix.lower() == '.sto' for f in files))
        self.assertEqual(len(files), 2)  # Should only count .sto files

    def test_copy_setup_files(self):
        setup_folders = list(self.car_folders.values())
        setup_files = [Path(f) for f in self.setup_files.keys() if f.endswith('.sto')]

        copied_files, errors = copy_setup_files(setup_folders, setup_files)

        # Check if files were copied correctly
        self.assertEqual(len(copied_files), 2)
        self.assertEqual(len(errors), 0)

        # Verify files exist in destination folders
        for car_folder in self.car_folders.values():
            car_code = car_folder.name
            matching_files = list(car_folder.glob(f"*{car_code}*.sto"))
            self.assertEqual(len(matching_files), 1)

    def test_copy_setup_files_with_invalid_filename(self):
        # Create a file with invalid format
        invalid_file = Path("invalid_format.sto")
        with open(invalid_file, 'w') as f:
            f.write("Invalid content")

        setup_folders = list(self.car_folders.values())
        setup_files = [invalid_file]

        copied_files, errors = copy_setup_files(setup_folders, setup_files)

        # Check error handling
        self.assertEqual(len(copied_files), 0)
        self.assertEqual(len(errors), 1)
        self.assertTrue("Invalid filename format" in errors[0])

        # Clean up
        invalid_file.unlink()

    def test_copy_setup_files_with_nonexistent_car(self):
        # Create a setup file for a non-existent car
        nonexistent_car_file = Path("VRS_25S1DS_nonexistentcar_test.sto")
        with open(nonexistent_car_file, 'w') as f:
            f.write("Test content")

        setup_folders = list(self.car_folders.values())
        setup_files = [nonexistent_car_file]

        copied_files, errors = copy_setup_files(setup_folders, setup_files)

        # Check error handling
        self.assertEqual(len(copied_files), 0)
        self.assertEqual(len(errors), 1)
        self.assertTrue("No matching folder found" in errors[0])

        # Clean up
        nonexistent_car_file.unlink()

if __name__ == '__main__':
    unittest.main()
