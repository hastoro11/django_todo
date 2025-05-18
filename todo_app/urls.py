from django.urls import path
from . import views
app_name = 'todo_app'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home' ),
    path('login/', views.LoginView.as_view(), name='login' ),
    path('logout/', views.log_out, name='logout' ),
    path('login_complete/', views.login_complete, name='login_complete' ),
    path('add_todo/', views.add_todo, name='add_todo'),
    path('edit_todo/<int:pk>', views.EditTodoView.as_view(), name='edit_todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete_todo'),
    path('complete_todo/<int:pk>', views.complete_todo, name='complete_todo'),
]