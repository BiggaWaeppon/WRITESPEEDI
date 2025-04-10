"""
CONSOLE-APP_CONSOLE-APP
Ein einfacher Texteingabetester für die Konsole

GUI-Modus mit allen Funktionen
"""

import time
import os
import json
from datetime import datetime
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import subprocess

# Testtext Optionen
test_texts = {
    'de': "Der schnelle braune Fuchs springt über den faulen Hund"
}

class TypingSpeedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Tester")
        self.root.geometry("800x600")
        
        # Hauptframe
        self.main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Obere Menüleiste
        self.menu_frame = tk.Frame(self.main_frame, bg="#e0e0e0")
        self.menu_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Start-Button
        self.start_button = tk.Button(self.menu_frame, 
                                    text="Test starten",
                                    command=self.start_test,
                                    width=20, height=2,
                                    bg="#4CAF50",
                                    fg="white",
                                    font=("Arial", 12, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Statistik-Button
        self.stats_button = tk.Button(self.menu_frame,
                                    text="Statistiken",
                                    command=self.show_statistics,
                                    width=20, height=2,
                                    bg="#2196F3",
                                    fg="white",
                                    font=("Arial", 12, "bold"))
        self.stats_button.pack(side=tk.LEFT, padx=10)
        
        # Testbereich
        self.test_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.test_frame.pack(fill=tk.BOTH, expand=True)
        
        # Testtext
        self.text_label = tk.Label(self.test_frame, 
                                 text="",
                                 font=("Arial", 16),
                                 wraplength=700,
                                 justify=tk.LEFT,
                                 bg="#f0f0f0")
        self.text_label.pack(pady=20)
        
        # Eingabefeld
        self.input_frame = tk.Frame(self.test_frame, bg="#f0f0f0")
        self.input_frame.pack(fill=tk.X)
        
        self.input_entry = tk.Entry(self.input_frame,
                                  font=("Arial", 14),
                                  width=50)
        self.input_entry.pack(fill=tk.X, expand=True, padx=10)
        
        # Ergebnisse
        self.results_frame = tk.Frame(self.test_frame, bg="#f0f0f0")
        self.results_frame.pack(fill=tk.X, pady=20)
        
        self.wpm_label = tk.Label(self.results_frame, 
                                 text="WPM: 0",
                                 font=("Arial", 14),
                                 bg="#f0f0f0")
        self.wpm_label.pack(side=tk.LEFT, padx=10)
        
        self.accuracy_label = tk.Label(self.results_frame, 
                                     text="Genauigkeit: 0%",
                                     font=("Arial", 14),
                                     bg="#f0f0f0")
        self.accuracy_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(self.results_frame, 
                                 text="Zeit: 0 Sekunden",
                                 font=("Arial", 14),
                                 bg="#f0f0f0")
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        # Statistik-Frame
        self.stats_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        
        # Zurück-Button
        self.back_button = tk.Button(self.stats_frame,
                                   text="Zurück",
                                   command=self.show_test,
                                   width=15, height=1,
                                   bg="#f44336",
                                   fg="white",
                                   font=("Arial", 12, "bold"))
        
        # Reset-Button
        self.reset_button = tk.Button(self.stats_frame,
                                    text="Statistiken zurücksetzen",
                                    command=self.show_reset_password,
                                    width=25, height=1,
                                    bg="#f44336",
                                    fg="white",
                                    font=("Arial", 12, "bold"))
        
        # Tabelle für Statistiken
        self.stats_table = ttk.Treeview(self.stats_frame,
                                      columns=("Datum", "WPM", "Genauigkeit"),
                                      show="headings")
        
        self.stats_table.heading("Datum", text="Datum")
        self.stats_table.heading("WPM", text="WPM")
        self.stats_table.heading("Genauigkeit", text="Genauigkeit")
        
        self.stats_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.current_test = None
        self.start_time = None
        self.results = []
        
        # Lade gespeicherte Ergebnisse
        self.load_results()
        
    def load_results(self):
        """Lädt gespeicherte Testergebnisse"""
        try:
            with open("results.json", "r") as f:
                self.results = json.load(f)
            self.update_stats_table()
        except FileNotFoundError:
            self.results = []
        except json.JSONDecodeError:
            self.results = []
            self.save_results()
    
    def save_results(self):
        """Speichert Testergebnisse"""
        with open("results.json", "w") as f:
            json.dump(self.results, f)
    
    def update_stats_table(self):
        """Aktualisiert die Statistik-Tabelle"""
        for item in self.stats_table.get_children():
            self.stats_table.delete(item)
            
        for result in self.results:
            self.stats_table.insert("", "end", values=(
                result["date"],
                result["wpm"],
                f"{result["accuracy"]}%"
            ))
    
    def start_test(self):
        """Startet einen neuen Test"""
        if self.current_test:
            return
            
        # Testtext auswählen
        test_text = test_texts["de"]
        
        # Testbereich aktualisieren
        self.text_label.config(text=test_text)
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()
        
        # Timer starten
        self.start_time = time.time()
        self.current_test = test_text
        
        # Eingabefeld aktualisieren
        self.input_entry.config(state=tk.NORMAL)
        
        # Ergebnisse zurücksetzen
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Genauigkeit: 0%")
        self.time_label.config(text="Zeit: 0 Sekunden")
    
    def calculate_results(self, typed_text):
        """Berechnet die Testergebnisse"""
        if not self.current_test:
            return None
            
        # Zeit berechnen
        end_time = time.time()
        time_elapsed = end_time - self.start_time
        
        # WPM berechnen
        words = typed_text.split()
        wpm = len(words) / (time_elapsed / 60)
        
        # Genauigkeit berechnen
        correct_chars = sum(1 for a, b in zip(typed_text, self.current_test) if a == b)
        accuracy = (correct_chars / len(self.current_test)) * 100
        
        return {
            "wpm": round(wpm, 1),
            "accuracy": round(accuracy, 1),
            "time": round(time_elapsed, 1)
        }
    
    def save_result(self, result):
        """Speichert ein Testergebnis"""
        self.results.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "wpm": result["wpm"],
            "accuracy": result["accuracy"]
        })
        self.save_results()
        self.update_stats_table()
    
    def update_input(self, event):
        """Aktualisiert die Eingabe und berechnet die Ergebnisse"""
        if not self.current_test:
            return
            
        typed_text = self.input_entry.get()
        
        # Berechne vorläufige Ergebnisse
        results = self.calculate_results(typed_text)
        if results:
            self.wpm_label.config(text=f"WPM: {results['wpm']}")
            self.accuracy_label.config(text=f"Genauigkeit: {results['accuracy']}%")
            self.time_label.config(text=f"Zeit: {results['time']} Sekunden")
            
        # Wenn der Text abgeschlossen ist
        if typed_text == self.current_test:
            self.end_test(results)
    
    def end_test(self, results):
        """Beendet den Test und speichert die Ergebnisse"""
        if results:
            self.save_result(results)
            messagebox.showinfo("Test abgeschlossen",
                              f"WPM: {results['wpm']}\n"
                              f"Genauigkeit: {results['accuracy']}%\n"
                              f"Zeit: {results['time']} Sekunden")
        
        self.current_test = None
        self.start_time = None
        self.input_entry.config(state=tk.DISABLED)
    
    def show_reset_password(self):
        """Zeigt das Passwortfenster für das Zurücksetzen der Statistiken"""
        password_window = tk.Toplevel(self.root)
        password_window.title("Admin-Login")
        password_window.geometry("300x150")
        
        # Passwort-Eingabefeld
        password_label = tk.Label(password_window, 
                                text="Admin-Passwort:",
                                font=("Arial", 12))
        password_label.pack(pady=10)
        
        password_entry = tk.Entry(password_window,
                                show="*",
                                font=("Arial", 12))
        password_entry.pack(pady=10)
        
        # Login-Button
        login_button = tk.Button(password_window,
                               text="Bestätigen",
                               command=lambda: self.reset_stats(password_entry.get(), password_window),
                               width=15, height=1,
                               bg="#4CAF50",
                               fg="white",
                               font=("Arial", 12, "bold"))
        login_button.pack(pady=10)
        
        password_entry.focus()
        
    def reset_stats(self, password, window):
        """Zurücksetzen der Statistiken nach erfolgreicher Authentifizierung"""
        if password == "admin123":
            self.results = []
            self.save_results()
            self.update_stats_table()
            messagebox.showinfo("Erfolgreich", "Statistiken wurden zurückgesetzt")
            window.destroy()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort!")
            window.destroy()
    
    def show_statistics(self):
        """Zeigt die Statistik-Tabelle an"""
        # Zeige Statistik-Frame
        self.stats_frame.pack(fill=tk.BOTH, expand=True)
        self.test_frame.pack_forget()
        
        # Zeige Zurück-Button
        self.back_button.pack(pady=10)
        
        # Zeige Reset-Button
        self.reset_button.pack(pady=10)
        
        # Zeige Tabelle
        self.stats_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def show_test(self):
        """Zeigt den Test-Bereich an"""
        self.test_frame.pack(fill=tk.BOTH, expand=True)
        self.stats_frame.pack_forget()
        
        # Verstecke Zurück-Button
        self.back_button.pack_forget()
        
        # Verstecke Reset-Button
        self.reset_button.pack_forget()
    
    def run(self):
        """Startet die GUI-Application"""
        # Eingabefeld-Events binden
        self.input_entry.bind("<KeyRelease>", self.update_input)
        
        # Starten der GUI
        self.root.mainloop()

def main():
    """Hauptfunktion des Programms"""
    # Starte direkt mit der GUI
    app = TypingSpeedGUI()
    app.run()

if __name__ == "__main__":
    main()
