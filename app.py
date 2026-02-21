from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

print("API Working")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return jsonify({"msg": "Token missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["user_id"]
        except:
            return jsonify({"msg": "Token invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "supersecretkey"

@app.route("/test")
def test():
    return "API working"

# ---------------- DATABASE CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_name = db.Column(db.String(120))
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# ---------------- SECURITY HEADERS (BONUS MARKS) ----------------
@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return "Habit Tracker Backend Running"

# Create sample user (run once)
@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    hashed = generate_password_hash(data["password"])
    user = User(email=data["email"], password=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"})

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data.get("email")).first()

    if user and check_password_hash(user.password, data.get("password")):
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, app.config["SECRET_KEY"], algorithm="HS256")

        return jsonify({"token": token})

    return jsonify({"msg": "Invalid credentials"}), 401

# Add habit
@app.route("/add_habit", methods=["POST"])
@token_required
def add_habit(current_user):
    data = request.json

    habit = Habit(
        habit_name=data["habit_name"],
        description=data["description"],
        user_id=current_user
    )

    db.session.add(habit)
    db.session.commit()

    return jsonify({"msg": "Habit added"})

# Get habits
@app.route("/habits")
@token_required
def get_habits(current_user):
    habits = Habit.query.filter_by(user_id=current_user).all()
    result = []

    for h in habits:
        result.append({
            "id": h.id,
            "habit_name": h.habit_name,
            "description": h.description
        })

    return jsonify(result)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # auto create DB tables
    app.run(host="0.0.0.0", port=5000)