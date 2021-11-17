from django.shortcuts import render

from social.models import Board, Topic

def home_page(request):
    announcements = []
    try:
        board = Board.objects.get(name="Announcements")
        announcements = Topic.objects.filter(board=board).order_by('-date')[:5]
    except:
        announcements = []
        
    return render(request, 'core/home_page.html', {'announcements':announcements})

def privacy_policy_page(request):
    return render(request, 'core/privacy_policy_page.html')

def colors_page(request):
    return render(request, 'core/features/colors_page.html')

def rules_page(request):
    return render(request, 'core/rules_page.html')