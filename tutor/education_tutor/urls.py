from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/<int:language_id>/', views.start_quiz, name='start_quiz'),
    path('submit_quiz/<int:language_id>/', views.submit_quiz, name='submit_quiz'),
    path("results/", views.quiz_results, name="quiz_results"),  # ✅ Ensure this exists
    path('roadmap/<int:language_id>/<str:level>/', views.roadmap, name='roadmap'),\
    path('quiz_template/', views.quiz_view, name='quiz_template'),


]
