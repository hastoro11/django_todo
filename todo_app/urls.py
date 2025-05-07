from django.urls import path
from . import views
app_name = 'todo_app'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home' ),
    path('login/', views.LoginView.as_view(), name='login' ),
    path('logout/', views.log_out, name='logout' ),
    path('login_complete/', views.login_complete, name='login_complete' ),
]