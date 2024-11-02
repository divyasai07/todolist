from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.signup, name="signup"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("todo",views.todo,name="todo"),
    path("addtask",views.addtask,name="addtask"),
    path("edittask/<int:pk>",views.edittask,name="edittask"),
    path("deletetask/<int:pk>",views.deletetask,name="deletetask")
]