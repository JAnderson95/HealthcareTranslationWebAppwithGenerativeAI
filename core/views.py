from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# Create your views here.
def home (request):
    return render (request, 'core/home.html')

def privacyView(TemplateView):
    templante_menu = 'core/privacy.html'


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html',{
        'user':request.user
    })