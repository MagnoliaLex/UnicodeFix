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

### 1. Web Interface (Recommended - Modern UI)

```powershell
# Launch the modern web interface
.\unicodefix-web.bat

# Or using PowerShell
.\Start-UnicodeFix-Web.ps1

# Or manually
python run_web.py
```

The web interface provides:
- Modern, clean UI with dark mode support
- Drag-and-drop file upload
- Real-time text cleaning
- Copy and download results
- Cross-platform compatibility

### 2. Batch File (Command Line)

```powershell
# Clean specific files
.\unicodefix.bat file1.txt file2.txt

# Clean files with pipe input
Get-Content input.txt | .\unicodefix.bat > cleaned.txt

# Get help
.\unicodefix.bat --help
```

### 3. PowerShell Functions (After restarting PowerShell)

```powershell
# Using the unicodefix alias
unicodefix file1.txt file2.txt

# Using the cleanup-text alias
cleanup-text file1.txt file2.txt

# Pipe usage
Get-Content input.txt | unicodefix > cleaned.txt
```

### 4. Windows Explorer Integration (Optional)

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

### Common Issues

#### "cannot import name 'str' from 'typing'" Error
This error occurs with Python 3.13+ due to changes in the typing module. 

**Solution:**
```powershell
# Clear Python cache and restart
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force bin\__pycache__ -ErrorAction SilentlyContinue
python run_web.py
```

#### NPM/Node.js Errors ("Could not read package.json")
This is a Python project, not a Node.js project. **Do not run npm commands.**

The web interface uses:
- Python FastAPI backend
- CDN-hosted Tailwind CSS (no build process needed)
- No Node.js or npm dependencies required

**If you see npm errors:** You're in the wrong directory or running the wrong commands. Use Python commands instead:
```powershell
# Correct commands for UnicodeFix
python run_web.py              # Start web interface
python test_web.py             # Test components
.\unicodefix-web.bat           # Windows launcher
```

#### Web Server Port Already in Use
```powershell
# Check what's using port 8000
netstat -ano | findstr :8000

# Kill the process if needed (replace PID with actual process ID)
taskkill /F /PID <PID>
```

#### Virtual Environment Issues
```powershell
# Recreate virtual environment
Remove-Item -Recurse -Force venv
.\setup.ps1
```

#### PowerShell Execution Policy
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Getting Help

If you encounter issues:
1. Run `python test_web.py` to verify components
2. Check the troubleshooting section above
3. Ensure you're using Python commands, not npm/Node.js
4. Verify Python 3.8+ is installed and in PATH

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