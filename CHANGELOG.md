# Changelog for UnicodeFix

## 2025-12-08 Windows Compatibility Update

- **Added Windows support**: Complete PowerShell setup script (`setup.ps1`)
- **Windows launcher**: Created `unicodefix.bat` for easy Windows execution
- **Explorer integration**: Windows context menu support via `windows/setup-context-menu.ps1`
- **Enhanced Unicode cleaning**: Added ellipsis (\u2026) and non-breaking space (\u00A0) support
- **Cross-platform line endings**: Automatic Windows CRLF handling
- **Comprehensive documentation**: Added `README_Windows.md` with Windows-specific instructions
- **Improved error handling**: Better virtual environment detection and error messages
- **PowerShell integration**: Native PowerShell functions and aliases after setup

## 2025-04-27 20250427_01-update

- Update README
- Update cleanup-text.py to handle trailing whitespace
- Whitespace on empty lines (newline preserved)

## 2025-04-26 20250427_00-release

- Initial release
- Added STDIO pipe handling as a filter
