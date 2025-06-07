#!/usr/bin/env python3
"""
MacWhisper Pro License Bypass - Simple GUI
A simplified GUI interface that avoids import issues.
"""

import http.server
import json
import os
import queue
import socketserver
import subprocess
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk


class SimpleLicenseBypass:
    """Simplified license bypass implementation"""

    def __init__(self, app_path="/Applications/MacWhisper.app"):
        self.app_path = app_path
        self.license_key = "FAKE-LICENSE-KEY-12345-67890"
        self.license_email = "fake@email.com"
        self.backup_hosts = None

    def run_command(self, cmd, check=False):
        """Run shell command"""
        try:
            if isinstance(cmd, str):
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, check=check
                )
            else:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=check
                )
            return result
        except subprocess.CalledProcessError:
            return None

    def check_app_exists(self):
        """Check if MacWhisper app exists"""
        return os.path.exists(self.app_path)

    def backup_hosts_file(self):
        """Backup the original hosts file"""
        try:
            with open("/etc/hosts", "r") as f:
                self.backup_hosts = f.read()
            return True
        except Exception:
            return False

    def modify_hosts_file(self):
        """Add Gumroad API redirect to hosts file"""
        try:
            with open("/etc/hosts", "r") as f:
                current_hosts = f.read()

            if "api.gumroad.com" not in current_hosts:
                cmd = 'echo "127.0.0.1 api.gumroad.com" | sudo tee -a /etc/hosts'
                result = self.run_command(cmd)
                return result and result.returncode == 0
            return True
        except Exception:
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
            "-U",
        ]
        result = self.run_command(cmd)
        return result is not None

    def set_preferences(self):
        """Set application preferences"""
        preferences = [
            ("hasValidLicense", "bool", "true"),
            ("isProVersion", "bool", "true"),
            ("licenseValidated", "bool", "true"),
            ("gumroadLicenseEmail", "string", self.license_email),
        ]

        success_count = 0
        for key, type_str, value in preferences:
            cmd = f"defaults write com.goodsnooze.MacWhisper {key} -{type_str} {value}"
            result = self.run_command(cmd)
            if result and result.returncode == 0:
                success_count += 1

        return success_count > 0

    def create_license_files(self):
        """Create offline license files"""
        license_data = {
            "license_key": self.license_key,
            "email": self.license_email,
            "purchase_date": "2024-01-01T00:00:00Z",
            "verified": True,
            "pro_enabled": True,
        }

        try:
            license_path = f"{self.app_path}/Contents/Resources/license.json"
            os.makedirs(os.path.dirname(license_path), exist_ok=True)
            with open(license_path, "w") as f:
                json.dump(license_data, f, indent=2)
            return True
        except Exception:
            return False

    def resign_app(self):
        """Re-sign the application"""
        # Remove quarantine
        cmd1 = ["xattr", "-cr", self.app_path]
        self.run_command(cmd1)

        # Remove signature
        cmd2 = ["codesign", "--remove-signature", self.app_path]
        self.run_command(cmd2)

        # Re-sign
        cmd3 = ["codesign", "-s", "-", "--force", "--deep", self.app_path]
        result = self.run_command(cmd3)
        return result and result.returncode == 0

    def cleanup(self):
        """Restore original settings"""
        # Restore hosts file
        if self.backup_hosts:
            try:
                with open("/etc/hosts", "w") as f:
                    f.write(self.backup_hosts)
            except Exception:
                pass

        # Remove keychain entry
        cmd = ["security", "delete-generic-password", "-s", "com.goodsnooze.MacWhisper"]
        self.run_command(cmd)

        # Reset preferences
        cmd = "defaults delete com.goodsnooze.MacWhisper"
        self.run_command(cmd)


class FakeGumroadHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for fake license responses"""

    def log_message(self, format, *args):
        pass

    def do_POST(self):
        if self.path == "/v2/licenses/verify":
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
                },
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Fake Gumroad Server Running")


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MacWhisper Pro License Bypass")
        self.root.geometry("700x600")

        # Variables
        self.app_path = tk.StringVar(value="/Applications/MacWhisper.app")
        self.bypass = None
        self.server_thread = None
        self.server_running = False
        self.log_queue = queue.Queue()

        self.setup_gui()
        self.process_logs()

    def setup_gui(self):
        """Setup the GUI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            main_frame,
            text="MacWhisper Pro License Bypass Tool",
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=(0, 20))

        # App path
        path_frame = ttk.LabelFrame(
            main_frame, text="MacWhisper App Path", padding="10"
        )
        path_frame.pack(fill=tk.X, pady=(0, 10))

        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X)

        self.path_entry = ttk.Entry(path_entry_frame, textvariable=self.app_path)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_btn = ttk.Button(
            path_entry_frame, text="Browse", command=self.browse_app
        )
        browse_btn.pack(side=tk.RIGHT)

        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))

        self.status_label = ttk.Label(status_frame, text="Ready", foreground="blue")
        self.status_label.pack(anchor=tk.W)

        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(10, 0))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.apply_btn = ttk.Button(
            button_frame, text="Apply Bypass", command=self.apply_bypass
        )
        self.apply_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.launch_btn = ttk.Button(
            button_frame,
            text="Launch MacWhisper",
            command=self.launch_app,
            state="disabled",
        )
        self.launch_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.cleanup_btn = ttk.Button(
            button_frame, text="Cleanup", command=self.cleanup, state="disabled"
        )
        self.cleanup_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_btn = ttk.Button(
            button_frame, text="Stop Server", command=self.stop_server, state="disabled"
        )
        self.stop_btn.pack(side=tk.LEFT)

        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Instructions
        info_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10")
        info_frame.pack(fill=tk.X)

        instructions = """1. Verify MacWhisper app path above
2. Click 'Apply Bypass' to configure license bypass
3. Click 'Launch MacWhisper' to start app with Pro features
4. Use 'Cleanup' to restore settings when done

Note: Requires administrator privileges (run with sudo)"""

        info_label = ttk.Label(info_frame, text=instructions, justify=tk.LEFT)
        info_label.pack(anchor=tk.W)

    def browse_app(self):
        """Browse for app"""
        filename = filedialog.askopenfilename(
            title="Select MacWhisper.app",
            initialdir="/Applications",
            filetypes=[("Application", "*.app")],
        )
        if filename:
            self.app_path.set(filename)

    def log(self, message):
        """Add log message"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")

    def process_logs(self):
        """Process log queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.process_logs)

    def update_status(self, text, color="black"):
        """Update status"""
        self.status_label.config(text=text, foreground=color)

    def check_permissions(self):
        """Check admin privileges"""
        if os.geteuid() != 0:
            messagebox.showerror(
                "Permission Error",
                "This tool requires administrator privileges.\n\n"
                "Please run with: sudo python3 simple_gui.py",
            )
            return False
        return True

    def apply_bypass_worker(self):
        """Apply bypass in thread"""
        try:
            self.log("Starting MacWhisper bypass...")

            self.bypass = SimpleLicenseBypass(self.app_path.get())

            if not self.bypass.check_app_exists():
                self.log("ERROR: MacWhisper app not found!")
                self.update_status("App not found", "red")
                return

            self.log("✅ Found MacWhisper app")

            self.log("📡 Configuring network interception...")
            self.bypass.backup_hosts_file()
            self.bypass.modify_hosts_file()

            self.log("🔑 Adding keychain entry...")
            self.bypass.create_keychain_entry()

            self.log("⚙️ Setting preferences...")
            self.bypass.set_preferences()

            self.log("📄 Creating license files...")
            self.bypass.create_license_files()

            self.log("✍️ Re-signing app...")
            if not self.bypass.resign_app():
                self.log("WARNING: Re-signing failed")

            self.log("🚀 Starting license server...")
            self.start_server()

            self.log("🎉 Bypass applied successfully!")
            self.update_status("Bypass applied", "green")

            # Update buttons
            self.root.after(0, self.enable_post_bypass_buttons)

        except Exception as e:
            self.log(f"ERROR: {e}")
            self.update_status("Bypass failed", "red")
        finally:
            self.progress.stop()

    def apply_bypass(self):
        """Apply the bypass"""
        if not self.check_permissions():
            return

        if not os.path.exists(self.app_path.get()):
            messagebox.showerror("Error", f"App not found: {self.app_path.get()}")
            return

        result = messagebox.askyesno("Confirm", "Apply MacWhisper license bypass?")
        if not result:
            return

        self.update_status("Applying bypass...", "orange")
        self.progress.start()
        self.apply_btn.config(state="disabled")

        thread = threading.Thread(target=self.apply_bypass_worker, daemon=True)
        thread.start()

    def enable_post_bypass_buttons(self):
        """Enable buttons after successful bypass"""
        self.apply_btn.config(state="disabled")
        self.launch_btn.config(state="normal")
        self.cleanup_btn.config(state="normal")
        self.stop_btn.config(state="normal")

    def start_server(self):
        """Start license server"""

        def server_worker():
            try:
                self.server_running = True
                with socketserver.TCPServer(("", 8080), FakeGumroadHandler) as httpd:
                    self.log("🌐 License server started on port 8080")
                    while self.server_running:
                        httpd.handle_request()
            except Exception as e:
                self.log(f"Server error: {e}")

        self.server_thread = threading.Thread(target=server_worker, daemon=True)
        self.server_thread.start()

    def stop_server(self):
        """Stop license server"""
        self.server_running = False
        self.log("🛑 Stopping license server...")
        self.update_status("Server stopped", "orange")
        self.stop_btn.config(state="disabled")

    def launch_app(self):
        """Launch MacWhisper"""
        try:
            self.log("🚀 Launching MacWhisper...")
            subprocess.Popen(["open", self.app_path.get()])
            self.log("✅ MacWhisper launched")
        except Exception as e:
            self.log(f"Launch error: {e}")
            messagebox.showerror("Launch Error", f"Failed to launch: {e}")

    def cleanup(self):
        """Cleanup system modifications"""
        result = messagebox.askyesno(
            "Confirm Cleanup", "Restore original system settings?"
        )
        if not result:
            return

        self.log("🧹 Starting cleanup...")

        if self.bypass:
            try:
                self.bypass.cleanup()
                self.log("✅ Cleanup completed")
                self.update_status("Cleanup completed", "green")
            except Exception as e:
                self.log(f"Cleanup error: {e}")

        self.stop_server()

        # Reset buttons
        self.apply_btn.config(state="normal")
        self.launch_btn.config(state="disabled")
        self.cleanup_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SimpleGUI(root)

    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    def on_closing():
        if hasattr(app, "server_running") and app.server_running:
            result = messagebox.askyesno(
                "Confirm Exit", "License server is running. Stop and exit?"
            )
            if result:
                app.stop_server()
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    print("MacWhisper Pro License Bypass GUI")
    print("Note: Requires administrator privileges")
    root.mainloop()


if __name__ == "__main__":
    main()
