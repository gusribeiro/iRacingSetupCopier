import os
import shutil
from pathlib import Path
import ctypes
import logging
from typing import List, Tuple, Dict
import tkinter as tk
from tkinter import ttk

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

    # Create a mapping of car codes to folders for faster lookup
    folder_map: Dict[str, Path] = {
        folder.name.lower(): folder for folder in setup_folders
    }

    for setup_file in setup_files:
        try:
            car_code = extract_car_code(setup_file.stem)
            matching_folder = folder_map.get(car_code)

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

def show_message_box(message: str, title: str, icon: int = 0x40):
    """
    Show a custom message box with scrollable text area.

    Args:
        message (str): Message to display
        title (str): Window title
        icon (int): Icon type (0x40 for info, 0x10 for error)
    """
    try:
        # Create the main window
        root = tk.Tk()
        root.title(title)

        # Set window size and position
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        # Insert message
        text_widget.insert(tk.END, message)
        text_widget.config(state=tk.DISABLED)  # Make text read-only

        # Create OK button
        ok_button = ttk.Button(main_frame, text="OK", command=root.destroy)
        ok_button.pack(pady=10)

        # Set icon
        if icon == 0x10:  # Error icon
            root.iconbitmap("error.ico") if os.path.exists("error.ico") else None
        else:  # Info icon
            root.iconbitmap("info.ico") if os.path.exists("info.ico") else None

        # Start the event loop
        root.mainloop()

    except Exception as e:
        logging.error(f"Failed to show message box: {str(e)}")
        # Fallback to Windows message box if Tkinter fails
        try:
            ctypes.windll.user32.MessageBoxW(0, message, title, icon)
        except Exception as e2:
            logging.error(f"Failed to show fallback message box: {str(e2)}")

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
            alert_msg.append("Arquivos copiados com sucesso:\n" + '\n'.join(f"- {f}" for f in copied_files))
        if errors:
            alert_msg.append("\nErros encontrados:\n" + '\n'.join(f"- {e}" for e in errors))
        if not copied_files and not errors:
            alert_msg.append("Nenhum arquivo foi processado.")
        if not errors and copied_files:
            alert_msg.append("\nTodos os arquivos foram copiados com sucesso!")

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
