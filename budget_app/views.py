from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import ExpenseInfo, AccountInfo
from .forms import ExpenseForm
from django.db.models import Q, Sum
# Create your views here.
# def login(request):
#     return render(request, 'budget_app/login.html')

def budget_app(request):
    return render(request, 'index.html', {})

def index(request):
    expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')

    try:
        budget_total = AccountInfo.objects.filter(user_budget=request.user)
        expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__gt=0)))
    except TypeError:
        print('No data.')

    context = {
        'user':request.user,
        'expense_items':expense_items,
        'budget':budget_total['budget'],
        'expenses':expense_total['expenses']
    }

    return render(request, 'budget_app/index.html', context)

def add_item(request):
    name = request.POST['expense_name']
    expense_cost = request.POST['cost']
    ## yyyy/mm/dd
    expense_date = request.POST['expense_date']

    ExpenseInfo.objects.create(expense_name=name, cost=expense_cost,
        date_added=expense_date, user_expense=request.user)

    budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
    expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))

    return HttpResponseRedirect('app')

def edit_item(request, id):
    ## Edit each item based on ID
    expense_item = ExpenseInfo.objects.get(id=id)
    form = ExpenseForm(instance = expense_item)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense_item)
        if form.is_valid():
            form.save()
            return redirect('/app')    

    context = {'form':form}

    return render(request, 'budget_app/edit.html', context)

def update_item(request, id):
    expense_item = ExpenseInfo.objects.get(id=id)
    form = ExpenseForm(instance = expense_item)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense_item)
        if form.is_valid():
            form.save()
            return redirect('budget_app/index.html')

    return render(request, 'budget_app/edit.html', {'expense_item':expense_item})

def delete_item(request, id):
    ## Delete each item based on PK
    expense_item = ExpenseInfo.objects.get(id=id)
    if request.method == "POST":
        expense_item.delete()
        return redirect('/app')

    context = { 'expense_item': expense_item }
    return render(request, 'budget_app/remove.html', context)
    
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('app')
        else:
            for msg in form.error_message:
                print(form.error_messages[msg])
    else:
        form = UserCreationForm
        return render(request, 'budget_app/sign_up.html', {'form':form})
    # return render(request, 'registration/sign_up.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')