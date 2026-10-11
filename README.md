<div align="center">

# 🧠 MindSync
### Digital Loneliness Predictor

*A machine learning–powered web application that assesses digital loneliness risk through adaptive psychological assessments.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)

</div>

---

## 📌 Project Overview

**MindSync** is a full-stack web application that predicts a user's digital loneliness risk level — **Low**, **Moderate**, or **High** — using a trained Random Forest classifier. Users complete a 20-question adaptive assessment drawn from a pool of 60 psychologically grounded questions across five behavioural categories. The system delivers instant predictions with confidence scores and personalised recommendations, while maintaining a full assessment history for longitudinal self-tracking.

---

## 🚨 Problem Statement

The rapid expansion of digital technology has paradoxically increased feelings of social isolation. Excessive screen time, passive social media consumption, and reduced face-to-face interaction contribute to a growing mental health concern known as **digital loneliness** — yet most individuals remain unaware of their own risk level.

There is a lack of accessible, data-driven tools that can:
- Quantify digital loneliness risk in a structured, repeatable way
- Provide personalised, actionable guidance based on individual behaviour patterns
- Track changes in risk over time to measure the impact of lifestyle adjustments

MindSync addresses this gap by combining behavioural psychology with machine learning to deliver a clinically-inspired self-assessment experience.

---

## 🎯 Objectives

- **Assess** digital loneliness risk through a validated 20-question behavioural survey
- **Predict** risk level (Low / Moderate / High) using a trained ML classifier
- **Personalise** recommendations based on the predicted risk category
- **Track** assessment history to enable longitudinal self-monitoring
- **Secure** user data with authentication, session management, and ownership checks
- **Scale** the question bank dynamically so each session presents a fresh, randomised subset

---

## 🛠️ Technologies Used

| Layer | Technology |
|---|---|
| **Backend Framework** | Flask 3.x (Python) |
| **Database** | MySQL 8.0 via PyMySQL |
| **ORM & Migrations** | SQLAlchemy + Flask-Migrate (Alembic) |
| **Authentication** | Flask-Login + Flask-Bcrypt |
| **Machine Learning** | scikit-learn (Random Forest Classifier) |
| **ML Data Handling** | NumPy, Pandas |
| **Frontend** | Bootstrap 5.3.7, Bootstrap Icons 1.11.3 |
| **Fonts** | Google Fonts — Poppins |
| **Session Management** | Flask server-side sessions |
| **Architecture** | MVC (Model-View-Controller) |

---

## 🤖 Machine Learning Algorithm

### Random Forest Classifier

MindSync uses a **Random Forest Classifier** (`n_estimators=100`, `random_state=42`) trained on a synthetically generated, balanced dataset of **1,000 records** (333 each for Low, Moderate, and High risk).

**Feature Engineering:**
- 20 Likert-scale responses (1–5) per assessment
- Score ranges map to risk categories: Low `[20–46]`, Moderate `[47–73]`, High `[74–100]`
- Stratified 80/20 train-test split ensures class balance in evaluation

**Performance:**
- Training Accuracy: **100%** on balanced dataset
- Model serialised to `ml/models/random_forest_model.pkl` via `joblib`
- Confidence score derived from `predict_proba()` for the predicted class

**Prediction Pipeline:**
```
User Answers (20 × int) → NumPy Array → model.predict() → Risk Label
                                       → model.predict_proba() → Confidence %
```

---

## 📦 Modules

### 1. 🔐 Authentication Module
Handles user registration, login, logout, and session management. Passwords are hashed with bcrypt. Login supports a `?next=` redirect parameter for seamless post-login navigation.

### 2. 📋 Assessment Module
Presents a 20-question adaptive survey drawn randomly from a pool of 60 questions. Tracks navigation state (Previous/Next) and answer persistence in the Flask session. Submits answers for scoring and ML prediction.

### 3. 🤖 Prediction Service
Loads the trained Random Forest model once at application startup. Accepts a list of 20 integer answers, returns the predicted risk label and confidence percentage. Integrated into the assessment submission flow.

### 4. 📊 Dashboard Module
Displays the user's latest assessment result (score, ML prediction, confidence, date) and total assessment count. Shows placeholder values for new users with no history.

### 5. 🗂️ Assessment History Module
Lists all past assessments in reverse chronological order with ML prediction and confidence columns. Each record links to a detail view with full stat cards and personalised recommendations. Ownership checks prevent cross-user data access.

### 6. 💡 Recommendations Engine
Delivers category-specific, actionable recommendations based on the predicted risk level (Low / Moderate / High). Recommendations are rendered on both the result page and each history detail page.

---

## 📁 Folder Structure

