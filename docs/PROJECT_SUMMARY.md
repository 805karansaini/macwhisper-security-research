# MacWhisper Pro License Bypass Tool - Project Summary

## 📦 What's Included

This directory contains a complete security testing toolkit for bypassing MacWhisper Pro licensing restrictions. The solution includes both GUI and command-line interfaces with comprehensive documentation.

### 🗂️ File Structure

```
MacWhisperSecTest/
├── 🚀 QUICK_START.md          # 60-second setup guide (START HERE!)
├── 📖 README.md               # Comprehensive documentation
├── 📋 PROJECT_SUMMARY.md      # This file - project overview
├── 📄 requirements.txt        # Dependencies (none required)
│
├── 🖥️  GUI Applications
│   ├── simple_gui.py          # ⭐ Recommended GUI (no import issues)
│   ├── gui_app.py             # Advanced GUI (feature-rich)
│   └── launch_gui.py          # GUI launcher with checks
│
├── 🔧 Core Components
│   ├── license_server.py      # ⭐ Main bypass implementation
│   └── launch.sh              # Interactive launcher script
│
└── 🧪 Testing & Utilities
    └── test_setup.py           # Setup verification tool
```

## ⭐ Recommended Usage Paths

### For Non-Technical Users (Easiest)
```bash
# 1. Open Terminal, navigate to this directory
cd MacWhisperSecTest

# 2. Run the launcher and choose Simple GUI
sudo ./launch.sh
# Choose option 1 when prompted
```

### For Quick GUI Access
```bash
# Direct launch of the simple GUI
sudo python3 simple_gui.py
```

### For Technical Users (Command Line)
```bash
# Apply bypass via command line
sudo python3 license_server.py

# Launch MacWhisper (in another terminal)
open /Applications/MacWhisper.app
```

## 🎯 What This Tool Does

### Multi-Layered Bypass Approach

1. **🔑 Keychain Integration**
   - Injects fake license keys into macOS keychain
   - Service: `com.goodsnooze.MacWhisper`

2. **⚙️ System Preferences**
   - Sets license validation flags
   - Configures Pro version status

3. **🌐 Network Interception**
   - Redirects Gumroad API calls to localhost
   - Runs fake license server on port 8080

4. **📄 Offline License Files**
   - Creates license files in app bundle
   - Provides offline validation fallback

5. **✍️ Code Re-signing**
   - Removes and reapplies app signatures
   - Ensures modified app can launch

## ✅ Success Criteria

When working correctly, you should see:
- ✅ MacWhisper launches without "Upgrade to Pro" dialogs
- ✅ All transcription models accessible (Whisper Large, etc.)
- ✅ Batch processing features available
- ✅ All export formats unlocked (SRT, VTT, TXT, JSON)
- ✅ No license validation errors

## 🛡️ Safety Features

- **Automatic Backups**: Original system files backed up
- **Cleanup Functionality**: Restore original settings anytime
- **Permission Checks**: Validates admin privileges before modifications
- **Error Handling**: Graceful failure without system damage
- **Reversible Changes**: All modifications can be undone

## 🔧 Technical Implementation

### Core Technologies
- **Python 3.7+**: Main implementation language
- **Tkinter**: GUI framework (built into Python)
- **HTTP Server**: Network interception
- **macOS Security**: Keychain and code signing integration
- **Shell Scripting**: Launcher and utilities

### System Integration Points
- **Keychain Services**: License key storage
- **Defaults System**: Application preferences
- **Hosts File**: Network redirection
- **Code Signing**: Application signature management

## 📊 Testing & Verification

### Automated Testing
```bash
# Run comprehensive setup test
python3 test_setup.py
```

### Manual Verification Steps
1. Check MacWhisper launches without upgrade prompts
2. Verify Pro features are accessible
3. Test batch processing functionality
4. Confirm all export formats work

## 🧹 Cleanup & Maintenance

### Automatic Cleanup
- Use "Cleanup" button in GUI applications
- Or run: `sudo python3 license_server.py cleanup`

### Manual Cleanup (if needed)
```bash
# Remove keychain entries
security delete-generic-password -s "com.goodsnooze.MacWhisper"

# Reset application preferences
defaults delete com.goodsnooze.MacWhisper

# Restore hosts file (remove 127.0.0.1 api.gumroad.com line)
sudo nano /etc/hosts
```

## 🎓 Educational Value

This tool demonstrates several important security concepts:

### Security Research Techniques
- **Binary Analysis**: Understanding app structure and licensing
- **System Integration**: Keychain and preferences manipulation
- **Network Interception**: HTTP traffic redirection
- **Code Signing**: Certificate management and app modification

### macOS Security Features
- **Keychain Services**: Secure credential storage
- **Code Signing**: Application integrity verification
- **System Preferences**: Application configuration management
- **Network Security**: Host-based filtering and redirection

## ⚠️ Important Disclaimers

### Legal and Ethical Use
- **Educational Purposes Only**: For security research and learning
- **Own Software Only**: Use only on software you own or have permission to modify
- **Compliance Required**: Users responsible for following applicable laws
- **No Commercial Use**: Not for bypassing legitimate software licenses

### Technical Limitations
- **macOS Only**: Designed specifically for macOS systems
- **Version Specific**: May need updates for new MacWhisper versions
- **Admin Required**: Requires administrator privileges for full functionality
- **Network Dependent**: License server must remain running during use

## 🚀 Getting Started

1. **Read QUICK_START.md** for immediate usage instructions
2. **Run test_setup.py** to verify your system is ready
3. **Use launch.sh** for guided, interactive setup
4. **Check README.md** for comprehensive documentation

## 📞 Support Resources

### Self-Help
1. **QUICK_START.md**: Fast setup guide
2. **README.md**: Detailed documentation
3. **test_setup.py**: Automated diagnostics
4. **GUI logs**: Real-time operation feedback

### Troubleshooting Process
1. Run setup test: `python3 test_setup.py`
2. Check system requirements (macOS, Python 3.7+, admin privileges)
3. Verify MacWhisper is installed at `/Applications/MacWhisper.app`
4. Try command line mode if GUI has issues
5. Use cleanup function to reset if problems occur

---

**🎯 Ready to start? Open QUICK_START.md and follow the 60-second setup guide!**
