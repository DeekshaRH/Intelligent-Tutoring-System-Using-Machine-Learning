# Intelligent Tutoring System using Machine Learning

This project is an AI-powered Intelligent Tutoring System designed to personalize learning experiences for students based on their initial assessments. It uses a Django backend, machine learning models, and a structured database to deliver adaptive content, track progress, and provide tailored feedback.

---

## 🚀 Features

- Student registration and domain selection
- Initial assessment and learning phase classification (Beginner, Intermediate, Advanced)
- Machine Learning model for performance prediction
- Personalized learning roadmap generation
- Adaptive content and quizzes based on progress
- Student progress tracking and final evaluation

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite
- **Machine Learning**: Scikit-learn (Random Forest), Joblib
- **Others**: HTML/CSS (if frontend is integrated), Streamlit (optional)

---

## 📂 Project Structure

```
intelligent_tutoring_system/
├── manage.py
├── db.sqlite3
├── train_model.py
├── ml_model.pkl
├── scaler.pkl
├── your_app/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
└── .venv/
```

---

## 🧠 ML Model

The ML model (`ml_model.pkl`) predicts a student's learning phase based on their assessment scores using a trained **Random Forest Classifier**. The model is trained and saved using `train_model.py`.

---

## 💻 Getting Started

### 🔧 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/intelligent-tutoring-system.git
   cd intelligent-tutoring-system
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations and run the server:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

---

## 📈 Train the ML Model

Before running the server, you can retrain the model (optional):

```bash
python train_model.py
```

---

## 📬 Contact

Created by **Deeksha R H** – feel free to reach out!

---

## 📝 License

This project is for academic and learning purposes.