```
Digital-loneliness-predictor/
│
├── app/                            # Main application package
│   ├── controllers/                # Route handlers (MVC Controllers)
│   │   ├── auth_controller.py      # Register, login, logout, dashboard
│   │   ├── assessment_controller.py# Assessment instructions
│   │   ├── question_controller.py  # Question flow, scoring, submission
│   │   ├── history_controller.py   # History list + detail views
│   │   └── main_controller.py      # Home page
│   │
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── user.py                 # User model
│   │   ├── question.py             # Question model (pool of 60)
│   │   └── assessment_history.py   # Assessment result records
│   │
│   ├── services/                   # Business logic layer
│   │   ├── auth_service.py         # Registration & authentication logic
│   │   └── prediction_service.py   # ML model loading & inference
│   │
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── base.html               # Base layout (navbar, footer)
│   │   ├── home.html               # Landing page
│   │   ├── dashboard.html          # User dashboard
│   │   ├── register.html           # Registration form
│   │   ├── auth/login.html         # Login form
│   │   ├── assessment/             # Assessment flow templates
│   │   │   ├── instructions.html
│   │   │   ├── questions.html
│   │   │   └── result.html
│   │   └── history/                # History templates
│   │       ├── history.html
│   │       └── detail.html
│   │
│   ├── static/                     # Static assets
│   │   ├── css/base.css
│   │   ├── js/
│   │   └── img/
│   │
│   ├── __init__.py                 # App factory (create_app)
│   ├── config.py                   # Environment configurations
│   └── extensions.py               # Flask extensions (db, bcrypt, login)
│
├── ml/                             # Machine learning pipeline
│   ├── models/
│   │   └── random_forest_model.pkl # Trained model artifact
│   ├── generate_dataset.py         # Synthetic dataset generation
│   └── train_model.py              # Model training script
│
├── dataset/
│   └── digital_loneliness_dataset.csv  # Generated training data
│
├── migrations/                     # Alembic migration scripts
│   └── versions/
│
├── tests/                          # Test suite (placeholder)
├── seed_questions.py               # Seeds 60 questions into the database
├── run.py                          # Application entry point
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Digital-loneliness-predictor.git
cd Digital-loneliness-predictor
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (or set environment variables directly):

```env
SECRET_KEY=your-secure-secret-key
DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/digital_loneliness_db
```

### 5. Create the MySQL Database

```sql
CREATE DATABASE digital_loneliness_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Apply Database Migrations

```bash
flask db upgrade
```

### 7. Seed the Question Bank

```bash
python seed_questions.py
```

### 8. Train the ML Model *(optional — pre-trained model included)*

```bash
# Generate dataset
python ml/generate_dataset.py

# Train and save model
python ml/train_model.py
```

---

## ▶️ How to Run

```bash
python run.py
```

The application will start at **`http://127.0.0.1:5000`**

| Route | Description |
|---|---|
| `/` | Landing page |
| `/register` | Create a new account |
| `/login` | User login |
| `/dashboard` | User dashboard (requires login) |
| `/assessment` | Assessment instructions |
| `/assessment/questions` | Take the assessment |
| `/assessment/result` | View prediction result |
| `/history` | Assessment history list |
| `/history/<id>` | Assessment detail view |

---

## 📸 Screenshots

> *Screenshots will be added after UI finalisation.*

| Page | Preview |
|---|---|
| 🏠 Home Page | `screenshots/home.png` |
| 📊 Dashboard | `screenshots/dashboard.png` |
| 📋 Assessment Questions | `screenshots/questions.png` |
| ✅ Result Page | `screenshots/result.png` |
| 🗂️ History Page | `screenshots/history.png` |
| 🔍 History Detail | `screenshots/detail.png` |

---

## 🚀 Future Enhancements

- [ ] **PDF Report Export** — Allow users to download their assessment result as a formatted PDF
- [ ] **Admin Dashboard** — Analytics panel showing aggregate risk distribution across all users
- [ ] **Email Notifications** — Periodic reminders to retake the assessment and track progress
- [ ] **Multi-language Support** — Localisation for broader accessibility
- [ ] **REST API** — Expose prediction endpoint for third-party integrations or mobile apps
- [ ] **OAuth Integration** — Sign in with Google / GitHub
- [ ] **Trend Visualisation** — Line charts showing risk score progression over time
- [ ] **CSRF Protection** — Implement Flask-WTF CSRF tokens across all POST forms
- [ ] **Unit & Integration Tests** — Full test coverage using pytest

---

## 👤 Author

<div align="center">

**Arul**

*Full-Stack Developer & ML Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/<your-username>)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/<your-profile>)

</div>

---

<div align="center">

*Built with ❤️ using Flask, scikit-learn, and Bootstrap*

</div>
