#!/bin/bash

# MacWhisper Pro License Bypass Tool Launcher
# Checks prerequisites and launches the GUI application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    print_color $CYAN "========================================================"
    print_color $CYAN "MacWhisper Pro License Bypass Tool"
    print_color $CYAN "Security Testing Tool for Educational Purposes"
    print_color $CYAN "========================================================"
    echo
}

check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_color $RED "❌ Error: This tool is designed for macOS only"
        print_color $YELLOW "Current OS: $OSTYPE"
        exit 1
    fi
    print_color $GREEN "✅ Operating System: macOS"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        print_color $RED "❌ Error: Python 3 is not installed"
        print_color $YELLOW "Please install Python 3.7 or higher"
        exit 1
    fi

    local python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_color $GREEN "✅ Python Version: $python_version"

    # Check if version is 3.7 or higher
    if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)"; then
        print_color $GREEN "✅ Python version compatible"
    else
        print_color $RED "❌ Error: Python 3.7 or higher required"
        print_color $YELLOW "Current version: $python_version"
        exit 1
    fi
}

check_tkinter() {
    if python3 -c "import tkinter" &> /dev/null; then
        print_color $GREEN "✅ Tkinter (GUI support) available"
    else
        print_color $RED "❌ Error: Tkinter not available"
        print_color $YELLOW "GUI functionality will not work"
        print_color $YELLOW "Consider using command line version: license_server.py"
        exit 1
    fi
}

check_permissions() {
    if [[ $EUID -eq 0 ]]; then
        print_color $GREEN "✅ Running with administrator privileges"
        return 0
    else
        print_color $YELLOW "⚠️  Warning: Not running with administrator privileges"
        print_color $YELLOW "Some features may not work properly"
        print_color $CYAN "To run with admin privileges: sudo ./launch.sh"
        return 1
    fi
}

check_files() {
    local required_files=("src/core/license_server.py" "src/gui/simple_gui.py")
    local missing_files=()

    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done

    if [[ ${#missing_files[@]} -eq 0 ]]; then
        print_color $GREEN "✅ All required files present"
        return 0
    else
        print_color $RED "❌ Error: Missing required files:"
        for file in "${missing_files[@]}"; do
            print_color $RED "   - $file"
        done
        exit 1
    fi
}

check_macwhisper() {
    local default_path="/Applications/MacWhisper.app"
    if [[ -d "$default_path" ]]; then
        print_color $GREEN "✅ MacWhisper found at: $default_path"
    else
        print_color $YELLOW "⚠️  MacWhisper not found at default location: $default_path"
        print_color $CYAN "You can specify a custom path in the GUI"
    fi
}

show_menu() {
    echo
    print_color $WHITE "Available options:"
    print_color $CYAN "1. Launch Simple GUI (Recommended)"
    print_color $CYAN "2. Launch Advanced GUI"
    print_color $CYAN "3. Command Line Mode"
    print_color $CYAN "4. Exit"
    echo
}

launch_simple_gui() {
    print_color $BLUE "🚀 Launching Simple GUI..."
    exec python3 -m src.gui.simple_gui
}

launch_advanced_gui() {
    print_color $BLUE "🚀 Launching Advanced GUI..."
    if [[ -f "src/gui/gui_app.py" ]]; then
        exec python3 -m src.gui.gui_app
    else
        print_color $RED "❌ Advanced GUI not available (src/gui/gui_app.py missing)"
        print_color $CYAN "Falling back to Simple GUI..."
        launch_simple_gui
    fi
}

launch_cli() {
    print_color $BLUE "🚀 Launching Command Line Mode..."
    exec python3 -m src.core.license_server
}

main() {
    print_header

    # System checks
    print_color $BLUE "🔍 Performing system checks..."
    check_macos
    check_python
    check_tkinter
    check_files
    check_macwhisper

    local has_admin=0
    check_permissions && has_admin=1

    echo
    print_color $GREEN "✅ System checks completed"

    # Show disclaimer
    echo
    print_color $YELLOW "⚠️  DISCLAIMER:"
    print_color $WHITE "This tool is for educational and security research purposes only."
    print_color $WHITE "Use only on software you own or have explicit permission to modify."
    print_color $WHITE "Users are responsible for complying with applicable laws."

    # Interactive mode if no arguments
    if [[ $# -eq 0 ]]; then
        while true; do
            show_menu
            read -p "Choose an option (1-4): " choice

            case $choice in
                1)
                    launch_simple_gui
                    break
                    ;;
                2)
                    launch_advanced_gui
                    break
                    ;;
                3)
                    if [[ $has_admin -eq 0 ]]; then
                        print_color $YELLOW "⚠️  Command line mode requires admin privileges"
                        read -p "Continue anyway? (y/N): " confirm
                        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
                            continue
                        fi
                    fi
                    launch_cli
                    break
                    ;;
                4)
                    print_color $CYAN "👋 Goodbye!"
                    exit 0
                    ;;
                *)
                    print_color $RED "❌ Invalid option. Please choose 1-4."
                    ;;
            esac
        done
    else
        # Command line arguments
        case "$1" in
            "gui"|"simple")
                launch_simple_gui
                ;;
            "advanced")
                launch_advanced_gui
                ;;
            "cli"|"command")
                launch_cli
                ;;
            "help"|"-h"|"--help")
                echo "Usage: $0 [option]"
                echo "Options:"
                echo "  gui, simple    Launch simple GUI (default)"
                echo "  advanced       Launch advanced GUI"
                echo "  cli, command   Launch command line mode"
                echo "  help           Show this help message"
                ;;
            *)
                print_color $RED "❌ Unknown option: $1"
                print_color $CYAN "Use '$0 help' for usage information"
                exit 1
                ;;
        esac
    fi
}

# Make sure we're in the project root directory
cd "$(dirname "$0")/.."

# Run main function
main "$@"
