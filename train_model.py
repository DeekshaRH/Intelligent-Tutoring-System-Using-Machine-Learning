import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Set non-interactive backend for safe matplotlib use (if needed)
import matplotlib
matplotlib.use('Agg')

# For reproducibility
np.random.seed(42)

# Load data from Django
def load_data():
    try:
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutor.settings")
        django.setup()
        from education_tutor.models import QuizResult

        results = QuizResult.objects.all()
        if not results.exists():
            return None

        df = pd.DataFrame({
            'score': [r.score for r in results],
            'time_taken': pd.to_numeric([r.time_taken for r in results], errors='coerce'),
            'accuracy': [r.accuracy for r in results],
            'level': [{'Beginner': 0, 'Intermediate': 1, 'Expert': 2}[r.level] for r in results]
        })
        return df.dropna()
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Fallback data
fallback_data = pd.DataFrame({
    'score': [2, 4, 6, 9, 11, 13, 7, 10, 3, 5, 8, 12, 1, 3, 5, 7, 9, 10, 12, 14],
    'time_taken': [300, 400, 350, 500, 600, 550, 450, 480, 370, 420, 460, 580, 320, 380, 410, 470, 520, 490, 570, 610],
    'accuracy': [40.0, 50.0, 60.0, 80.0, 90.0, 95.0, 70.0, 85.0, 45.0, 55.0, 75.0, 88.0, 30.0, 50.0, 60.0, 70.0, 82.0, 87.0, 92.0, 96.0],
    'level': [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, 1, 2, 0, 0, 1, 1, 1, 2, 2, 2]
})

# Step 1: Load and clean data
data = load_data()
if data is None or len(data) < 20:
    data = fallback_data

# Basic filtering
data = data[(data['time_taken'] > 0) & (data['accuracy'].between(0, 100)) & (data['score'] >= 0)]

# Step 2: Prepare features and target
X = data[['score', 'time_taken', 'accuracy']]
y = data['level']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 4: Train simple Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# Step 5: Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Ensure correct handling if not all classes appear in the test set
labels = [0, 1, 2]
target_names = ['Beginner', 'Intermediate', 'Expert']

print(classification_report(
    y_test,
    y_pred,
    labels=labels,
    target_names=target_names,
    zero_division=0
))


# Step 6: Save model
base_dir = os.path.dirname(__file__)
joblib.dump(model, os.path.join(base_dir, "ml_model.pkl"))
joblib.dump(scaler, os.path.join(base_dir, "scaler.pkl"))
print("✅ Model and scaler saved.")
