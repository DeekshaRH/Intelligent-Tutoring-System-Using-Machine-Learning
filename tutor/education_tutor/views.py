import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProgrammingLanguage, Question, QuizResult

# Load roadmap data from JSON file
import os
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProgrammingLanguage

def load_roadmap_data():
    # Corrected file path using settings.BASE_DIR
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

    # Ensure the language name matches JSON keys
    roadmap_steps = roadmap_data.get(language.name, {}).get(level, [])

    return render(request, 'education_tutor/roadmap.html', {
        'language': language,
        'level': level,
        'roadmap': roadmap_steps,
    })

# ✅ User Registration
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

# ✅ User Login
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

# ✅ User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# ✅ Dashboard (Lists Programming Languages)
@login_required
def dashboard(request):
    languages = ProgrammingLanguage.objects.all()
    return render(request, 'education_tutor/dashboard.html', {'languages': languages})

# ✅ Start Quiz
@login_required
def start_quiz(request, language_id):
    language = get_object_or_404(ProgrammingLanguage, id=language_id)
    questions = Question.objects.filter(language=language)
    return render(request, 'education_tutor/quiz.html', {'language': language, 'questions': questions})

# ✅ Submit Quiz
@login_required
def submit_quiz(request, language_id):
    if request.method == "POST":
        language = get_object_or_404(ProgrammingLanguage, id=language_id)
        questions = Question.objects.filter(language=language)
        
        score = sum(1 for question in questions if request.POST.get(str(question.id)) == question.correct_option)
        level = "Beginner" if score < 5 else "Intermediate" if score < 10 else "Expert"
        
        QuizResult.objects.create(user=request.user, language=language, score=score, level=level)
        messages.success(request, f"Quiz submitted! You scored {score}/{questions.count()} - Level: {level}")
        return redirect("quiz_results")
    
    return redirect("dashboard")

# ✅ Quiz Results
@login_required
def quiz_results(request):
    results = QuizResult.objects.filter(user=request.user)
    return render(request, 'education_tutor/results.html', {'quiz_results': results})

# views.py

from django.shortcuts import render
from education_tutor.models import Question
import random

def quiz_view(request, language_name):
    # Fetch random 5 questions from the selected language
    questions = Question.objects.filter(language__name=language_name)
    random_questions = random.sample(list(questions), 5)  # Select 5 random questions

    return render(request, 'education_tutor/quiz_template.html', {'questions': random_questions})
