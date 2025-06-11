import os
import json
import joblib
import matplotlib.pyplot as plt
import io
import urllib
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import ProgrammingLanguage, Question, QuizResult, Roadmap

# Load trained ML model and scaler
model_path = os.path.join(settings.BASE_DIR, "ml_model.pkl")
scaler_path = os.path.join(settings.BASE_DIR, "scaler.pkl")
if os.path.exists(model_path) and os.path.exists(scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
else:
    model = None
    scaler = None

# Generate performance graphs for each programming language
def generate_performance_graph(user):
    graph_urls = {}  # Dictionary to store graphs for each language

    # Get all languages the user has taken quizzes for
    languages = QuizResult.objects.filter(user=user).values_list('language', flat=True).distinct()

    for language_id in languages:
        language = get_object_or_404(ProgrammingLanguage, id=language_id)
        results = QuizResult.objects.filter(user=user, language=language).order_by('id')

        if not results.exists():  # Skip if no results for this language
            continue

        # Extract data for plotting
        attempts = list(range(1, len(results) + 1))  # X-axis: Quiz attempts
        scores = [result.score for result in results]  # Y-axis: Scores
        accuracies = [result.accuracy for result in results]  # For hover data

        # Create the graph
        fig, ax = plt.subplots(figsize=(6, 4))

        # Plot scores
        ax.plot(attempts, scores, marker='o', linestyle='-', color='b', label=f"{language.name} Score")
        ax.set_xlabel("Quiz Attempt Number")
        ax.set_ylabel("Score", color='b')
        ax.tick_params(axis='y', labelcolor='b')
        ax.grid(True)

        # Set integer ticks for x and y axes
        ax.set_xticks(range(1, len(attempts) + 1))  # Integer ticks for x-axis
        ax.set_yticks(range(0, max(scores) + 1, 1))  # Integer ticks for y-axis

        # Title and legend
        plt.title(f"Performance Over Time ({language.name})")
        fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05))

        # Save the graph in memory
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        # Encode the image to send to the template
        graph_url = urllib.parse.quote(base64.b64encode(buffer.getvalue()).decode())
        # Prepare data for hover tooltips
        data = [{'attempt': attempt, 'score': score, 'accuracy': accuracy} 
                for attempt, score, accuracy in zip(attempts, scores, accuracies)]
        graph_urls[language.name] = {
            'url': graph_url,
            'data_json': json.dumps(data)  # Serialize data to JSON string
        }

    return graph_urls

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'education_tutor/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'education_tutor/login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard
@login_required
def dashboard(request):
    languages = ProgrammingLanguage.objects.all()
    return render(request, 'education_tutor/dashboard.html', {'languages': languages})
 

    

# Start Quiz
@login_required
def start_quiz(request, language_id):
    language = get_object_or_404(ProgrammingLanguage, id=language_id)
    questions = Question.objects.filter(language=language)
    return render(request, 'education_tutor/quiz.html', {'language': language, 'questions': questions})


# Submit Quiz (Uses ML to predict level)
@login_required
def submit_quiz(request, language_id):
    if request.method == "POST":
        language = get_object_or_404(ProgrammingLanguage, id=language_id)
        questions = Question.objects.filter(language=language)

        # Calculate score
        total_questions = questions.count()
        correct_answers = sum(1 for question in questions if request.POST.get(str(question.id)) == question.correct_option)
        accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        time_taken = float(request.POST.get("time_taken", 300))  # Default 300 sec if not available

        # Predict level using ML model
        if model and scaler:
            input_data = scaler.transform([[correct_answers, time_taken, accuracy]])
            predicted_level = model.predict(input_data)[0]
            level_mapping = {0: 'Beginner', 1: 'Intermediate', 2: 'Expert'}
            level = level_mapping.get(predicted_level, 'Beginner')
        else:
            level = "Beginner" if correct_answers < 5 else "Intermediate" if correct_answers < 10 else "Expert"

        # Save result
        QuizResult.objects.create(user=request.user, language=language, score=correct_answers, 
                                  time_taken=time_taken, accuracy=accuracy, level=level)

        messages.success(request, f"Quiz submitted! You scored {correct_answers}/{total_questions} - Level: {level}")
        return redirect("quiz_results")

    return redirect("dashboard")

# Quiz Results
@login_required
def quiz_results(request):
    results = QuizResult.objects.filter(user=request.user)
    return render(request, 'education_tutor/results.html', {'quiz_results': results})

# Performance Graphs
@login_required
def performance(request):
    graph_urls = generate_performance_graph(request.user)
    return render(request, 'education_tutor/performance.html', {'graph_urls': graph_urls})

# Load roadmap data from JSON file
def load_roadmap_data():
    roadmap_path = os.path.join(settings.BASE_DIR, "education_tutor", "static", "data", "roadmaps.json")  

    if not os.path.exists(roadmap_path):
        print(f"⚠️ Roadmap file not found at: {roadmap_path}")  # Debugging message
        return {}

    try:
        with open(roadmap_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON Decoding Error: {e}")  # Debugging message
        return {}

@login_required
def roadmap(request, language_id, level):
    language = get_object_or_404(ProgrammingLanguage, id=language_id)
    roadmap_data = load_roadmap_data()
    roadmap_steps = roadmap_data.get(language.name, {}).get(level, [])

    return render(request, 'education_tutor/roadmap.html', {
        'language': language,
        'level': level,
        'roadmap': roadmap_steps,
    })