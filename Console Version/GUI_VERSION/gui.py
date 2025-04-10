import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class TypingSpeedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Tester")
        self.root.geometry("600x400")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Create title
        tk.Label(self.main_frame, text="Welcome to Typing Speed Tester", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        # Create mode selection frame
        mode_frame = tk.Frame(self.main_frame)
        mode_frame.pack(pady=20)
        
        # GUI Mode button
        self.gui_button = tk.Button(mode_frame, text="Start GUI Mode", 
                                  command=self.start_gui_mode,
                                  width=20, height=2)
        self.gui_button.pack(side=tk.LEFT, padx=10)
        
        # Terminal Mode button
        self.terminal_button = tk.Button(mode_frame, text="Switch to Terminal Mode",
                                       command=self.switch_to_terminal,
                                       width=20, height=2)
        self.terminal_button.pack(side=tk.RIGHT, padx=10)
        
        # Status label
        self.status_label = tk.Label(self.main_frame, text="", 
                                   font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        self.update_status()
        
    def update_status(self):
        self.status_label.config(text="Select your preferred mode to continue")
        
    def start_gui_mode(self):
        # This will be implemented later when we add the main GUI functionality
        messagebox.showinfo("Coming Soon", "GUI mode will be implemented soon!")
        
    def switch_to_terminal(self):
        # Close the GUI window
        self.root.destroy()
        
        # Get the path to the console version
        console_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  "CONSOLE-APP_CONSOLE-APP", "main.py")
        
        # Run the console version
        try:
            subprocess.run([sys.executable, console_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start terminal version: {str(e)}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TypingSpeedGUI()
    app.run()
