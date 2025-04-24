from rest_framework import serializers
from .models import Chapter, Lesson, Flashcard, Quiz


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'chinese_character', 'pinyin', 'english_translation', 'lesson']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'lesson']


class LessonSerializer(serializers.ModelSerializer):
    flashcards = FlashcardSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'chapter', 'flashcards', 'quizzes']


class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'lessons']

