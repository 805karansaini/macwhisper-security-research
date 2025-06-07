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


def check_permissions():
    """Check if running with administrator privileges"""
    if os.geteuid() != 0:
        print("⚠️  Warning: This tool requires administrator privileges")
        print("To run with admin privileges (from project root):")
        print(f"sudo {sys.executable} -m src.gui.launch_gui")
        print("\nContinuing anyway... (some features may not work)")
        return False
    return True


def main():
    """Main launcher function"""
    print("=" * 60)
    print("MacWhisper Pro License Bypass Tool - GUI Launcher")
    print("=" * 60)

    # Change to project root directory
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        os.chdir(project_root)
        print(f"ℹ️ Changed working directory to project root: {project_root}")
    except Exception as e:
        print(f"❌ ERROR: Could not change to project root directory: {e}")
        sys.exit(1)

    # Check system requirements
    if not check_python_version():
        sys.exit(1)

    if not check_macos():
        sys.exit(1)

    # check_files() is removed as gui_app.py now handles its import directly
    # and we launch gui_app.py as a module from the project root.

    # Check permissions
    has_admin = check_permissions()

    print(f"\n✅ Python version: {sys.version}")
    print(f"✅ Platform: {sys.platform}")
    # No longer checking for specific files here, as module loading handles it.
    print(
        f"{'✅' if has_admin else '⚠️ '} Admin privileges: {'Yes' if has_admin else 'No'}"
    )

    print("\n🚀 Launching GUI application as a module...")

    try:
        # Launch the GUI application as a module
        subprocess.run([sys.executable, "-m", "src.gui.gui_app"], check=True)
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
