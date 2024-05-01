from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signUpView, name='signup'),
    path('chat/', views.openChat, name='chat'),
    path('chat/sendmessage/', views.sendMessage, name="sendmessage"),
    path('searchusers/', views.searchUsers, name='searchusers'),
    path('addfriend/', views.addFriend, name='addfriend'),
    path('delete/', views.deleteChat, name='delete'),
    path('deleteconfirm/', views.deleteConfirm, name='deleteconfirm'),
    path('deletefriend/', views.deleteFriend, name='deletefriend')
]