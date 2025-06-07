# MacWhisper Pro License Bypass - Quick Start Guide

## 🚀 Getting Started (60 seconds)

### Prerequisites
- **macOS** (any recent version)
- **Python 3.7+** (already installed on macOS)
- **MacWhisper.app** (download from official website if needed)
- **Administrator privileges** (required for system modifications)

### Option 1: Easy GUI Launch (Recommended)
```bash
# 1. Open Terminal and navigate to the tool directory
cd MacWhisperSecTest

# 2. Run the interactive launcher
sudo ./launch.sh

# 3. Choose option 1 (Simple GUI) when prompted
# 4. Follow the GUI instructions
```

### Option 2: Direct GUI Launch
```bash
# Run the simple GUI directly
sudo python3 simple_gui.py
```

### Option 3: Command Line (Advanced Users)
```bash
# Apply bypass directly via command line
sudo python3 license_server.py

# In another terminal, launch MacWhisper
open /Applications/MacWhisper.app

# To cleanup when done
sudo python3 license_server.py cleanup
```

## 📱 Using the GUI

1. **Verify App Path**: Ensure MacWhisper path is correct (default: `/Applications/MacWhisper.app`)
2. **Click "Apply Bypass"**: This configures all bypass layers
3. **Click "Launch MacWhisper"**: Opens MacWhisper with Pro features unlocked
4. **Use "Cleanup"**: Restores original settings when finished

## ✅ Success Indicators

After applying the bypass, you should see:
- ✅ No "Upgrade to Pro" dialogs in MacWhisper
- ✅ Access to all transcription models
- ✅ Batch processing features available
- ✅ All export formats unlocked

## 🔧 Troubleshooting

### Common Issues & Solutions

**"Permission denied"**
```bash
# Solution: Run with sudo
sudo python3 simple_gui.py
```

**"MacWhisper is damaged"**
```bash
# Solution: Remove quarantine attributes
xattr -cr /Applications/MacWhisper.app
```

**Port 8080 in use**
```bash
# Check what's using the port
lsof -i :8080
# Kill the process if needed
sudo kill -9 [PID]
```

**GUI won't start**
```bash
# Test GUI support
python3 -c "import tkinter; print('GUI OK')"
# If fails, use command line mode instead
```

## 🧪 Test Your Setup

```bash
# Run the setup test to verify everything works
python3 test_setup.py
```

## 🧹 Cleanup & Removal

To completely remove all traces:

```bash
# Use the GUI cleanup button, OR run:
sudo python3 license_server.py cleanup

# Manual cleanup if needed:
sudo python3 -c "
import subprocess
subprocess.run(['security', 'delete-generic-password', '-s', 'com.goodsnooze.MacWhisper'], capture_output=True)
subprocess.run(['defaults', 'delete', 'com.goodsnooze.MacWhisper'], capture_output=True)
print('Manual cleanup completed')
"
```

## 📞 Need Help?

1. **Run the test**: `python3 test_setup.py`
2. **Check README.md** for detailed documentation
3. **Verify system requirements** are met
4. **Try command line mode** if GUI has issues

## ⚠️ Important Notes

- **Keep the tool running** while using MacWhisper (for network interception)
- **Run with sudo** for full functionality
- **Use cleanup** to restore settings when done
- **Tool is for educational/research purposes only**

---

**Ready to start? Run: `sudo ./launch.sh` and choose option 1!**
