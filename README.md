# MacWhisper Security Research

A comprehensive security research toolkit for analyzing and bypassing MacWhisper Pro licensing restrictions. This project demonstrates various security testing techniques including keychain manipulation, network interception, and application reverse engineering.

## ⚠️ Important Disclaimer

This tool is provided **strictly for educational and security research purposes only**. It is intended for:

- Security researchers studying application licensing mechanisms
- Educational demonstrations of macOS security features
- Testing on software you own or have explicit permission to modify

**Users are solely responsible for complying with all applicable laws, software licenses, and terms of service.**

## 🎯 Features

- **Multi-layered bypass approach** combining multiple security techniques
- **GUI and CLI interfaces** for different user experience levels
- **System integration** with macOS keychain and preferences
- **Network interception** capabilities for license validation bypass
- **Comprehensive documentation** for educational purposes
- **Safety features** with automatic cleanup and restoration

## 📋 Requirements

- **macOS 10.15+** (tested on various versions)
- **Python 3.7+** (included with macOS)
- **Administrator privileges** (required for system modifications)
- **Target application** (MacWhisper.app) installed

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/macwhisper-security-research.git
   cd macwhisper-security-research
   ```

2. **Run the setup test:**
   ```bash
   python3 tests/test_setup.py
   ```

3. **Launch the GUI (recommended):**
   ```bash
   sudo python3 src/gui/simple_gui.py
   ```

4. **Or use the interactive launcher:**
   ```bash
   sudo ./scripts/launch.sh
   ```

## 📁 Project Structure

```
macwhisper-security-research/
├── README.md                          # This file
├── requirements.txt                   # Dependencies (none required)
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
│
├── src/                              # Source code
│   ├── core/                         # Core functionality
│   │   └── license_server.py         # Main bypass implementation
│   ├── gui/                          # GUI applications
│   │   ├── simple_gui.py             # Simple GUI (recommended)
│   │   ├── gui_app.py                # Advanced GUI
│   │   └── launch_gui.py             # GUI launcher
│   └── utils/                        # Utility functions
│
├── scripts/                          # Utility scripts
│   └── launch.sh                     # Interactive launcher
│
├── tests/                           # Testing utilities
│   └── test_setup.py                # Setup verification
│
└── docs/                            # Documentation
    ├── QUICK_START.md               # 60-second setup guide
    ├── PROJECT_SUMMARY.md           # Project overview
    ├── STATUS_REPORT.md             # Development status
    ├── technical-documentation.md   # Complete technical docs
    └── flow-diagram.mermaid         # Architecture diagram
```

## 🔬 Technical Overview

This research demonstrates a **multi-layered approach** to application security analysis:

### Layer 1: Keychain Integration
- Analyzes macOS keychain storage mechanisms
- Demonstrates credential injection techniques
- Studies application authentication flows

### Layer 2: System Preferences
- Examines application preference storage
- Tests configuration-based license validation
- Demonstrates defaults system manipulation

### Layer 3: Network Interception
- Implements HTTP traffic redirection
- Analyzes network-based license validation
- Demonstrates local server implementation

### Layer 4: Offline License Files
- Studies application bundle modification
- Tests offline validation mechanisms
- Demonstrates file-based bypass techniques

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 60 seconds
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - High-level project overview
- **[Technical Documentation](docs/technical-documentation.md)** - Complete technical analysis
- **[Status Report](docs/STATUS_REPORT.md)** - Current development status

## 🛡️ Safety & Ethics

### Built-in Safety Features
- Automatic backups of modified system files
- Comprehensive error handling
- Graceful cleanup and restoration
- Permission validation before modifications

### Ethical Guidelines
- Use only for legitimate security research
- Respect intellectual property rights
- Follow responsible disclosure practices
- Comply with applicable laws and regulations

## 🧪 Testing

```bash
# Run setup verification
python3 tests/test_setup.py

# Verify system requirements
python3 -c "import sys; print(f'Python {sys.version}')"

# Check administrator privileges
sudo -v && echo "Admin privileges confirmed"
```

## 🤝 Contributing

This is a research project. If you're interested in contributing:

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate documentation
4. Submit a pull request with detailed explanation

Please ensure all contributions maintain the educational focus and ethical standards of the project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- macOS security research community
- Open source security tools and methodologies
- Educational institutions supporting security research

## ⚠️ Legal Notice

This software is provided for educational purposes only. The authors and contributors are not responsible for any misuse of this tool. Users must ensure they have appropriate authorization before using this tool on any software or system.

---

**For detailed usage instructions, see [docs/QUICK_START.md](docs/QUICK_START.md)**
