"""
CONSOLE-APP_CONSOLE-APP
Ein einfacher Texteingabetester für die Konsole
"""

import time
# time: Python Standardbibliothek für Zeitmessungen
# time.time() gibt die aktuelle Zeit in Sekunden seit dem Unix Epoch
# Grund für die Wahl: Einfache und präzise Zeitmessung für die Testdauer
# Vorteile: Keine zusätzlichen Abhängigkeiten, sehr präzise Messung

import os
# os: Python Standardbibliothek für Betriebssystem-Operationen
# os.path.join() erstellt korrekte Dateipfade für das jeweilige Betriebssystem
# Grund für die Wahl: Plattformunabhängige Dateipfad-Verwaltung
# Vorteile: Funktioniert auf allen Betriebssystemen (Windows, Linux, Mac)
#            Vermeidet Fehler durch manuelle Pfad-Verkettung

from datetime import datetime
# datetime: Python Standardbibliothek für Datum- und Zeitoperationen
# datetime.now() gibt das aktuelle Datum und die aktuelle Zeit
# Grund für die Wahl: Einfache Datums- und Zeitformatierung
# Vorteile: Standardisierte Zeitformatierung für die Testergebnisse
#            Einfache Speicherung der Testzeitpunkte

# Testtext Optionen
# Dictionary (Wörterbuch) mit Sprachoptionen
# Schlüssel: 'en' für Englisch, 'de' für Deutsch
# Wert: Der entsprechende Testtext
# Grund für die Wahl: Einfache und flexible Sprachverwaltung
# Vorteile: Leicht erweiterbar für weitere Sprachen
#            Effiziente Zugriff auf Texte durch Schlüssel
#            Einfache Wartung der Texte

test_texts = {
    'en': "The quick brown fox jumps over the lazy dog",
    'de': "Der schnelle braune Fuchs springt über den faulen Hund"
}

def show_menu():
    """
    Zeigt das Hauptmenü an mit den folgenden Optionen:
    1. Test starten
    2. Ergebnisse anzeigen
    3. Programm beenden
    """
    print("\nTEXT-EINGABETESTER")
    print("1. Test starten")
    print("2. Ergebnisse anzeigen")
    print("3. Beenden")

