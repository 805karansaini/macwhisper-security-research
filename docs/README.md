# MacWhisper Pro License Bypass Tool

A comprehensive security testing tool for bypassing MacWhisper Pro licensing restrictions. This tool implements a multi-layered approach combining keychain manipulation, system preferences modification, network interception, and offline license file creation.

## ⚠️ Disclaimer

This tool is provided for **educational and security research purposes only**. Use only on software you own or have explicit permission to modify. Users are responsible for complying with all applicable laws and software licenses.

## 🎯 Features

- **Multi-layered bypass approach** - Combines multiple bypass techniques for maximum effectiveness
- **GUI Interface** - User-friendly graphical interface for non-technical users
- **Command Line Interface** - Advanced CLI for technical users
- **System Integration** - Deep integration with macOS keychain and preferences
- **Network Interception** - Local HTTP server for license validation bypass
- **Automatic Cleanup** - Restore original system settings when done
- **Safety Checks** - Built-in safety mechanisms to prevent system damage

## 📋 Requirements

- **macOS** (tested on macOS 10.15+)
- **Python 3.7+** (built-in on macOS)
- **Administrator privileges** (required for system modifications)
- **MacWhisper.app** installed in `/Applications/` or custom path

## 🛠️ Installation

1. **Download the tool:**
   ```bash
   # Navigate to your desired directory
   cd ~/Desktop

   # If you have the MacWhisperSecTest directory:
   cd MacWhisperSecTest
   ```

2. **Verify files are present:**
   ```bash
   ls -la
   # Should show: license_server.py, gui_app.py, launch_gui.py, README.md
   ```

3. **Make scripts executable:**
   ```bash
   chmod +x *.py
   ```

## 🚀 Usage

### GUI Mode (Recommended for Non-Technical Users)

1. **Launch the GUI:**
   ```bash
   sudo python3 launch_gui.py
   ```

2. **Follow the GUI steps:**
   - Verify MacWhisper app path (default: `/Applications/MacWhisper.app`)
   - Click "Apply Bypass" to configure the license bypass
   - Click "Launch MacWhisper" to start the app with Pro features
   - Use "Cleanup" to restore original settings when done

### Command Line Mode (Advanced Users)

1. **Apply the bypass:**
   ```bash
   sudo python3 license_server.py
   ```

2. **Launch MacWhisper** (in another terminal):
   ```bash
   open /Applications/MacWhisper.app
   ```

3. **Cleanup when done:**
   ```bash
   sudo python3 license_server.py cleanup
   ```

## 🔧 Technical Details

### How It Works

The tool implements a **4-layer bypass approach**:

1. **Keychain Integration**
   - Injects fake license keys into macOS keychain
   - Uses service identifier: `com.goodsnooze.MacWhisper`
   - Key attribute: `gumroadLicenseKey_Key`

2. **System Preferences**
   - Sets application preferences for license validation
   - Modifies: `hasValidLicense`, `isProVersion`, `licenseValidated`
   - Target domain: `com.goodsnooze.MacWhisper`

3. **Network Interception**
   - Redirects Gumroad API calls to localhost
   - Modifies `/etc/hosts` file: `127.0.0.1 api.gumroad.com`
   - Runs local HTTP server on port 8080

4. **Offline License Files**
   - Creates license files in app bundle
   - Locations: `license.json`, `offline_license.json`, etc.
   - Contains fake license data and feature flags

### File Structure

```
MacWhisperSecTest/
├── license_server.py    # Core bypass implementation
├── gui_app.py          # GUI interface
├── launch_gui.py       # GUI launcher with checks
├── requirements.txt    # Python dependencies (none required)
└── README.md          # This file
```

### System Modifications

The tool makes the following **reversible** system changes:

- **Keychain entries** for license storage
- **Application preferences** for license state
- **Hosts file modification** for API redirection
- **App bundle files** for offline validation
- **Code signature removal/re-signing** for app execution

All changes can be restored using the cleanup functionality.

## 🛡️ Safety Features

- **Automatic backups** of modified system files
- **Permission checks** before making changes
- **Error handling** to prevent system damage
- **Cleanup functionality** to restore original state
- **Safe code signing** with ad-hoc signatures

## 📊 Success Verification

After applying the bypass, verify success by checking:

1. **No upgrade prompts** when launching MacWhisper
2. **Pro features accessible** (advanced models, batch processing)
3. **Export formats unlocked** (multiple format options)
4. **No license validation errors** in console/logs

## 🔍 Troubleshooting

### Common Issues

1. **"Permission denied" errors**
   ```bash
   # Solution: Run with sudo
   sudo python3 launch_gui.py
   ```

2. **"MacWhisper is damaged" error**
   ```bash
   # Solution: Remove quarantine attributes
   xattr -cr /Applications/MacWhisper.app
   ```

3. **App won't launch after bypass**
   ```bash
   # Solution: Re-sign the application
   codesign -s - --force --deep /Applications/MacWhisper.app
   ```

4. **License server port conflict**
   ```bash
   # Solution: Check what's using port 8080
   lsof -i :8080
   # Kill conflicting process if needed
   ```

### Cleanup Issues

If cleanup doesn't work properly:

```bash
# Manual cleanup steps:

# 1. Restore hosts file
sudo cp /etc/hosts.backup /etc/hosts  # if backup exists

# 2. Remove keychain entries
security delete-generic-password -s "com.goodsnooze.MacWhisper"

# 3. Reset preferences
defaults delete com.goodsnooze.MacWhisper

# 4. Remove license files
rm /Applications/MacWhisper.app/Contents/Resources/*license*.json
```

## 🔬 Advanced Configuration

### Custom App Path

```bash
# For non-standard MacWhisper installation:
python3 license_server.py --app-path "/path/to/MacWhisper.app"
```

### Custom License Data

Edit `license_server.py` to modify:
- `self.license_key` - Custom license key
- `self.license_email` - Custom email address
- License response data in `GumroadHandler`

### Network Configuration

- **Default port:** 8080
- **API endpoint:** `api.gumroad.com/v2/licenses/verify`
- **Redirect:** `127.0.0.1 api.gumroad.com`

## 📝 Development Notes

### Adding Features

1. **New bypass layers** - Add methods to `MacWhisperBypass` class
2. **GUI enhancements** - Modify `MacWhisperGUI` class in `gui_app.py`
3. **CLI options** - Extend argument parsing in `license_server.py`

### Testing

```bash
# Test individual components:
python3 -c "from license_server import MacWhisperBypass; b = MacWhisperBypass(); print('Import OK')"

# Test GUI components:
python3 -c "import tkinter; print('GUI support OK')"

# Test permissions:
python3 -c "import os; print('Root privileges:', os.geteuid() == 0)"
```

## 📚 References

- [MacWhisper Official Website](https://goodsnooze.gumroad.com/l/macwhisper)
- [Gumroad API Documentation](https://help.gumroad.com/article/76-api)
- [macOS Security Research](https://developer.apple.com/security/)

## 📞 Support

For technical support or questions:

1. **Check troubleshooting section** above
2. **Verify system requirements** are met
3. **Run with verbose output** for detailed error information
4. **Check console/system logs** for additional error details

## 🔄 Version History

- **v1.0** - Initial release with multi-layered bypass
- **v1.1** - Added GUI interface for non-technical users
- **v1.2** - Enhanced error handling and safety checks

---

**Remember:** Use this tool responsibly and only for legitimate security research purposes.
