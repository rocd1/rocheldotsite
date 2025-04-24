from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from .models import Chapter, Lesson, Flashcard, Quiz
from .serializers import ChapterSerializer, LessonSerializer, FlashcardSerializer, QuizSerializer



# views.py
def offline_view(request):
    return render(request, 'mandarin/offline.html')

def home(request):
    chapters = Chapter.objects.all()  
    return render(request, 'mandarin/home.html', {'chapters': chapters})


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('home')  

    return render(request, 'mandarin/register.html')  


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'mandarin/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')  


def chapter_detail(request, chapter_id):
    chapter = get_object_or_404(Chapter.objects.prefetch_related('lessons'), id=chapter_id)
    lessons = chapter.lessons.all()
    
    return render(request, 'mandarin/chapter_detail.html', {
        'chapter': chapter,
        'lessons': lessons
    })



from django.core.paginator import Paginator



def lesson_detail(request, lesson_id):
    # Retrieve the lesson and prefetch related flashcards and quizzes
    lesson = get_object_or_404(Lesson.objects.prefetch_related('flashcards', 'quizzes'), id=lesson_id)
    flashcards_list = lesson.flashcards.all().order_by('id')
    quizzes_list = lesson.quizzes.all().order_by('id')
    
    # Pagination for flashcards (8 per page)
    flashcard_paginator = Paginator(flashcards_list, 8)
    flashcard_page_number = request.GET.get('flashcard_page')
    flashcards = flashcard_paginator.get_page(flashcard_page_number)

    # Pagination for quizzes (5 per page)
    quiz_paginator = Paginator(quizzes_list, 5)
    quiz_page_number = request.GET.get('quiz_page')
    quizzes = quiz_paginator.get_page(quiz_page_number)
    

    # Initialize quiz results and score
    results = {}
    score = 0

    if request.method == 'POST':
            # Loop through the submitted answers
            for key, value in request.POST.items():
                if key.startswith('question_'):  
                    quiz_id = key.split('_')[1]  
                    try:
                        quiz = Quiz.objects.get(id=quiz_id)  
                        user_answer = value  
                        is_correct = user_answer == quiz.correct_answer  
                        
                        # Store result details
                        results[quiz.id] = {
                            'question': quiz.question,
                            'user_answer': user_answer,
                            'correct_answer': quiz.correct_answer,
                            'correct_answer_text': getattr(quiz, f"option_{quiz.correct_answer.lower()}"), 
                            'is_correct': is_correct
                        }
                        
                        if is_correct:
                            score += 1
                    except Quiz.DoesNotExist:
                        # Handle case where quiz ID does not exist
                        results[quiz_id] = {
                            'error': 'Quiz not found'
                        }


    # Render the template with the full results
    return render(request, 'mandarin/lesson_detail.html', {
        'lesson': lesson,
        'flashcards': flashcards,
        'quizzes': quizzes,
        'results': results,  
        'score': score,      
    })



# Chapter ViewSet
class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAdminUser]


# Lesson ViewSet
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]

# Flashcard ViewSet
class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAdminUser]


# Quiz ViewSet
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAdminUser]
