#!/usr/bin/env python3
"""
MacWhisper Pro License Bypass Tool - GUI Launcher
Simple launcher for the GUI application with proper error handling.
"""

import os
import subprocess
import sys


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True


def check_macos():
    """Check if running on macOS"""
    if sys.platform != "darwin":
        print("ERROR: This tool is designed for macOS only")
        return False
    return True


def check_files():
    """Check if required files exist"""
    required_files = ["license_server.py", "gui_app.py"]
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("ERROR: Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    return True


def check_permissions():
    """Check if running with administrator privileges"""
    if os.geteuid() != 0:
        print("⚠️  Warning: This tool requires administrator privileges")
        print("To run with admin privileges:")
        print(f"sudo python3 {sys.argv[0]}")
        print("\nContinuing anyway... (some features may not work)")
        return False
    return True


def main():
    """Main launcher function"""
    print("=" * 60)
    print("MacWhisper Pro License Bypass Tool - GUI Launcher")
    print("=" * 60)

    # Check system requirements
    if not check_python_version():
        sys.exit(1)

    if not check_macos():
        sys.exit(1)

    if not check_files():
        print("\nPlease ensure all required files are in the same directory:")
        print("  - license_server.py")
        print("  - gui_app.py")
        print("  - launch_gui.py (this file)")
        sys.exit(1)

    # Check permissions
    has_admin = check_permissions()

    print(f"\n✅ Python version: {sys.version}")
    print(f"✅ Platform: {sys.platform}")
    print("✅ Required files: Present")
    print(
        f"{'✅' if has_admin else '⚠️ '} Admin privileges: {'Yes' if has_admin else 'No'}"
    )

    print("\n🚀 Launching GUI application...")

    try:
        # Launch the GUI application
        subprocess.run([sys.executable, "gui_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to launch GUI: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Launch cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
