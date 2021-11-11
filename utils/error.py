from django.shortcuts import render, redirect

def error_page(request):
    error = request.session.pop('error', False)
    if error == False:
        error = "We are not sure what, but we will work on fixing it."
    return render(request, 'core/error_page.html', {'error':error})

def handle_error(request, message):
    request.session['error'] = message
    return render(request, 'core/error_page.html', {'error':message})

def require_login(request):
    if not request.user.is_authenticated():
        return render(request, 'core/error_page.html', {'error':"You must be logged in to view this page."})