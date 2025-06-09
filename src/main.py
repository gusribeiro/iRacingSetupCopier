import os
import shutil
from pathlib import Path
import ctypes
import logging
from typing import List, Tuple, Dict
import tkinter as tk
from tkinter import ttk
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('setup_copier.log')
    ]
)

def get_iracing_setup_folders() -> List[Path]:
    """
    Get all setup folders from iRacing directory.

    Returns:
        List[Path]: List of Path objects representing setup folders

    Raises:
        FileNotFoundError: If iRacing setups directory is not found
    """
    iracing_path = Path.home() / "Documents" / "iRacing" / "setups"
    if not iracing_path.exists():
        raise FileNotFoundError(f"iRacing setups directory not found at: {iracing_path}")

    folders = [folder for folder in iracing_path.iterdir() if folder.is_dir()]

    logging.info(f"Found {len(folders)} setup folders:")
    for folder in folders:
        logging.info(f"- {folder.name}")

    return folders

def get_current_setup_files() -> List[Path]:
    """
    Get all setup files from current directory.

    Returns:
        List[Path]: List of Path objects representing .sto files
    """
    current_dir = Path.cwd()
    files = [file for file in current_dir.iterdir() if file.is_file() and file.suffix.lower() == '.sto']

    logging.info(f"Found {len(files)} setup files in current directory")
    return files

def extract_car_code(filename: str) -> str:
    """
    Extract car code from setup filename.

    Args:
        filename (str): Setup filename

    Returns:
        str: Extracted car code

    Raises:
        ValueError: If filename format is invalid
    """
    try:
        return filename.split('_')[2].lower()
    except IndexError:
        raise ValueError(f"Invalid filename format: {filename}. Expected format: VRS_25S1DS_CARCODE_*.sto")

def copy_setup_files(setup_folders: List[Path], setup_files: List[Path]) -> Tuple[List[str], List[str]]:
    """
    Copy setup files to their corresponding folders based on car code in filename.

    Args:
        setup_folders (List[Path]): List of setup folder paths
        setup_files (List[Path]): List of setup file paths

    Returns:
        Tuple[List[str], List[str]]: Tuple containing lists of successful copies and errors
    """
    copied_files = []
    errors = []

    # Load the car code to folder mapping
    with open(Path(__file__).parent / 'iracing-folders.json', 'r') as f:
        car_code_mapping = json.load(f)

    # Create a reverse mapping for easier lookup, converting all keys and values to lowercase
    folder_mapping = {v.lower(): v for v in car_code_mapping.values()}  # Default mapping
    folder_mapping.update({k.lower(): v for k, v in car_code_mapping.items() if k})

    for setup_file in setup_files:
        try:
            car_code = extract_car_code(setup_file.stem)
            matching_folder = None

            # First try to find an exact match in the mapping
            if car_code.lower() in folder_mapping:
                folder_name = folder_mapping[car_code.lower()]
                matching_folder = next((folder for folder in setup_folders if folder.name.lower() == folder_name.lower()), None)

            # If no exact match, try to find a partial match
            if not matching_folder:
                for folder in setup_folders:
                    if car_code.lower() in folder.name.lower():
                        matching_folder = folder
                        break

            if matching_folder:
                destination = matching_folder / setup_file.name
                shutil.copy2(setup_file, destination)
                copied_files.append(f"{setup_file.name} -> {matching_folder.name}")
                logging.info(f"Copied {setup_file.name} to {matching_folder.name}")
            else:
                error_msg = f"No matching folder found for car code '{car_code}' in {setup_file.name}"
                errors.append(error_msg)
                logging.warning(error_msg)

        except ValueError as e:
            errors.append(str(e))
            logging.error(str(e))
        except Exception as e:
            error_msg = f"Error copying {setup_file.name}: {str(e)}"
            errors.append(error_msg)
            logging.error(error_msg)

    return copied_files, errors

def show_message_box(message: str, title: str, icon: int):
    """
    Show a message box with the given message and title.

    Args:
        message (str): Message to display
        title (str): Title of the message box
        icon (int): Icon to display (0x10 for error, 0x40 for info)
    """
    ctypes.windll.user32.MessageBoxW(0, message, title, icon)

def main():
    try:
        logging.info("Starting iRacing setup files copy process...")

        # Get setup folders from iRacing directory
        setup_folders = get_iracing_setup_folders()

        # Get setup files from current directory
        setup_files = get_current_setup_files()

        if not setup_files:
            message = "Nenhum arquivo de setup (.sto) encontrado no diretório atual!"
            logging.warning(message)
            show_message_box(message, "Aviso", 0x30)
            return

        # Copy files to their respective folders
        copied_files, errors = copy_setup_files(setup_folders, setup_files)

        # Build alert message
        alert_msg = []
        if copied_files:
            alert_msg.append(f"{len(copied_files)} arquivo(s) copiado(s) com sucesso!")
        if errors:
            alert_msg.append(f"{len(errors)} arquivo(s) com erro.")
            # Log detailed errors to file
            with open('setup_errors.log', 'w') as f:
                f.write('\n'.join(errors))

        final_msg = '\n'.join(alert_msg)

        # Show appropriate message box
        icon = 0x10 if errors else 0x40  # MB_ICONERROR if errors, MB_ICONINFORMATION otherwise
        show_message_box(final_msg, "Resultado da cópia de setups", icon)

    except Exception as e:
        error_msg = f"Erro fatal: {str(e)}"
        logging.error(error_msg)
        show_message_box(error_msg, "Erro", 0x10)

if __name__ == "__main__":
    main()
