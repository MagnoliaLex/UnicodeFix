# UnicodeFix - Windows Installation and Usage Guide

This guide provides Windows-specific instructions for installing and using UnicodeFix.

## Prerequisites

- Python 3.8 or higher
- PowerShell 5.0 or higher (Windows 10/11 includes this by default)
- Git (optional, for cloning the repository)

## Installation

1. **Clone or download the repository:**
   ```powershell
   git clone https://github.com/unixwzrd/UnicodeFix.git
   cd UnicodeFix
   ```

2. **Allow PowerShell script execution (if needed):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Run the setup script:**
   ```powershell
   .\setup.ps1
   ```

The setup script will:
- Create a Python virtual environment
- Install the required dependencies
- Create a `unicodefix.bat` launcher
- Add PowerShell functions for easier command-line usage

## Usage Options

### 1. Batch File (Recommended for beginners)

```powershell
# Clean specific files
.\unicodefix.bat file1.txt file2.txt

# Clean files with pipe input
Get-Content input.txt | .\unicodefix.bat > cleaned.txt

# Get help
.\unicodefix.bat --help
```

### 2. PowerShell Functions (After restarting PowerShell)

```powershell
# Using the unicodefix alias
unicodefix file1.txt file2.txt

# Using the cleanup-text alias
cleanup-text file1.txt file2.txt

# Pipe usage
Get-Content input.txt | unicodefix > cleaned.txt
```

### 3. Windows Explorer Integration (Optional)

For right-click context menu integration:

1. **Run as Administrator:**
   ```powershell
   # Right-click PowerShell and "Run as Administrator"
   .\windows\setup-context-menu.ps1
   ```

2. **Usage:**
   - Right-click any file → "Clean Unicode"
   - Right-click in empty folder space → "Clean Unicode Files Here"

3. **To remove:**
   ```powershell
   .\windows\setup-context-menu.ps1 -Remove
   ```

## Advanced Usage

### Direct Python Script Execution

If you prefer to work with the Python script directly:

```powershell
# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Run the script
python bin\cleanup-text.py file1.txt file2.txt

# Deactivate when done
deactivate
```

### VS Code Integration

1. Install the "PowerShell" extension
2. Open your project in VS Code
3. Use the integrated terminal to run:
   ```powershell
   .\unicodefix.bat filename.txt
   ```

### Command Prompt (cmd) Usage

```cmd
REM Navigate to the UnicodeFix directory
cd C:\path\to\UnicodeFix

REM Use the batch file
unicodefix.bat file1.txt file2.txt
```

## Troubleshooting

### "Execution of scripts is disabled" Error

Run this command in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

### "Python not found" Error

1. Install Python from [python.org](https://python.org)
2. Make sure to check "Add Python to PATH" during installation
3. Restart your terminal and try again

### Virtual Environment Issues

If the virtual environment becomes corrupted:
```powershell
# Remove the old environment
Remove-Item venv -Recurse -Force

# Recreate it
.\setup.ps1 -Force
```

### Context Menu Not Working

1. Ensure you ran `setup-context-menu.ps1` as Administrator
2. Try logging out and back in, or restart Windows
3. Check that the paths in the registry entries are correct

## Features Specific to Windows

- **Line Ending Normalization**: Automatically handles Windows CRLF line endings
- **PowerShell Integration**: Native PowerShell functions and aliases
- **Explorer Context Menu**: Right-click integration for easy file processing
- **Batch File Launcher**: Simple double-click execution
- **Cross-Platform Compatibility**: Works seamlessly with files from other platforms

## File Locations

After installation, you'll find:
- `setup.ps1` - Main setup script
- `unicodefix.bat` - Windows launcher
- `windows/` - Windows-specific files
  - `setup-context-menu.ps1` - Context menu installer
  - `unicodefix-context-menu.reg` - Registry template (manual installation)
- `bin/cleanup-text.py` - Main Python script
- `venv/` - Python virtual environment

## Support

For Windows-specific issues, please check:
1. This guide first
2. The main [README.md](README.md) for general information
3. Open an issue on the GitHub repository

## License

Same as the main project - MIT License. See [LICENSE](LICENSE) for details. 