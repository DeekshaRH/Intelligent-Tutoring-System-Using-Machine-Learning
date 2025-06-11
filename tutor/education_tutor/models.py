from django.db import models
from django.contrib.auth.models import User

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=200)

    def __str__(self):
        return self.text
class QuizResult(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')

    def set_level(self):
        """Determine user level based on score and update the field."""
        if self.score > 10:
            self.level = "Expert"
        elif self.score >= 5:
            self.level = "Intermediate"
        else:
            self.level = "Beginner"
        self.save()


    def __str__(self):
        return f"{self.user.username} - {self.language.name} - {self.level}"

class Roadmap(models.Model):
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Expert', 'Expert')])
    study_plan = models.TextField()  # JSON format for structured roadmap

    def __str__(self):
        return f"{self.language.name} - {self.level} Roadmap"
