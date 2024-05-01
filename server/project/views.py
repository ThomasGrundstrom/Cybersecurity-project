import sqlite3
from django.shortcuts import render, redirect
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
    friends = acc.friends.all()
    accounts = Account.objects.exclude(user_id=request.user.id)
    chats = acc.chats.all()
    return render(request, 'project/index.html', {'friends': friends, 'accounts': accounts, 'chats': chats})

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
def searchUsers(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    query = request.GET.get('query')
    response = cursor.execute("SELECT username FROM auth_user WHERE username LIKE '%" + query + "%'")
    users = []
    for i in response:
        if i[0] != request.user.username:
            users.append(i[0])
#    SECURE SEARCH FUNCTION BELOW:
#    users = User.objects.filter(username__icontains=query).exclude(username=request.user.username).values_list('username', flat=True)
    return render(request, 'project/displayusers.html', {'users': users})

@login_required
def addFriend(request):
    if request.method == 'POST':
        acc1 = Account.objects.get(user=request.user)
        acc2name = request.POST.get('username')
        user2 = User.objects.get(username=acc2name)
        acc2 = Account.objects.get(user=user2)
        if len(acc1.friends.all()) != 0:
            for friend in acc1.friends.all():
                if acc2 == friend:
                    return redirect('/')
        acc1.friends.add(acc2)
        acc1.save()
    return redirect('/')

@login_required
def openChat(request):
    to = User.objects.get(username=request.GET.get('to'))
    try:
        chat = Chat.objects.get(user1=request.user, user2=to)
    except:
        chat, created = Chat.objects.get_or_create(user1 = to, user2 = request.user)
        if created:
            acc1 = Account.objects.get(user=request.user)
            acc2 = Account.objects.get(user=to)
            acc1.chats.add(chat)
            acc2.chats.add(chat)
            acc1.save()
            acc2.save()
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

@login_required
def deleteChat(request):
    to = request.GET.get('to')
    return render(request, 'project/deleteconfirm.html', {'to': to})

@login_required
def deleteConfirm(request):
    if request.method == 'POST':
        to = request.POST.get('to')
        receiver = User.objects.get(username=to)
        try:
            chat = Chat.objects.get(user1=request.user, user2=receiver)
        except:
            chat = Chat.objects.get(user1=receiver, user2=request.user)
        for message in chat.messages.all():
            message.delete()
        chat.delete()
    return redirect('/')

@login_required
def deleteFriend(request):
    if request.method == 'POST':
        friend = request.POST.get('friend')
        friend_user = User.objects.get(username=friend)
        friend_acc = Account.objects.get(user=friend_user)
        acc = Account.objects.get(user=request.user)
        acc.friends.remove(friend_acc)
    return redirect('/')