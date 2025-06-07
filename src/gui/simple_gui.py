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

from src.core.license_server import MacWhisperBypass, GumroadHandler


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

            self.bypass = MacWhisperBypass(app_path=self.app_path.get(), verbose=False)

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
            self.bypass.create_offline_license_files()

            self.log("✍️ Re-signing app...")
            self.log("   Removing app signature...")
            self.bypass.remove_app_signature()
            self.log("   Re-signing app...")
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
                with socketserver.TCPServer(("", 8080), GumroadHandler) as httpd:
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
