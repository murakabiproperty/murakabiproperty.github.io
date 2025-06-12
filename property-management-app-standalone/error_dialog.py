"""
Enhanced Error Dialog for Property Management System
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path
from datetime import datetime
import subprocess
import sys

class DetailedErrorDialog:
    def __init__(self, parent, title, message, details=None, suggestions=None):
        self.parent = parent
        self.title = title
        self.message = message
        self.details = details or "No additional details available."
        self.suggestions = suggestions or []
        
        self.create_dialog()
    
    def create_dialog(self):
        """Create the detailed error dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("600x500")
        self.dialog.configure(bg='white')
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Main content frame
        main_frame = tk.Frame(self.dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Error icon and title
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, text=self.title, font=("Arial", 16, "bold"), 
                              bg='white', fg='#e74c3c')
        title_label.pack(anchor='w')
        
        # Main message
        message_label = tk.Label(main_frame, text=self.message, font=("Arial", 12), 
                               bg='white', fg='#34495e', wraplength=550, justify='left')
        message_label.pack(anchor='w', pady=(0, 15))
        
        # Details section
        details_frame = tk.LabelFrame(main_frame, text="Error Details", font=("Arial", 10, "bold"),
                                    bg='white', fg='#7f8c8d')
        details_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Scrollable text for details
        details_text = scrolledtext.ScrolledText(details_frame, height=8, width=60, 
                                               font=("Courier", 9), bg='#f8f9fa', 
                                               fg='#2c3e50')
        details_text.pack(fill='both', expand=True, padx=10, pady=10)
        details_text.insert('1.0', self.details)
        details_text.config(state='disabled')
        
        # Suggestions section
        if self.suggestions:
            suggestions_frame = tk.LabelFrame(main_frame, text="Suggested Actions", 
                                            font=("Arial", 10, "bold"), bg='white', 
                                            fg='#27ae60')
            suggestions_frame.pack(fill='x', pady=(0, 15))
            
            for i, suggestion in enumerate(self.suggestions, 1):
                suggestion_label = tk.Label(suggestions_frame, 
                                          text=f"{i}. {suggestion}", 
                                          font=("Arial", 10), bg='white', fg='#2c3e50',
                                          wraplength=550, justify='left')
                suggestion_label.pack(anchor='w', padx=10, pady=5)
        
        # Action buttons
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(fill='x')
        
        # Run debug button
        debug_btn = tk.Button(buttons_frame, text="Run Debug", font=("Arial", 10),
                             bg='#3498db', fg='white', padx=15, pady=8,
                             command=self.run_debug)
        debug_btn.pack(side='left', padx=(0, 10))
        
        # View logs button
        logs_btn = tk.Button(buttons_frame, text="View Logs", font=("Arial", 10),
                            bg='#9b59b6', fg='white', padx=15, pady=8,
                            command=self.view_logs)
        logs_btn.pack(side='left', padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(buttons_frame, text="Close", font=("Arial", 10),
                             bg='#95a5a6', fg='white', padx=20, pady=8,
                             command=self.dialog.destroy)
        close_btn.pack(side='right')
        
        # Focus on close button
        close_btn.focus_set()
        
        # Bind escape key to close
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
    
    def run_debug(self):
        """Run debug script"""
        try:
            debug_script = Path("debug_edit_sync.py")
            if debug_script.exists():
                subprocess.Popen([sys.executable, str(debug_script)], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                messagebox.showinfo("Debug Started", 
                                  "Debug script is running in a new console window.")
            else:
                messagebox.showerror("Debug Script Not Found", 
                                   "The debug script was not found.")
        except Exception as e:
            messagebox.showerror("Error Running Debug", f"Failed to run debug script: {str(e)}")
    
    def view_logs(self):
        """View error logs"""
        try:
            log_viewer = Path("view_sync_errors.py")
            if log_viewer.exists():
                subprocess.Popen([sys.executable, str(log_viewer)], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                messagebox.showinfo("Log Viewer Started", 
                                  "Log viewer is running in a new console window.")
            else:
                messagebox.showerror("Log Viewer Not Found", 
                                   "The log viewer was not found.")
        except Exception as e:
            messagebox.showerror("Error Opening Logs", f"Failed to open log viewer: {str(e)}")

def show_sync_error(parent, error_message, detailed_error=None):
    """Show a detailed sync error dialog"""
    suggestions = [
        "Check your internet connection",
        "Run debug script to test Airtable connection",
        "Check if the record still exists in Airtable",
        "Verify Airtable API credentials",
        "Try editing the property again after a few minutes"
    ]
    
    details = f"""Error: {error_message}

Detailed Information:
{detailed_error or 'No additional details available.'}

Possible Causes:
- Network connectivity issues
- Airtable record was deleted
- Invalid API credentials
- Temporary Airtable service issues

Troubleshooting Steps:
1. Run the debug script to test the connection
2. Check the logs for more detailed error information
3. Verify that the record exists in your Airtable base
4. Ensure your API key has proper permissions
"""
    
    DetailedErrorDialog(
        parent=parent,
        title="Airtable Synchronization Failed",
        message="The property was updated locally but failed to sync with Airtable.",
        details=details,
        suggestions=suggestions
    ) 