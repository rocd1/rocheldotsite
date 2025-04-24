from . import views

from django.conf import settings
from django.conf.urls.static import static



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChapterViewSet, LessonViewSet, FlashcardViewSet, QuizViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'chapters', ChapterViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'flashcards', FlashcardViewSet)
router.register(r'quizzes', QuizViewSet)

urlpatterns = [
    path('offline/', views.offline_view, name='offline'),

    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('chapters/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),

    path('api/', include(router.urls)),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)