# 🏎️ iRacing Setup Copier

### 📝 Description
iRacing Setup Copier is a Python utility that helps iRacing users automatically copy setup files (.sto) to their corresponding car folders in the iRacing setups directory. This tool is particularly useful for managing multiple setup files and ensuring they are placed in the correct car folders.

### ✨ Features
- 🔍 Automatically detects setup folders in your iRacing directory
- 📋 Copies .sto files to their corresponding car folders based on the car code in the filename
- 💻 Provides both terminal and GUI feedback about the copying process
- ⚠️ Error handling and validation for file operations
- 🏆 Supports the VRS setup file naming convention (VRS_25S1DS_CARCODE_*.sto)

### 📋 Requirements
- 🐍 Python 3.x
- 🪟 Windows operating system
- 🎮 iRacing installed with the default setup directory structure

### 🚀 Installation
1. Clone this repository:
```bash
git clone https://github.com/yourusername/iRacingSetupCopier.git
cd iRacingSetupCopier
```

2. No additional dependencies are required as the script uses only Python standard libraries.

### 💡 Usage
1. 📥 Download the latest executable from the releases page
2. 📁 Place the executable in the folder containing your .sto setup files
3. 🖱️ Double-click the executable to run it
4. The program will automatically:
   - 🔍 Find your iRacing setups directory
   - 📋 Copy the setup files to their corresponding car folders
   - 📊 Show a summary of the operation results

### 📝 File Naming Convention
The script expects setup files to follow this naming pattern:
```
*_*_CARCODE_*.sto
```
Where:
- CARCODE must be in the third position, separated by underscores (_)
- CARCODE is the car identifier that matches the folder name in your iRacing setups directory

### 🤝 Contributing
Contributions are always welcome! If you'd like to contribute to the project, follow these steps:

1. 🍴 Fork the project
2. 🌿 Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the Branch (`git push origin feature/AmazingFeature`)
5. 🔄 Open a Pull Request

Please make sure to:
- 📚 Follow code best practices
- ✅ Add tests for new features
- 📝 Update documentation when necessary
- 🧹 Keep the code clean and well-organized

To report bugs or suggest new features, please open an issue on GitHub.
