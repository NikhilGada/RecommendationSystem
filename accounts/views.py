from django.shortcuts import render
from scipy import sparse
# Create your views here.
import os 
import pickle 
import random
import pandas as pd
from django.http import JsonResponse
from csv import writer
import datetime

from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)


def reading_pickle(request):
    filename=os.path.dirname(os.path.abspath(__file__))+'/grocery_pickle.pkl'
    with open(filename,'rb') as f:
        model=pickle.load(f)
    return model

def about(request):
    return render(request,'blog/about.html')


def detailmovie(request):
    model=reading_pickle(request)
    movie=request.GET['movie']
    if movie in model.index:
        return render(request,'blog/detail.html',{'movie':movie})
    else:
        return render(request,'blog/detail.html',{'movie':movie,'message':'Movie Not Found'})
            


def get_similar(request,movie_name,rating):
    model=reading_pickle(request)
    similar_ratings = model[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

def reco(request,movie_collection):
    similar_movies = pd.DataFrame()
    for movie,rating in movie_collection:
        similar_movies = similar_movies.append(get_similar(request,movie,rating),ignore_index = True)
    movie=similar_movies.sum().sort_values(ascending=False).head(9).index
    return movie

def recommendation(request):
    record=os.path.dirname(os.path.abspath(__file__))+'/record.csv'
    movie_name=request.GET['movie']
    rating=request.GET['ratings']
# Here it same data in csv
    with open(record,'a',newline="") as wf:
        csv_writer=writer(wf)
        csv_writer.writerow([movie_name,rating,datetime.date.today()])
    
    movie_collection=[]
    movie_collection.append((movie_name,int(rating)))
    movie=reco(request,movie_collection)
    return render(request,'blog/recommendation.html',{'moviess':movie[1:],'m':movie_name})


def Search(request):
    model=reading_pickle(request)
    mName=request.GET['q']
    value=[val for val in model.index if val.startswith(mName.title())]
    return JsonResponse({'movie':value[:10]})

def home(request):
    model=reading_pickle(request)
    movie=[]
    s=model.index.size-1
    for i in range(21):
        r=random.randint(1,s)
        movie.append(model.index[r])
    return render(request,'blog/home.html',{'moviess':movie})


