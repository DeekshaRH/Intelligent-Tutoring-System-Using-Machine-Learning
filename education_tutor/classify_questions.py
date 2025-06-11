import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from education_tutor.models import Question

# Fetch all questions
questions = [q.text for q in Question.objects.all()]

# Convert text to numerical features
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(questions)

# Apply clustering (3 clusters for Easy, Medium, Hard)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Save model
joblib.dump((vectorizer, kmeans), "question_difficulty_classifier.pkl")

# Map clusters to difficulty levels
difficulty_mapping = {0: "Easy", 1: "Medium", 2: "Hard"}

# Save classification results
for i, question in enumerate(Question.objects.all()):
    question.difficulty = difficulty_mapping[clusters[i]]
    question.save()

print("✅ Question classification completed!")
