from django.shortcuts import render,redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from . import models
from .models import Task
# Create your views here.
def signup(request):
   if request.method=="POST":
      username= request.POST['username']
      email = request.POST['email']
      password= request.POST['password']
      confirmpassword= request.POST['confirmpassword']
      if password==confirmpassword:
         if User.objects.filter(username=username).exists():
          messages.info(request,'username taken')
          return redirect('signup')
         elif User.objects.filter(email=email).exists():
          messages.info(request,'email taken')
          return redirect('signup')
         else:
          user = User.objects.create_user(username=username, password=password,email=email)
          user.save()
          print("user created")
          return redirect('login')
      else:
       messages.info(request,'password no match ')
       return redirect('signup')
   else:
     return render(request, 'signup.html')
    
def login(request):
   if request.method=="POST":
     username=request.POST['username']
     password=request.POST['password']
     user = auth.authenticate(username=username,password=password)
     if user is not None:
       auth.login(request,user)
       return redirect('todo')
     else:
       messages.info(request,'invalid credentials')
       return redirect("login")
   else:
     return render(request,'login.html')
def todo(request):
  if request.method=="POST":
    return redirect('addtask')
  
  res = models.Task.objects.filter(user=request.user).order_by('created')
  return render(request, 'todo.html', {'res': res})
  

def addtask(request):
  if request.method=="POST":
    title=request.POST['title']
    description=request.POST['description']
    if title:
      if len(title)>30:
        messages.info(request,"Title length is long")
      else:
        obj=models.Task(title=title, description=description,user=request.user)
        obj.save()
        return redirect('todo')
    else:
     messages.info(request, "Please add task")
  
  return render(request, 'addtask.html')

def edittask(request,pk):
    task = get_object_or_404(Task, id=pk, user=request.user)  
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo')  
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'edittask.html', context)

def deletetask(request,pk):
   task = get_object_or_404(Task, id=pk, user=request.user)
   if request.method == 'POST':
        task.delete()  
        return redirect('todo')  
   return render(request, 'deletetask.html', {'task': task})

def logout(request):
   auth.logout(request)
   return redirect('signup')