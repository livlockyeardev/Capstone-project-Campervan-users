from django.shortcuts import render

# Create your views here.
wex\capstone\yourapp\views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = form.cleaned_data['password']
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Change to your login page name
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})