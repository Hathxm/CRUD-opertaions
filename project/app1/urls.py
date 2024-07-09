from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.signup,name='signup'),
    path('login',views.user_login,name='login'),
    path('home',views.index,name='index'),
    path('customadmin',views.admin,name='admin'),
    path('logout',views.user_logout,name='logout'),
    path('add',views.add_user,name='add'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('edit/<int:id>',views.edit,name='edit'),  

]