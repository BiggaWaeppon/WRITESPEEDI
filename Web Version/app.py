from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from models import db, User, Score
from utils import hash_password, verify_password, generate_typing_text, calculate_typing_speed, calculate_accuracy

login_manager = LoginManager()

def get_typing_text():
    return generate_typing_text()

def is_admin():
    return current_user.is_authenticated and current_user.is_admin

def create_app(config='production'):
    app = Flask(__name__)
    
    if config == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    else:
        app.config['SECRET_KEY'] = 'your-secret-key-here'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typespeed.db'
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        hashed = hash_password(password)
        new_user = User(username=username, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'Registration successful'})

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and verify_password(user.password, data.get('password')):
            login_user(user)
            return jsonify({'message': 'Login successful'})
        
        return jsonify({'error': 'Invalid credentials'}), 401

    @app.route('/admin/login', methods=['POST'])
    def admin_login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and verify_password(user.password, password) and user.is_admin:
            login_user(user)
            return jsonify({'message': 'Admin login successful'})
        
        return jsonify({'error': 'Invalid admin credentials'}), 401

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out'})

    @app.route('/admin/reset/scores', methods=['POST'])
    @login_required
    def admin_reset_scores():
        if not is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        try:
            # Delete all scores
            Score.query.delete()
            db.session.commit()
            return jsonify({'message': 'All scores have been deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/admin/reset/users', methods=['POST'])
    @login_required
    def admin_reset_users():
        if not is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        try:
            # Delete all non-admin users
            User.query.filter_by(is_admin=False).delete()
            db.session.commit()
            return jsonify({'message': 'All users have been deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/admin/reset', methods=['POST'])
    @login_required
    def admin_reset():
        if not is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        try:
            # Delete all scores and non-admin users
            Score.query.delete()
            User.query.filter_by(is_admin=False).delete()
            db.session.commit()
            return jsonify({'message': 'All scores and non-admin users have been deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/admin/status')
    @login_required
    def admin_status():
        if not is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        user_count = User.query.filter_by(is_admin=False).count()
        score_count = Score.query.count()
        
        return jsonify({
            'users': user_count,
            'scores': score_count
        })

    @app.route('/get_text')
    def get_text():
        return jsonify({
            'text': get_typing_text()
        })

    @app.route('/save_score', methods=['POST'])
    @login_required
    def save_score():
        data = request.json
        try:
            wpm = calculate_typing_speed(data.get('wordsTyped'), data.get('timeElapsed'))
            accuracy = calculate_accuracy(data.get('correctChars'), data.get('totalChars'))
            
            new_score = Score(
                wpm=wpm,
                accuracy=accuracy,
                user_id=current_user.id
            )
            db.session.add(new_score)
            db.session.commit()
            return jsonify({'message': 'Score saved'})
        except Exception as e:
            print(f"Error saving score: {str(e)}")  # Add debug logging
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/leaderboard')
    def leaderboard():
        # Get user statistics including total games, average WPM, and best WPM
        stats = db.session.query(
            User.username,
            db.func.count(Score.id).label('total_games'),
            db.func.avg(Score.wpm).label('avg_wpm'),
            db.func.max(Score.wpm).label('max_wpm'),
            db.func.avg(Score.accuracy).label('avg_accuracy')
        ).join(Score).group_by(User.id).order_by(db.desc('max_wpm')).all()
        
        return jsonify([{
            'username': stat.username,
            'totalGames': int(stat.total_games),
            'averageWPM': round(float(stat.avg_wpm), 1),
            'bestWPM': round(float(stat.max_wpm), 1),
            'averageAccuracy': round(float(stat.avg_accuracy), 1)
        } for stat in stats])

    @app.route('/user_history')
    @login_required
    def user_history():
        scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.timestamp.desc()).all()
        return jsonify([{
            'wpm': score.wpm,
            'accuracy': score.accuracy,
            'timestamp': score.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for score in scores])
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create admin user
        hashed = hash_password('admin123')
        admin = User(username='admin', password=hashed, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        
    app.run(debug=True)