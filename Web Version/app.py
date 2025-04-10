# Importiere notwendige Flask-Module und -Abhängigkeiten
# Flask ist unser Webframework für die Erstellung der Anwendung
# SQLAlchemy ist unser ORM für Datenbankinteraktionen
# Flask-Login verwaltet Benutzerauthentifizierung und -Sitzungen
# bcrypt wird für sichere Passwort-Hashing verwendet
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
import random
from datetime import datetime
import requests

# Initialisiere die Flask-Anwendung
app = Flask(__name__)

# Konfiguriere die Anwendungseinstellungen
# SECRET_KEY wird für Sitzungsverschlüsselung verwendet
# SQLALCHEMY_DATABASE_URI gibt die Speicherort unserer SQLite-Datenbank an
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typespeed.db'

db = SQLAlchemy(app)  # Initialisiere die SQLAlchemy-Datenbankverbindung
login_manager = LoginManager()  # Initialisiere Flask-Login für Benutzerauthentifizierung
login_manager.init_app(app)  # Verbinde LoginManager mit unserer Flask-App
login_manager.login_view = 'login'  # Setze die Login-Ansicht für nicht autorisierten Zugriff

# Datenbankmodell für Benutzer
# Diese Klasse definiert die Struktur der Benutzer in der Datenbank
# Jeder Benutzer hat:
# - Eine eindeutige ID
# - Einen Benutzernamen (muss einzigartig sein)
# - Ein gehashtes Passwort (nie im Klartext gespeichert)
# - Einen Admin-Status (Standard: False)
# - Eine Beziehung zu den Scores des Benutzers
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jeden Benutzer
    username = db.Column(db.String(80), unique=True, nullable=False)  # Benutzername muss einzigartig sein
    password = db.Column(db.String(120), nullable=False)  # Passwort wird gehasht gespeichert
    is_admin = db.Column(db.Boolean, default=False)  # Admin-Status (Standard: False)
    scores = db.relationship('Score', backref='user', lazy=True)  # Verknüpfung zu den Scores des Benutzers

# Datenbankmodell für Scores
# Diese Klasse speichert die Ergebnisse der Tipptest
# Jeder Score enthält:
# - Eine eindeutige ID
# - Die WPM (Words per Minute) als Geschwindigkeitsmessung
# - Die Genauigkeit als Prozentsatz
# - Ein Zeitstempel, wann der Score erzielt wurde
# - Eine Verknüpfung zum Benutzer, der den Score erzielt hat
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jeden Score
    wpm = db.Column(db.Float, nullable=False)  # Geschwindigkeit in Wörtern pro Minute
    accuracy = db.Column(db.Float, nullable=False)  # Genauigkeit in Prozent
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Zeitpunkt der Erzielung
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Verknüpfung zum Benutzer

# Funktion zum Laden eines Benutzers aus der Datenbank
# Diese Funktion wird von Flask-Login verwendet
# Sie nimmt eine Benutzer-ID und gibt das entsprechende Benutzerobjekt zurück
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Funktion zum Abrufen des Tipptextes
# Diese Funktion gibt den vorgegebenen Text zurück, den Benutzer während des Tipptests eingeben müssen
# Der Text ist absichtlich herausfordernd gestaltet, enthält aber auch verständliche Wörter und technische Begriffe
def get_typing_text():
    return """Die Zukunft der Technologie liegt in künstlicher Intelligenz und maschinellem Lernen. 
    Als Computer leistungsfähiger werden, können sie riesige Datenmengen verarbeiten und komplexe Probleme lösen. 
    Wissenschaftler und Ingenieure arbeiten zusammen, um intelligente Systeme zu schaffen, die menschliche Sprache verstehen, 
    Muster erkennen und Entscheidungen treffen können. Diese Fortschritte verändern die Art, wie wir leben und arbeiten, 
    und machen unsere täglichen Aufgaben einfacher und effizienter."""

# Funktion zur Überprüfung der Admin-Rechte
# Diese Hilfsfunktion überprüft, ob der aktuell eingeloggte Benutzer Administratorrechte hat
# Sie prüft zwei Bedingungen:
# 1. Der Benutzer muss eingeloggt sein
# 2. Der Benutzer muss den Admin-Flag gesetzt haben
# Diese Funktion wird im gesamten System verwendet, um Admin-funktionen zu schützen
def is_admin():
    return current_user.is_authenticated and current_user.is_admin

# Routenhandler - Diese sind die Hauptendpunkte der Anwendung

