import os
import shutil
from pathlib import Path
import ctypes

def get_iracing_setup_folders():
    """Get all setup folders from iRacing directory."""
    iracing_path = Path.home() / "Documents" / "iRacing" / "setups"
    if not iracing_path.exists():
        raise FileNotFoundError(f"iRacing setups directory not found at: {iracing_path}")

    folders = [folder for folder in iracing_path.iterdir() if folder.is_dir()]

    # Log all found folders
    print("\nFound setup folders:")
    for folder in folders:
        print(f"- {folder.name}")
    print()  # Add empty line for better readability

    return folders

def get_current_setup_files():
    """Get all setup files from current directory."""
    current_dir = Path.cwd()
    return [file for file in current_dir.iterdir() if file.is_file() and file.suffix.lower() == '.sto']

def copy_setup_files(setup_folders, setup_files):
    """Copy setup files to their corresponding folders based on car code in filename."""
    copied_files = []
    errors = []

    for setup_file in setup_files:
        # Extract car code from filename (assuming format: VRS_25S1DS_CARCODE_*.sto)
        try:
            car_code = setup_file.stem.split('_')[2].lower()
        except IndexError:
            errors.append(f"Invalid filename format for {setup_file.name}")
            continue

        # Find matching folder
        matching_folder = None
        for folder in setup_folders:
            if car_code in folder.name.lower():
                matching_folder = folder
                break

        if matching_folder:
            try:
                destination = matching_folder / setup_file.name
                shutil.copy2(setup_file, destination)
                copied_files.append(f"{setup_file.name} -> {matching_folder.name}")
            except Exception as e:
                errors.append(f"Error copying {setup_file.name}: {str(e)}")
        else:
            errors.append(f"No matching folder found for car code '{car_code}' in {setup_file.name}")

    return copied_files, errors

def main():
    try:
        print("Starting iRacing setup files copy process...")

        # Get setup folders from iRacing directory
        setup_folders = get_iracing_setup_folders()
        print(f"Found {len(setup_folders)} setup folders in iRacing directory")

        # Get setup files from current directory
        setup_files = get_current_setup_files()
        print(f"Found {len(setup_files)} setup files in current directory")

        if not setup_files:
            print("No setup files found in current directory!")
            # Show alert for no files
            ctypes.windll.user32.MessageBoxW(0, "Nenhum arquivo de setup (.sto) encontrado no diretório atual!", "Aviso", 0x30)
            return

        # Copy files to their respective folders
        copied_files, errors = copy_setup_files(setup_folders, setup_files)

        # Display results in terminal
        if copied_files:
            print("\nSuccessfully copied files:")
            for file in copied_files:
                print(f"- {file}")

        if errors:
            print("\nErrors encountered:")
            for error in errors:
                print(f"- {error}")

        if not errors:
            print("\nAll files were copied successfully!")

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

        # Show alert
        if errors:
            icon = 0x10  # MB_ICONERROR
        else:
            icon = 0x40  # MB_ICONINFORMATION
        ctypes.windll.user32.MessageBoxW(0, final_msg, "Resultado da cópia de setups", icon)

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        # Show alert for fatal error
        ctypes.windll.user32.MessageBoxW(0, f"Erro fatal: {str(e)}", "Erro", 0x10)

if __name__ == "__main__":
    main()
