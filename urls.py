from django.urls import path
from .views import *

urlpatterns = [
    path('', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('todo/', todo_view, name='todo'),
    
    path('todo_edit/<int:task_serno>/', todo_edit_view, name='todo_edit'),  # Add trailing slash here

    path('update_status/<int:task_id>/', update_task_status , name='update_status'),
    path('delete_task/<int:task_serno>/',delete_task_view ,name='delete_task'      )  

]


# Request URL:	http://127.0.0.1:8000/todo_edit//