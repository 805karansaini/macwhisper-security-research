#!/usr/bin/env python3
"""
MacWhisper Pro License Bypass - Multi-Layered Solution
Based on comprehensive security research and documentation.

This script implements a complete bypass of MacWhisper's licensing system
using multiple layers: keychain integration, preferences manipulation,
network interception, and offline license files.
"""

import http.server
import json
import os
import socketserver
import subprocess
import sys


class Colors:
    """ANSI color codes for terminal output"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    END = "\033[0m"


class MacWhisperBypass:
    def __init__(self, app_path="/Applications/MacWhisper.app", verbose=True):
        self.app_path = app_path
        self.verbose = verbose
        self.server = None
        self.server_thread = None
        self.license_key = "FAKE-LICENSE-KEY-12345-67890"
        self.license_email = "fake@email.com"
        self.backup_hosts = None

    def log(self, message, color=Colors.WHITE):
        """Print colored log message"""
        if self.verbose:
            print(f"{color}{message}{Colors.END}")

    def run_command(self, cmd, check=True, capture_output=True):
        """Run shell command with error handling"""
        try:
            if isinstance(cmd, str):
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=capture_output,
                    text=True,
                    check=check,
                )
            else:
                result = subprocess.run(
                    cmd, capture_output=capture_output, text=True, check=check
                )
            return result
        except subprocess.CalledProcessError as e:
            if self.verbose:
                self.log(f"Command failed: {e}", Colors.RED)
            return None

    def check_app_exists(self):
        """Check if MacWhisper app exists"""
        if not os.path.exists(self.app_path):
            self.log(f"❌ MacWhisper app not found at: {self.app_path}", Colors.RED)
            return False
        self.log(f"✅ Found MacWhisper app at: {self.app_path}", Colors.GREEN)
        return True

    def backup_hosts_file(self):
        """Backup the original hosts file"""
        try:
            with open("/etc/hosts", "r") as f:
                self.backup_hosts = f.read()
            self.log("✅ Backed up hosts file", Colors.GREEN)
            return True
        except Exception as e:
            self.log(f"❌ Failed to backup hosts file: {e}", Colors.RED)
            return False

    def modify_hosts_file(self):
        """Add Gumroad API redirect to hosts file"""
        hosts_entry = "127.0.0.1 api.gumroad.com"

        try:
            # Check if entry already exists
            with open("/etc/hosts", "r") as f:
                current_hosts = f.read()

            if "api.gumroad.com" in current_hosts:
                self.log("✅ Hosts file already modified", Colors.YELLOW)
                return True

            # Add entry using Python file I/O
            try:
                with open("/etc/hosts", "a") as f:
                    f.write(f"\n{hosts_entry}\n")
                self.log("✅ Modified hosts file for API redirection", Colors.GREEN)
                return True
            except (IOError, PermissionError) as e_io:
                self.log(f"❌ Failed to write to hosts file: {e_io}", Colors.RED)
                return False
            except Exception as e_generic: # Catch any other unexpected error
                self.log(f"❌ Unexpected error modifying hosts file: {e_generic}", Colors.RED)
                return False
        except Exception as e: # For the initial read operation or other issues
            self.log(f"❌ Error accessing hosts file: {e}", Colors.RED)
            return False

    def create_keychain_entry(self):
        """Add fake license key to macOS keychain"""
        cmd = [
            "security",
            "add-generic-password",
            "-s",
            "com.goodsnooze.MacWhisper",
            "-a",
            "gumroadLicenseKey_Key",
            "-w",
            self.license_key,
            "-T",
            self.app_path,
            "-U",  # Update if exists
        ]

        result = self.run_command(cmd, check=False)
        if result and result.returncode == 0:
            self.log("✅ Added license key to keychain", Colors.GREEN)
            return True
        else:
            self.log(
                "⚠️  Keychain entry may already exist or failed to add", Colors.YELLOW
            )
            return True  # Continue anyway

    def set_preferences(self):
        """Set application preferences for license validation"""
        preferences = [
            ("hasValidLicense", "bool", "true"),
            ("isProVersion", "bool", "true"),
            ("licenseValidated", "bool", "true"),
            ("gumroadLicenseEmail", "string", self.license_email),
            ("gumroadLicenseKey", "string", self.license_key),
            ("offlineLicenseValidated", "bool", "true"),
            ("proFeaturesEnabled", "bool", "true"),
        ]

        success_count = 0
        for key, type_str, value in preferences:
            cmd = f"defaults write com.goodsnooze.MacWhisper {key} -{type_str} {value}"
            result = self.run_command(cmd)
            if result and result.returncode == 0:
                success_count += 1

        self.log(f"✅ Set {success_count}/{len(preferences)} preferences", Colors.GREEN)
        return success_count > len(preferences) // 2

    def create_offline_license_files(self):
        """Create offline license files in app bundle"""
        license_data = {
            "license_key": self.license_key,
            "email": self.license_email,
            "purchase_date": "2024-01-01T00:00:00Z",
            "verified": True,
            "pro_enabled": True,
            "features": {
                "unlimited_transcription": True,
                "batch_processing": True,
                "advanced_models": True,
                "export_formats": ["txt", "srt", "vtt", "json"],
            },
        }

        license_paths = [
            f"{self.app_path}/Contents/Resources/license.json",
            f"{self.app_path}/Contents/Resources/offline_license.json",
            f"{self.app_path}/Contents/Resources/fake_license.json",
            f"{self.app_path}/Contents/Resources/pro_license.json",
        ]

        success_count = 0
        for path in license_paths:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w") as f:
                    json.dump(license_data, f, indent=2)
                success_count += 1
            except Exception as e:
                if self.verbose:
                    self.log(f"⚠️  Could not create {path}: {e}", Colors.YELLOW)

        self.log(
            f"✅ Created {success_count}/{len(license_paths)} license files",
            Colors.GREEN,
        )
        return success_count > 0

    def remove_app_signature(self):
        """Remove existing app signature"""
        cmd = ["codesign", "--remove-signature", self.app_path]
        result = self.run_command(cmd, check=False)
        if result and result.returncode == 0:
            self.log("✅ Removed app signature", Colors.GREEN)
            return True
        else:
            self.log("⚠️  Could not remove signature (may not exist)", Colors.YELLOW)
            return True  # Continue anyway

    def resign_app(self):
        """Re-sign app with ad-hoc signature"""
        # Remove quarantine attributes
        cmd1 = ["xattr", "-cr", self.app_path]
        self.run_command(cmd1, check=False)

        # Apply ad-hoc signature
        cmd2 = ["codesign", "-s", "-", "--force", "--deep", self.app_path]
        result = self.run_command(cmd2, check=False)

        if result and result.returncode == 0:
            self.log("✅ Re-signed app successfully", Colors.GREEN)
            return True
        else:
            self.log("❌ Failed to re-sign app", Colors.RED)
            return False

    def cleanup(self):
        """Restore original system settings"""
        self.log("🧹 Cleaning up system modifications...", Colors.CYAN)

        # Restore hosts file
        if self.backup_hosts:
            try:
                with open("/etc/hosts", "w") as f:
                    f.write(self.backup_hosts)
                self.log("✅ Restored hosts file", Colors.GREEN)
            except Exception as e:
                self.log(f"❌ Failed to restore hosts file: {e}", Colors.RED)
        else:
            # Remove the api.gumroad.com entry
            try:
                with open("/etc/hosts", "r") as f:
                    lines = f.readlines()

                with open("/etc/hosts", "w") as f:
                    for line in lines:
                        if "api.gumroad.com" not in line:
                            f.write(line)
                self.log("✅ Removed hosts file modifications", Colors.GREEN)
            except Exception as e:
                self.log(f"❌ Failed to clean hosts file: {e}", Colors.RED)

        # Remove keychain entries
        try:
            cmd = [
                "security",
                "delete-generic-password",
                "-s",
                "com.goodsnooze.MacWhisper",
            ]
            self.run_command(cmd, check=False)
            self.log("✅ Removed keychain entries", Colors.GREEN)
        except Exception as e:
            self.log(f"⚠️  Could not remove keychain entries: {e}", Colors.YELLOW)

        # Reset preferences
        try:
            cmd = "defaults delete com.goodsnooze.MacWhisper"
            self.run_command(cmd, check=False)
            self.log("✅ Reset application preferences", Colors.GREEN)
        except Exception as e:
            self.log(f"⚠️  Could not reset preferences: {e}", Colors.YELLOW)

        self.log("✅ Cleanup complete", Colors.GREEN)


class GumroadHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for fake Gumroad API responses"""

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

    def do_POST(self):
        if self.path == "/v2/licenses/verify":
            # Fake successful license verification
            response = {
                "success": True,
                "uses": 0,
                "purchase": {
                    "id": "fake_purchase_12345",
                    "email": "fake@email.com",
                    "price": 2900,
                    "currency": "USD",
                    "license_key": "FAKE-LICENSE-KEY-12345-67890",
                    "refunded": False,
                    "chargebacked": False,
                    "test": False,
                    "sale_timestamp": "2024-01-01T00:00:00Z",
                },
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response_json = json.dumps(response)
            self.wfile.write(response_json.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Fake Gumroad API Server Running")


def start_license_server(port=8080):
    """Start the fake license server"""
    try:
        with socketserver.TCPServer(("", port), GumroadHandler) as httpd:
            print(f"{Colors.GREEN}✅ License server running on port {port}{Colors.END}")
            httpd.serve_forever()
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to start server: {e}{Colors.END}")


def main():
    """Main execution function"""
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        # Cleanup mode
        bypass = MacWhisperBypass()
        bypass.cleanup()
        return

    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 60)
    print("MacWhisper Pro License Bypass - Multi-Layered Solution")
    print("=" * 60)
    print(f"{Colors.END}")

    # Check for sudo privileges
    if os.geteuid() != 0:
        print(
            f"{Colors.RED}❌ This script requires sudo privileges to modify hosts file{Colors.END}"
        )
        print(f"{Colors.YELLOW}Please run: sudo python3 license_server.py{Colors.END}")
        sys.exit(1)

    bypass = MacWhisperBypass()

    # Check if app exists
    if not bypass.check_app_exists():
        print(
            f"{Colors.RED}Please ensure MacWhisper.app is installed in /Applications/{Colors.END}"
        )
        sys.exit(1)

    print(f"\n{Colors.BLUE}🔧 Applying multi-layered bypass...{Colors.END}")

    # Step 1: Backup and modify hosts file
    bypass.log("\n1️⃣ Configuring network interception...", Colors.CYAN)
    bypass.backup_hosts_file()
    bypass.modify_hosts_file()

    # Step 2: Create keychain entry
    bypass.log("\n2️⃣ Injecting license data into keychain...", Colors.CYAN)
    bypass.create_keychain_entry()

    # Step 3: Set preferences
    bypass.log("\n3️⃣ Setting application preferences...", Colors.CYAN)
    bypass.set_preferences()

    # Step 4: Create offline license files
    bypass.log("\n4️⃣ Creating offline license files...", Colors.CYAN)
    bypass.create_offline_license_files()

    # Step 5: Re-sign app
    bypass.log("\n5️⃣ Re-signing application...", Colors.CYAN)
    bypass.remove_app_signature()
    bypass.resign_app()

    # Step 6: Start license server
    bypass.log("\n6️⃣ Starting license validation server...", Colors.CYAN)

    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Multi-layered bypass complete!{Colors.END}")
    print(
        f"{Colors.WHITE}The license server will now run to handle validation requests.{Colors.END}"
    )
    print(
        f"{Colors.YELLOW}Keep this terminal open and launch MacWhisper.app{Colors.END}"
    )
    print(f"{Colors.CYAN}Press Ctrl+C to stop the server{Colors.END}\n")

    try:
        start_license_server(8080)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 License server stopped{Colors.END}")
        print(
            f"{Colors.WHITE}Run 'sudo python3 license_server.py cleanup' to restore original settings{Colors.END}"
        )


if __name__ == "__main__":
    main()
