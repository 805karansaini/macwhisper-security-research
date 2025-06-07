#!/usr/bin/env python3
"""
MacWhisper Pro License Bypass - GUI Application
A user-friendly interface for the multi-layered license bypass solution.
"""

import os
import queue
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# Import license_server functionality
try:
    from license_server import GumroadHandler, MacWhisperBypass
except ImportError:
    print("ERROR: license_server.py module not found!")
    print("Make sure license_server.py is in the same directory as gui_app.py")
    sys.exit(1)


class MacWhisperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MacWhisper Pro License Bypass Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Variables
        self.app_path = tk.StringVar(value="/Applications/MacWhisper.app")
        self.bypass_instance = None
        self.server_thread = None
        self.server_running = False
        self.log_queue = queue.Queue()

        # Setup GUI
        self.setup_gui()

        # Start log processing
        self.process_log_queue()

    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="MacWhisper Pro License Bypass Tool",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # App path selection
        ttk.Label(
            main_frame, text="MacWhisper App Path:", font=("Arial", 10, "bold")
        ).grid(row=1, column=0, sticky=tk.W, pady=5)

        path_frame = ttk.Frame(main_frame)
        path_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15)
        )
        path_frame.columnconfigure(0, weight=1)

        self.path_entry = ttk.Entry(path_frame, textvariable=self.app_path, width=60)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        browse_button = ttk.Button(path_frame, text="Browse", command=self.browse_app)
        browse_button.grid(row=0, column=1)

        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15)
        )
        status_frame.columnconfigure(1, weight=1)

        self.status_label = ttk.Label(
            status_frame, text="Ready to apply bypass", foreground="blue"
        )
        self.status_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0)
        )

        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 15))

        self.apply_button = ttk.Button(
            button_frame,
            text="Apply Bypass",
            command=self.apply_bypass,
            style="Accent.TButton",
        )
        self.apply_button.pack(side=tk.LEFT, padx=(0, 10))

        self.launch_button = ttk.Button(
            button_frame,
            text="Launch MacWhisper",
            command=self.launch_app,
            state="disabled",
        )
        self.launch_button.pack(side=tk.LEFT, padx=(0, 10))

        self.cleanup_button = ttk.Button(
            button_frame, text="Cleanup", command=self.cleanup, state="disabled"
        )
        self.cleanup_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = ttk.Button(
            button_frame, text="Stop Server", command=self.stop_server, state="disabled"
        )
        self.stop_button.pack(side=tk.LEFT)

        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # Configure main frame row weight for log expansion
        main_frame.rowconfigure(5, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=15, width=80, font=("Consolas", 10)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10")
        info_frame.grid(
            row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        instructions = """Instructions:
1. Ensure MacWhisper.app is installed (default: /Applications/MacWhisper.app)
2. Click 'Apply Bypass' to configure the license bypass
3. Keep this application running and click 'Launch MacWhisper'
4. Use 'Cleanup' to restore original settings when done

Note: This tool requires administrator privileges for system modifications."""

        info_label = ttk.Label(
            info_frame, text=instructions, justify=tk.LEFT, font=("Arial", 9)
        )
        info_label.grid(row=0, column=0, sticky=tk.W)

    def browse_app(self):
        """Browse for MacWhisper.app location"""
        filename = filedialog.askopenfilename(
            title="Select MacWhisper.app",
            initialdir="/Applications",
            filetypes=[("Application", "*.app"), ("All files", "*.*")],
        )
        if filename:
            self.app_path.set(filename)

    def log_message(self, message, level="INFO"):
        """Add message to log queue for thread-safe logging"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        self.log_queue.put(formatted_message)

    def process_log_queue(self):
        """Process log messages from queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass

        # Schedule next check
        self.root.after(100, self.process_log_queue)

    def update_status(self, message, color="black"):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)

    def check_permissions(self):
        """Check if running with necessary permissions"""
        if os.geteuid() != 0:
            messagebox.showerror(
                "Permission Error",
                "This application requires administrator privileges.\n\n"
                "Please run with sudo:\nsudo python3 gui_app.py",
            )
            return False
        return True

    def apply_bypass_thread(self):
        """Apply bypass in separate thread"""
        try:
            self.log_message("Starting MacWhisper Pro license bypass...")
            self.log_message("=" * 50)

            # Create bypass instance
            self.bypass_instance = MacWhisperBypass(
                app_path=self.app_path.get(), verbose=False
            )

            # Check app exists
            if not self.bypass_instance.check_app_exists():
                self.log_message("ERROR: MacWhisper app not found!", "ERROR")
                self.update_status("❌ App not found", "red")
                self.progress.stop()
                self.apply_button.config(state="normal")
                return

            self.log_message("✅ Found MacWhisper app")

            # Step 1: Network configuration
            self.log_message("📡 Configuring network interception...")
            self.bypass_instance.backup_hosts_file()
            self.bypass_instance.modify_hosts_file()

            # Step 2: Keychain
            self.log_message("🔑 Injecting license data into keychain...")
            self.bypass_instance.create_keychain_entry()

            # Step 3: Preferences
            self.log_message("⚙️  Setting application preferences...")
            self.bypass_instance.set_preferences()

            # Step 4: License files
            self.log_message("📄 Creating offline license files...")
            self.bypass_instance.create_offline_license_files()

            # Step 5: Re-signing
            self.log_message("✍️  Re-signing application...")
            self.bypass_instance.remove_app_signature()
            if not self.bypass_instance.resign_app():
                self.log_message(
                    "WARNING: App re-signing failed, may not launch", "WARNING"
                )

            # Step 6: Start server
            self.log_message("🚀 Starting license validation server...")
            self.start_server_thread()

            self.log_message("=" * 50)
            self.log_message("🎉 License bypass applied successfully!")
            self.log_message("You can now launch MacWhisper with Pro features enabled.")

            self.update_status("✅ Bypass applied successfully", "green")

            # Update button states
            self.root.after(
                0,
                lambda: [
                    self.apply_button.config(state="disabled"),
                    self.launch_button.config(state="normal"),
                    self.cleanup_button.config(state="normal"),
                    self.stop_button.config(state="normal"),
                ],
            )

        except Exception as e:
            self.log_message(f"ERROR: {str(e)}", "ERROR")
            self.update_status("❌ Bypass failed", "red")
        finally:
            self.progress.stop()

    def apply_bypass(self):
        """Apply the license bypass"""
        if not self.check_permissions():
            return

        # Verify app path
        if not os.path.exists(self.app_path.get()):
            messagebox.showerror(
                "Error", f"MacWhisper app not found at:\n{self.app_path.get()}"
            )
            return

        # Confirm action
        result = messagebox.askyesno(
            "Confirm Action",
            "This will modify system settings to bypass MacWhisper's license validation.\n\n"
            "Continue?",
        )

        if not result:
            return

        # Start bypass process
        self.update_status("⏳ Applying bypass...", "orange")
        self.progress.start()
        self.apply_button.config(state="disabled")

        # Run in thread to prevent GUI freezing
        thread = threading.Thread(target=self.apply_bypass_thread)
        thread.daemon = True
        thread.start()

    def start_server_thread(self):
        """Start the license server in a separate thread"""

        def server_runner():
            try:
                self.server_running = True
                self.log_message("🌐 License server started on port 8080")
                import socketserver

                with socketserver.TCPServer(("", 8080), GumroadHandler) as httpd:
                    while self.server_running:
                        httpd.handle_request()
            except Exception as e:
                self.log_message(f"Server error: {e}", "ERROR")

        self.server_thread = threading.Thread(target=server_runner)
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop_server(self):
        """Stop the license server"""
        self.server_running = False
        if self.server_thread:
            self.log_message("🛑 Stopping license server...")
            self.update_status("🛑 Server stopped", "orange")
            self.stop_button.config(state="disabled")

    def launch_app(self):
        """Launch MacWhisper application"""
        try:
            self.log_message("🚀 Launching MacWhisper...")
            subprocess.Popen(["open", self.app_path.get()])
            self.log_message("✅ MacWhisper launched successfully")
        except Exception as e:
            self.log_message(f"ERROR launching app: {e}", "ERROR")
            messagebox.showerror("Launch Error", f"Failed to launch MacWhisper:\n{e}")

    def cleanup(self):
        """Cleanup system modifications"""
        result = messagebox.askyesno(
            "Confirm Cleanup",
            "This will restore original system settings and remove the license bypass.\n\n"
            "Continue?",
        )

        if not result:
            return

        self.log_message("🧹 Starting cleanup process...")

        if self.bypass_instance:
            try:
                self.bypass_instance.cleanup()
                self.log_message("✅ Cleanup completed successfully")
                self.update_status("✅ Cleanup completed", "green")
            except Exception as e:
                self.log_message(f"ERROR during cleanup: {e}", "ERROR")
                self.update_status("❌ Cleanup failed", "red")

        # Stop server
        self.stop_server()

        # Reset button states
        self.apply_button.config(state="normal")
        self.launch_button.config(state="disabled")
        self.cleanup_button.config(state="disabled")
        self.stop_button.config(state="disabled")

    def on_closing(self):
        """Handle application closing"""
        if self.server_running:
            result = messagebox.askyesno(
                "Confirm Exit",
                "The license server is still running.\n\n"
                "Do you want to stop it and exit?",
            )
            if result:
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main GUI application entry point"""
    # license_server classes are already imported at the top of the file

    # Create and run GUI
    root = tk.Tk()
    app = MacWhisperGUI(root)

    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Add icon and other window properties
    try:
        # Set window icon (if available)
        root.iconname("MacWhisper Bypass")
    except Exception as e:
        print(f"Error setting window icon: {e}")
        pass

    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    print("Starting MacWhisper Pro License Bypass GUI...")
    print("Note: This application requires administrator privileges.")

    root.mainloop()


if __name__ == "__main__":
    main()
