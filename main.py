import customtkinter as ctk
import sqlite3
import bcrypt
import random
import time
from typing import Optional
from datetime import datetime

class TypeSpeedTester:
    def __init__(self):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Type Speed Tester")
        self.root.geometry("800x600")
        
        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Database initialization
        self.init_database()
        
        # Variables
        self.current_user: Optional[str] = None
        self.test_started = False
        self.start_time = 0
        self.words_typed = 0
        self.correct_words = 0
        
        # Create and show login frame
        self.show_login_frame()
        
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect('typespeed.db')
        c = conn.cursor()
        
        # Create users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password TEXT)''')
        
        # Create scores table
        c.execute('''CREATE TABLE IF NOT EXISTS scores
                    (username TEXT, wpm REAL, accuracy REAL, timestamp TEXT,
                    FOREIGN KEY(username) REFERENCES users(username))''')
        
        conn.commit()
        conn.close()

    def show_login_frame(self):
        """Display login interface"""
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title = ctk.CTkLabel(self.login_frame, text="Type Speed Tester", 
                            font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Username entry
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(self.login_frame, 
                                         placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)
        
        # Login button
        login_btn = ctk.CTkButton(self.login_frame, text="Login", 
                                 command=self.login)
        login_btn.pack(pady=10)
        
        # Register button
        register_btn = ctk.CTkButton(self.login_frame, text="Register", 
                                    command=self.register)
        register_btn.pack(pady=10)

    def login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        conn = sqlite3.connect('typespeed.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        result = c.fetchone()
        
        if result and bcrypt.checkpw(password.encode(), result[0]):
            self.current_user = username
            self.login_frame.destroy()
            self.show_main_interface()
        else:
            error = ctk.CTkLabel(self.login_frame, text="Invalid credentials", 
                                text_color="red")
            error.pack(pady=10)
        
        conn.close()

    def register(self):
        """Handle user registration"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            error = ctk.CTkLabel(self.login_frame, text="Please fill all fields", 
                                text_color="red")
            error.pack(pady=10)
            return
        
        conn = sqlite3.connect('typespeed.db')
        c = conn.cursor()
        
        # Check if username exists
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        if c.fetchone():
            error = ctk.CTkLabel(self.login_frame, text="Username already exists", 
                                text_color="red")
            error.pack(pady=10)
            return
        
        # Hash password and store user
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        
        success = ctk.CTkLabel(self.login_frame, text="Registration successful!", 
                              text_color="green")
        success.pack(pady=10)

    def show_main_interface(self):
        """Display main typing test interface"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Welcome message
        welcome = ctk.CTkLabel(self.main_frame, 
                             text=f"Welcome, {self.current_user}!", 
                             font=("Arial", 20))
        welcome.pack(pady=10)
        
        # Text display area
        self.text_display = ctk.CTkTextbox(self.main_frame, height=100, 
                                          font=("Arial", 14))
        self.text_display.pack(pady=10, padx=10, fill="x")
        self.text_display.insert("1.0", "Click 'Start Test' to begin...")
        self.text_display.configure(state="disabled")
        
        # Input area
        self.input_area = ctk.CTkTextbox(self.main_frame, height=100, 
                                        font=("Arial", 14))
        self.input_area.pack(pady=10, padx=10, fill="x")
        self.input_area.configure(state="disabled")
        
        # Stats frame
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.pack(pady=10, fill="x")
        
        self.wpm_label = ctk.CTkLabel(stats_frame, text="WPM: 0")
        self.wpm_label.pack(side="left", padx=10)
        
        self.accuracy_label = ctk.CTkLabel(stats_frame, text="Accuracy: 0%")
        self.accuracy_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(stats_frame, text="Time: 0s")
        self.time_label.pack(side="left", padx=10)
        
        # Control buttons
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=10)
        
        start_btn = ctk.CTkButton(button_frame, text="Start Test", 
                                 command=self.start_test)
        start_btn.pack(side="left", padx=5)
        
        history_btn = ctk.CTkButton(button_frame, text="View History", 
                                   command=self.show_history)
        history_btn.pack(side="left", padx=5)
        
        logout_btn = ctk.CTkButton(button_frame, text="Logout", 
                                  command=self.logout)
        logout_btn.pack(side="left", padx=5)

    def start_test(self):
        """Start a new typing test"""
        sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Programming is the art of telling another human what one wants the computer to do.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        ]
        
        self.test_started = True
        self.start_time = time.time()
        self.words_typed = 0
        self.correct_words = 0
        
        # Reset and enable input area
        self.input_area.configure(state="normal")
        self.input_area.delete("1.0", "end")
        
        # Set new test text
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")
        self.current_text = random.choice(sample_texts)
        self.text_display.insert("1.0", self.current_text)
        self.text_display.configure(state="disabled")
        
        # Start timer update
        self.update_timer()

    def update_timer(self):
        """Update the timer and stats during the test"""
        if self.test_started:
            elapsed = int(time.time() - self.start_time)
            self.time_label.configure(text=f"Time: {elapsed}s")
            
            # Calculate WPM
            if elapsed > 0:
                words = len(self.input_area.get("1.0", "end-1c").split())
                wpm = (words / elapsed) * 60
                self.wpm_label.configure(text=f"WPM: {int(wpm)}")
            
            self.root.after(1000, self.update_timer)

    def show_history(self):
        """Display user's typing test history"""
        history_window = ctk.CTkToplevel(self.root)
        history_window.title("Test History")
        history_window.geometry("400x300")
        
        conn = sqlite3.connect('typespeed.db')
        c = conn.cursor()
        c.execute("""SELECT wpm, accuracy, timestamp 
                    FROM scores 
                    WHERE username=? 
                    ORDER BY timestamp DESC""", 
                 (self.current_user,))
        scores = c.fetchall()
        conn.close()
        
        if scores:
            for wpm, accuracy, timestamp in scores:
                score_frame = ctk.CTkFrame(history_window)
                score_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(score_frame, 
                            text=f"WPM: {int(wpm)} | Accuracy: {int(accuracy)}% | {timestamp}").pack()
        else:
            ctk.CTkLabel(history_window, text="No history available").pack(pady=20)

    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.main_frame.destroy()
        self.show_login_frame()

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TypeSpeedTester()
    app.run()
