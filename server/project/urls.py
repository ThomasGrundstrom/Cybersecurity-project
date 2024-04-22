from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signUpView, name='signup'),
    path('addbalance/', views.addBalance, name='addbalance')
]