# Startseite
# Dies ist der Hauptzugangspunkt der Anwendung
# Wenn Benutzer die Startseite ('/') besuchen, wird ihnen die index.html-Vorlage angezeigt
# Diese Vorlage enthält in der Regel das Login-Formular und die Registrierungsoptionen
@app.route('/')
def index():
    return render_template('index.html')

# Registrierungsendpunkt
# Dieser Endpunkt verarbeitet neue Benutzerregistrierungen
# Er akzeptiert POST-Anfragen mit JSON-Daten, die enthalten:
# - username: Der gewünschte Benutzername für das neue Konto
# - password: Das Passwort für das neue Konto
@app.route('/register', methods=['POST'])
def register():
    # Extrahiere Daten aus der eingehenden JSON-Anfrage
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Prüfe, ob der Benutzername bereits vergeben ist
    # Dies verhindert doppelte Konten und gewährleistet die Datenintegrität
    if User.query.filter_by(username=username).first():
        # Wenn Benutzername existiert, gib einen Fehler zurück mit Statuscode 400 (Bad Request)
        return jsonify({'error': 'Benutzername bereits vergeben'}), 400
    
    # Erstelle ein neues Benutzerkonto
    # 1. Hash das Passwort für die Sicherheit mit bcrypt
    #    - Stellt sicher, dass Passwörter niemals im Klartext gespeichert werden
    #    - Machen es extrem schwierig, das Passwort zu entschlüsseln
    # 2. Erstelle ein neues User-Objekt mit dem angegebenen Benutzernamen und gehashten Passwort
    # 3. Füge den neuen Benutzer zur Datenbank-Sitzung hinzu
    # 4. Speichere die Änderungen dauerhaft
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User(username=username, password=hashed)
    db.session.add(new_user)
    db.session.commit()
    
    # Gib eine Erfolgsmeldung an den Client zurück
    # Dies zeigt, dass die Registrierung erfolgreich war
    return jsonify({'message': 'Registrierung erfolgreich'})

# Benutzerauthentifizierungsendpunkt
# Dieser Endpunkt verarbeitet Benutzerauthentifizierungsanfragen
# Er akzeptiert POST-Anfragen mit JSON-Daten, die enthalten:
# - username: Der Benutzername des Kontos, auf das zugegriffen werden soll
# - password: Das Passwort für das Konto
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    
    # Überprüfe die Anmeldedaten und melde den Benutzer an
    if user and bcrypt.checkpw(data.get('password').encode(), user.password):
        login_user(user)
        return jsonify({'message': 'Anmeldung erfolgreich'})
    
    return jsonify({'error': 'Falsche Anmeldedaten'}), 401

# Admin-Authentifizierungsendpunkt
# Dieser Endpunkt verarbeitet Admin-Authentifizierungsanfragen
# Er akzeptiert POST-Anfragen mit JSON-Daten, die enthalten:
# - username: Der Benutzername des Admin-Kontos, auf das zugegriffen werden soll
# - password: Das Passwort für das Admin-Konto
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    # Überprüfe die Admin-Anmeldedaten
    if user and bcrypt.checkpw(password.encode(), user.password) and user.is_admin:
        login_user(user)
        return jsonify({'message': 'Admin-Anmeldung erfolgreich'})
    
    return jsonify({'error': 'Falsche Admin-Anmeldedaten'}), 401

# Benutzerabmelden-Endpunkt
# Dieser Endpunkt meldet den aktuellen Benutzer ab
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Abgemeldet'})

