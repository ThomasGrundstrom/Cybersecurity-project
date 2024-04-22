from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account

# Create your views here.

@login_required
def index(request):
    try:
        acc = Account.objects.get(user=request.user)
    except:
        acc = Account.objects.create(user=request.user)
    balance = acc.balance
    return render(request, 'project/index.html', {"balance": balance})

def signUpView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'project/signup.html', {"form": form})

@login_required
def addBalance(request):
    if request.method == "POST":
        acc = Account.objects.get(user=request.user)
        acc.balance += 10
        acc.save()
    return redirect('/')