def start_test():
    """
    Startet einen neuen Texteingabetest:
    1. Zeigt einen Testtext an
    2. Startet einen Timer
    3. Erwartet die Eingabe des Benutzers
    4. Berechnet die Geschwindigkeit (WPM) und Genauigkeit
    5. Speichert die Ergebnisse
    """
    print("\nTest wird gestartet...")
    
    # Sprachauswahl
    # print(): Python-Builtin-Funktion zum Anzeigen von Text
    # input(): Python-Builtin-Funktion zum Einlesen von Benutzereingaben
    # Grund für die Wahl: Einfache Benutzerschnittstelle
    # Vorteile: Keine zusätzlichen Abhängigkeiten
    #            Einfache Textausgabe und Eingabe
    print("\nWählen Sie die Sprache:")
    print("1. Deutsch")
    print("2. Englisch")
    lang_choice = input("\nWählen Sie eine Sprache (1-2): ")
    
    # Sprache festlegen
    # if/else: Bedingte Anweisung in Python
    # ==: Vergleichsoperator für Gleichheit
    # 'de'/'en': String-Literale
    # Grund für die Wahl: Einfache Sprachauswahl
    # Vorteile: Direkter Zugriff auf die Sprachtexte
    #            Einfache Auswertung der Benutzereingabe
    lang = 'de' if lang_choice == '1' else 'en'
    
    # Testtext für die gewählte Sprache
    # []: Dictionary-Zugriff-Operator
    # f-String: Formatierter String mit Variablen-Interpolation
    # Grund für die Wahl: Einfache Textausgabe
    # Vorteile: Direkter Zugriff auf den Text
    #            Einfache Variable-Integration
    test_text = test_texts[lang]
    print(f"\nGeben Sie diesen Text ein: {test_text}")
    
    # Timer starten
    # input(): Wartet auf Enter-Taste
    # time.time(): Gibt die aktuelle Zeit in Sekunden
    # Grund für die Wahl: Einfache Zeitmessung
    # Vorteile: Präzise Zeitmessung
    #            Einfache Bedienung für den Benutzer
    input("\nDrücken Sie Enter, um zu beginnen...")
    start_time = time.time()
    
    # Benutzereingabe erfassen
    # input(): Liest die Eingabe des Benutzers
    # time.time(): Gibt die aktuelle Zeit in Sekunden
    # Grund für die Wahl: Einfache Texteingabe
    # Vorteile: Direkte Eingabe von Text
    #            Einfache Zeitmessung des Eingabeprozesses
    user_input = input("\nHier eingeben: ")
    end_time = time.time()
    
    # Zeit berechnen
    # - Operator: Subtraktion
    # end_time - start_time: Berechnet die verstrichene Zeit in Sekunden
    # Grund für die Wahl: Einfache Zeitberechnung
    # Vorteile: Direkte Zeitdifferenzberechnung
    #            Einfache Implementierung
    time_taken = end_time - start_time
    print(f"\nVerlaufene Zeit: {time_taken:.2f} Sekunden")
    
    # Wörter pro Minute berechnen
    # len(): Python-Builtin-Funktion zur Länge einer Liste
    # split(): String-Methode zum Aufteilen in Wörter
    # / Operator: Division
    # * Operator: Multiplikation
    # Grund für die Wahl: Einfache WPM-Berechnung
    # Vorteile: Direkte Wörterzählung
    #            Einfache Umrechnung in Minuten
    #            Präzise Ergebnisse
    words = len(user_input.split())
    wpm = (words / time_taken) * 60
    print(f"\nWörter: {words}")
    print(f"Berechnung: ({words} / {time_taken:.2f}) * 60 = {wpm:.2f} WPM")
    
    # Genauigkeit berechnen
    # zip(): Python-Builtin-Funktion zum Kombinieren von Listen
    # sum(): Python-Builtin-Funktion zur Summe berechnen
    # if: Bedingte Anweisung
    # Grund für die Wahl: Einfache Genauigkeitsberechnung
    # Vorteile: Direkter Vergleich von Wörtern
    #            Einfache Summierung der korrekten Wörter
    #            Präzise Genauigkeitsberechnung
    correct_words = sum(1 for a, b in zip(test_text.split(), user_input.split()) if a == b)
    accuracy = (correct_words / words) * 100 if words > 0 else 0
    print(f"\nKorrekte Wörter: {correct_words} von {words}")
    print(f"Berechnung: ({correct_words} / {words}) * 100 = {accuracy:.2f}%")
    
    # Ergebnisse speichern
    # os.path.join(): Erstellt korrekten Dateipfad
    # with open(): Öffnet eine Datei sicher
    # .write(): Schreibt Text in die Datei
    # Grund für die Wahl: Einfache Ergebnisspeicherung
    # Vorteile: Plattformunabhängige Dateioperationen
    #            Sichere Datei-Öffnung und -Schließung
    #            Einfache Textspeicherung
    results_file = os.path.join(os.path.dirname(__file__), 'CONSOLE-APP_results.txt')
    with open(results_file, 'a') as f:
        f.write(f"\nTest am {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Sprache: {'Deutsch' if lang == 'de' else 'Englisch'}\n")
        f.write(f"Wörter pro Minute: {wpm:.2f}\n")
        f.write(f"Genauigkeit: {accuracy:.2f}%\n")
        f.write("-" * 50)
    
    print("\nTest abgeschlossen!")
    print(f"Sprache: {'Deutsch' if lang == 'de' else 'Englisch'}")
    print(f"Wörter pro Minute: {wpm:.2f}")
    print(f"Genauigkeit: {accuracy:.2f}%")

def view_results():
    """
    Zeigt die vorherigen Testergebnisse an:
    1. Liest die Ergebnisse aus der Datei
    2. Zeigt sie in der Konsole an
    """
    print("\nVorherige Ergebnisse:")
    results_file = os.path.join(os.path.dirname(__file__), 'CONSOLE-APP_results.txt')
    try:
        with open(results_file, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Keine Ergebnisse verfügbar.")

def main():
    """
    Hauptprogrammschleife:
    1. Zeigt Willkommensnachricht
    2. Zeigt Hauptmenü
    3. Verarbeitet Benutzereingaben
    """
    print("Willkommen beim Texteingabetester!")
    
    while True:
        show_menu()
        choice = input("\nWählen Sie eine Option (1-3): ")
        
        if choice == '1':
            start_test()
        elif choice == '2':
            view_results()
        elif choice == '3':
            print("\nAuf Wiedersehen!")
            break
        else:
            print("\nUngültige Eingabe. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()
