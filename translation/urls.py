from django.urls import path
from . import views

app_name= 'translation'

urlpatterns = [
    path('',views.TranslationView.as_view(), name='translate'),
    path('history/', views.TranslationHistoryView.as_view(), name='history'),
    path('delete/<int:pk>/',views.delete_translations, name='delete'),
]
