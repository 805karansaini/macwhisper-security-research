#!/usr/bin/env python3
"""
MacWhisper Pro License Bypass - Setup Test
Verifies that all components are working correctly.
"""

import importlib
import os
import subprocess
import sys


def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python version...")
    if sys.version_info >= (3, 7):
        print(
            f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - Compatible"
        )
        return True
    else:
        print(
            f"❌ Python {sys.version_info.major}.{sys.version_info.minor} - Too old (need 3.7+)"
        )
        return False


def test_imports():
    """Test required imports"""
    print("\nTesting required imports...")

    required_modules = [
        "tkinter",
        "http.server",
        "socketserver",
        "json",
        "subprocess",
        "threading",
        "queue",
        "os",
        "sys",
        "time",
        "pathlib",
    ]

    failed_imports = []

    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module} - {e}")
            failed_imports.append(module)

    return len(failed_imports) == 0


def test_tkinter_gui():
    """Test GUI functionality"""
    print("\nTesting GUI functionality...")
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ Tkinter GUI support available")
        return True
    except Exception as e:
        print(f"❌ GUI support failed: {e}")
        return False


def test_file_structure():
    """Test file structure"""
    print("\nTesting file structure...")

    required_files = [
        "src/core/license_server.py",
        "src/gui/simple_gui.py",
        "src/gui/gui_app.py",
        "src/gui/launch_gui.py",
        "scripts/launch.sh",
        "requirements.txt",
        "README.md",
    ]

    missing_files = []

    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)

    return len(missing_files) == 0


def test_license_server_import():
    """Test license server module import"""
    print("\nTesting license server import...")
    try:
        import os
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        from core.license_server import GumroadHandler, MacWhisperBypass

        print("✅ License server module imports successfully")
        return True
    except ImportError as e:
        print(f"❌ License server import failed: {e}")
        return False


def test_simple_gui_import():
    """Test simple GUI import"""
    print("\nTesting simple GUI import...")
    try:
        # We'll just check if the file can be parsed
        gui_path = os.path.join("src", "gui", "simple_gui.py")
        with open(gui_path, "r") as f:
            content = f.read()

        # Basic syntax check
        compile(content, gui_path, "exec")
        print("✅ Simple GUI syntax valid")
        return True
    except Exception as e:
        print(f"❌ Simple GUI syntax error: {e}")
        return False


def test_permissions():
    """Test permissions"""
    print("\nTesting permissions...")

    if os.geteuid() == 0:
        print("✅ Running with administrator privileges")
        return True
    else:
        print("⚠️  Not running with administrator privileges")
        print("   Some features may not work (this is OK for testing)")
        return True


def test_macos():
    """Test macOS compatibility"""
    print("\nTesting macOS compatibility...")

    if sys.platform == "darwin":
        print("✅ Running on macOS")
        return True
    else:
        print(f"⚠️  Running on {sys.platform} (tool designed for macOS)")
        return True


def test_shell_commands():
    """Test shell command execution"""
    print("\nTesting shell command execution...")

    try:
        # Test basic command execution
        result = subprocess.run(["echo", "test"], capture_output=True, text=True)
        if result.returncode == 0 and "test" in result.stdout:
            print("✅ Shell command execution works")
            return True
        else:
            print("❌ Shell command execution failed")
            return False
    except Exception as e:
        print(f"❌ Shell command execution error: {e}")
        return False


def generate_report(results):
    """Generate test report"""
    print("\n" + "=" * 50)
    print("SETUP TEST REPORT")
    print("=" * 50)

    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)

    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {(passed_tests / total_tests) * 100:.1f}%")

    print("\nDetailed results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<25} {status}")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed! The tool is ready to use.")
        return True
    else:
        print(
            f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please address issues before using the tool."
        )
        return False


def main():
    """Main test function"""
    print("MacWhisper Pro License Bypass - Setup Test")
    print("=" * 50)

    # Run all tests
    test_results = {
        "Python Version": test_python_version(),
        "Required Imports": test_imports(),
        "GUI Support": test_tkinter_gui(),
        "File Structure": test_file_structure(),
        "License Server": test_license_server_import(),
        "Simple GUI": test_simple_gui_import(),
        "Permissions": test_permissions(),
        "macOS Compatibility": test_macos(),
        "Shell Commands": test_shell_commands(),
    }

    # Generate report
    success = generate_report(test_results)

    if success:
        print("\n🚀 Ready to launch! Use one of these commands:")
        print("   ./scripts/launch.sh                    (Interactive launcher)")
        print("   python3 src/gui/simple_gui.py          (Simple GUI)")
        print("   sudo python3 src/core/license_server.py (Command line)")
    else:
        print("\n🔧 Please fix the failed tests before proceeding.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
