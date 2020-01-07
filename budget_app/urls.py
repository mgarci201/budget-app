from django.urls import path, include
from budget_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('app', views.index, name='index'),
    path('add_item', views.add_item, name='add item'),
    path('edit/<int:id>', views.edit_item, name='edit item'),
    path('delete/<int:id>', views.delete_item, name='delete_item'),

    ## We're using default django
    path('accounts/',include('django.contrib.auth.urls')),
    path('sign_up', views.sign_up , name='sign up'),
    path('logout',views.logout_view,name='logout'),
]
