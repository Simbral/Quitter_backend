Quitter Backend
This is the **backend API server** for the Quitter Habit-Tracking application.  
It provides user authentication, habit storage, and protected routes with JWT token authentication.

🚀 Features
🔹 Authentication
- Create Users *(stores hashed passwords)*
- Login Users
- Returns **JWT tokens** for authenticated access

🔹 Protected API Endpoints
Routes like adding or fetching habits require a valid token.

🔹 Habit Management
- Add a habit for a user
- Get habits list for authenticated user

🔹 Security
- Uses secure password hashing
- JWT auth via `Authorization` header
- Security response headers added

🧠 Tech Stack
| Component | Used |
|-----------|------|
| Framework | Flask |
| DB | SQLite |
| ORM | SQLAlchemy |
| Auth | JWT |
| CORS | Flask-CORS |

🛠 Installation & Setup

1️⃣ Clone the repo
git clone https://github.com/Simbral/Quitter_backend.git
cd Quitter_backend

2️⃣ Install dependencies
pip install -r requirements.txt

▶️ Running the Server
python app.py
By default the server starts at: http://127.0.0.1:5000/

📌 API Endpoints
✔ Test
GET /test
Returns: "API working"

✔ Home
GET /
Returns: "Habit Tracker Backend Running"

✔ Create User
POST /create_user

✔ Create User
POST /create_user

Body (JSON):

{
  "email": "user@example.com",
  "password": "your-password"
}

✔ Login
POST /login

Body (JSON):
{
  "email": "user@example.com",
  "password": "your-password"
}

Response JSON:

{ "token": "<JWT_TOKEN>" }

✔ Add Habit
POST /add_habit
Headers:
Authorization: <JWT_TOKEN>

Body:
{
  "habit_name": "Coding",
  "description": "Practice coding daily"
}

✔ Get Habits
GET /habits

Headers:
Authorization: <JWT_TOKEN>
Returns:
[
  {
    "id": 1,
    "habit_name": "Coding",
    "description": "Practice coding daily"
  }
]

🔐 Token Security

All protected endpoints require:
Authorization: <JWT_TOKEN>
(obtained from login)
