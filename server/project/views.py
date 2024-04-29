from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account, Chat, Message

# Create your views here.

@login_required
def index(request):
    try:
        acc = Account.objects.get(user=request.user)
    except:
        acc = Account.objects.create(user=request.user)
    balance = acc.balance
    friends = acc.friends.all()
    accounts = Account.objects.exclude(user_id=request.user.id)
    return render(request, 'project/index.html', {'balance': balance, 'friends': friends, 'accounts': accounts})

def signUpView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'project/signup.html', {'form': form})

@login_required
def addBalance(request):
    if request.method == 'POST':
        acc = Account.objects.get(user=request.user)
        acc.balance += 10
        acc.save()
    return redirect('/')

@login_required
def addFriend(request):
    if request.method == 'POST':
        acc1 = Account.objects.get(user=request.user)
        acc2name = request.POST.get('name')
        acc2 = Account.objects.get(user=acc2name)
    return redirect('/')

@login_required
def openChat(request):
    to = User.objects.get(username=request.GET.get('to'))
    try:
        chat = Chat.objects.get(user1=request.user, user2=to)
    except:
        chat, created = Chat.objects.get_or_create(user1 = to, user2 = request.user)
    messages = chat.messages.all()[::-1]
    return render(request, 'project/chat.html', {'chat': chat, 'to': to, 'messages': messages})

@login_required
def sendMessage(request):
    if request.method == 'POST':
        text = request.POST.get('newmessage')
        receiver = request.POST.get('receiver')
        to = User.objects.get(username=receiver)
        try:
            chat = Chat.objects.get(user1=request.user, user2=to)
        except:
            chat = Chat.objects.get(user1=to, user2=request.user)
        message = Message.objects.create(sender=request.user, content=text)
        chat.messages.add(message)
        chat.save()
    return redirect('/chat/?to=' + receiver)