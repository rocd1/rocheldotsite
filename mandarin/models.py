from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_lesson = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Current Lesson: {self.current_lesson}"


class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='flashcards')
    chinese_character = models.CharField(max_length=10)
    pinyin = models.CharField(max_length=50)
    english_translation = models.CharField(max_length=255)

    def __str__(self):
        return self.chinese_character


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return self.question[:50]