# Admin-Endpunkt zum Zurücksetzen aller Scores
# Dieser Endpunkt löscht alle Scores aus der Datenbank
# Er erfordert Admin-Authentifizierung
@app.route('/admin/reset/scores', methods=['POST'])
@login_required
def admin_reset_scores():
    if not is_admin():
        return jsonify({'error': 'Nicht autorisiert'}), 403
    
    try:
        # Lösche alle Scores aus der Datenbank
        Score.query.delete()
        db.session.commit()
        return jsonify({'message': 'Alle Scores wurden gelöscht'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admin-Endpunkt zum Zurücksetzen aller Benutzer
# Dieser Endpunkt löscht alle nicht-Admin-Benutzer aus der Datenbank
# Er erfordert Admin-Authentifizierung
@app.route('/admin/reset/users', methods=['POST'])
@login_required
def admin_reset_users():
    if not is_admin():
        return jsonify({'error': 'Nicht autorisiert'}), 403
    
    try:
        # Lösche alle nicht-Admin-Benutzer
        User.query.filter_by(is_admin=False).delete()
        db.session.commit()
        return jsonify({'message': 'Alle Benutzer wurden gelöscht'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admin-Endpunkt zum Zurücksetzen aller Daten
# Dieser Endpunkt löscht alle Scores und nicht-Admin-Benutzer aus der Datenbank
# Er erfordert Admin-Authentifizierung
@app.route('/admin/reset', methods=['POST'])
@login_required
def admin_reset():
    if not is_admin():
        return jsonify({'error': 'Nicht autorisiert'}), 403
    
    try:
        # Lösche alle Scores und nicht-Admin-Benutzer
        Score.query.delete()
        User.query.filter_by(is_admin=False).delete()
        db.session.commit()
        return jsonify({'message': 'Alle Scores und Benutzer wurden gelöscht'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admin-Status-Endpunkt zum Abrufen von Systemstatistiken
# Dieser Endpunkt gibt die Anzahl der Benutzer und Scores in der Datenbank zurück
# Er erfordert Admin-Authentifizierung
@app.route('/admin/status')
@login_required
def admin_status():
    if not is_admin():
        return jsonify({'error': 'Nicht autorisiert'}), 403
    
    # Hole die Anzahl der Benutzer und Scores
    user_count = User.query.filter_by(is_admin=False).count()
    score_count = Score.query.count()
    
    return jsonify({
        'Benutzer': user_count,
        'Scores': score_count
    })

# Endpunkt zum Abrufen des Tipptextes
# Dieser Endpunkt gibt den vorgegebenen Tipptext zurück
@app.route('/get_text')
def get_text():
    return jsonify({
        'text': get_typing_text()
    })

# Endpunkt zum Speichern eines Benutzerscores
# Dieser Endpunkt erstellt einen neuen Score-Eintrag in der Datenbank
# Er erfordert Benutzerauthentifizierung
@app.route('/save_score', methods=['POST'])
@login_required
def save_score():
    data = request.json
    try:
        # Erstelle und speichere einen neuen Score
        new_score = Score(
            wpm=float(data.get('wpm')),
            accuracy=float(data.get('accuracy')),
            user_id=current_user.id
        )
        db.session.add(new_score)
        db.session.commit()
        return jsonify({'message': 'Score gespeichert'})
    except Exception as e:
        print(f"Fehler beim Speichern des Scores: {str(e)}")  # Debug-Logging
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ranglisten-Endpunkt zum Abrufen der besten Benutzer
# Dieser Endpunkt gibt eine Liste der besten Benutzer basierend auf ihrer Tippsgeschwindigkeit zurück
@app.route('/leaderboard')
def leaderboard():
    # Hole Benutzerstatistiken einschließlich Gesamtspielen, Durchschnittsgeschwindigkeit und Bestgeschwindigkeit
    stats = db.session.query(
        User.username,
        db.func.count(Score.id).label('total_games'),
        db.func.avg(Score.wpm).label('avg_wpm'),
        db.func.max(Score.wpm).label('max_wpm'),
        db.func.avg(Score.accuracy).label('avg_accuracy')
    ).join(Score).group_by(User.id).order_by(db.desc('max_wpm')).all()
    
    return jsonify([{
        'Benutzername': stat.username,
        'Gesamtspiele': int(stat.total_games),
        'Durchschnittsgeschwindigkeit': round(float(stat.avg_wpm), 1),
        'Bestgeschwindigkeit': round(float(stat.max_wpm), 1),
        'Durchschnittliche Genauigkeit': round(float(stat.avg_accuracy), 1)
    } for stat in stats])

# Benutzerhistorien-Endpunkt zum Abrufen der persönlichen Score-Historie
# Dieser Endpunkt gibt eine Liste der Scores für den aktuellen Benutzer zurück
# Er erfordert Benutzerauthentifizierung
@app.route('/user_history')
@login_required
def user_history():
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.timestamp.desc()).all()
    return jsonify([{
        'wpm': score.wpm,
        'accuracy': score.accuracy,
        'timestamp': score.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for score in scores])

# Anwendungsstartcode
if __name__ == '__main__':
    with app.app_context():
        # Initialisiere die Datenbank
        # Lösche alle bestehenden Tabellen und erstelle sie neu
        db.drop_all()
        db.create_all()
        
        # Erstelle einen Standard-Admin-Benutzer
        # Dieser Benutzer hat den Benutzernamen 'admin' und das Passwort 'admin123'
        hashed = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt())
        admin = User(username='admin', password=hashed, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        
    # Starte den Flask-Entwicklungs-Server
    app.run(debug=True)
