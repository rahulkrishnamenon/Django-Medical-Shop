from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages 


def home(request):
    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form':form}
    return render(request, 'webapp/login.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect('login')

from django.db.models import Q

@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'
    my_records = Record.objects.filter(Q(medicine_name__iexact=query) | Q(medicine_name__startswith=query))

    context = {
        'records': my_records,
        'search_query': query,  # Pass the search query to the template
    }

    return render(request, 'webapp/dashboard.html', context=context)

#Create a record
@login_required(login_url='login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/create-record.html', context=context)

#update/edit record

@login_required(login_url='login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
      form = UpdateRecordForm(request.POST, instance=record)
      if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context=context)

#read/view record
@login_required(login_url='login')
def single_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request, 'webapp/view-record.html', context=context)

#delete
@login_required(login_url='login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('dashboard')
    return render(request,'webapp/delete-record.html',{'record':record})


