# app.py
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


"""app.py - Main application logic for the Report Automation System."""

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/feedback', methods=['POST'])
def feedback():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    fb = Feedback(message=data['message'], user_id=session['user_id'])
    db.session.add(fb)
    db.session.commit()
    return jsonify({"message": "Feedback submitted"}), 200

@app.route('/admin/feedbacks', methods=['GET'])
def admin_feedbacks():
    user = User.query.get(session.get('user_id'))
    if not user or not user.is_admin:
        return jsonify({"error": "Forbidden"}), 403
    feedbacks = Feedback.query.all()
    return jsonify([{"id": f.id, "message": f.message} for f in feedbacks])

if __name__ == '__main__':
    app.run(debug=True)
