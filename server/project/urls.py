from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signUpView, name='signup'),
    path('chat/', views.openChat, name='chat'),
    path('chat/sendmessage/', views.sendMessage, name="sendmessage"),
    path('searchusers/', views.searchUsers, name='searchusers'),
    path('addfriend/', views.addFriend, name='addfriend')
]