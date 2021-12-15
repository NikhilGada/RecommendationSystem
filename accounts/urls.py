from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('detail/',views.detailmovie,name='detailmovie'),
    path('recommendation/',views.recommendation,name='recommendation'),
    path('search/',views.Search,name='search'),
    path('about/',views.about,name='about'),
    path('home/',views.home,name='home')


]