from django.urls import path
from .views import home,dashboard,privacyView

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('privacy/', privacyView, name='privacy'),
]
