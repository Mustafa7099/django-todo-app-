from django.shortcuts import render , redirect , HttpResponse  , get_object_or_404
from .forms import *
from .models import Task
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate , login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt



from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def signup_view(request):
    
    try:
        if request.user.is_authenticated:
            return redirect('todo')  # ✅ منع المستخدم المسجل من التسجيل مرة أخرى

        if request.method == 'POST':
            signup_form = SignupForm(request.POST)

            if signup_form.is_valid():
                user = User.objects.create_user(
                first_name=signup_form.cleaned_data['first_name'],
                last_name=signup_form.cleaned_data['last_name'],
                username=signup_form.cleaned_data['username'],
                email=signup_form.cleaned_data['email'],
                password=signup_form.cleaned_data['password1']
                )
                # user = User.objects.create_user(signup_form)
                user.save()  # ✅ إنشاء المستخدم وحفظه بشكل آمن
                
                messages.success(request, "✅ Account created successfully! Please log in.")
                return redirect('login')
            else:
                # عرض جميع الأخطاء الموجودة في النموذج
                for field, errors in signup_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        else:
            signup_form = SignupForm()

    except Exception as error: 
        messages.error(request, f"❌ An unexpected error occurred: {error}")

    return render(request, 'signup.html', {'signup_form': signup_form  })


def login_view(request):
    # ✅ إذا كان المستخدم مسجلاً بالفعل، يتم توجيهه للصفحة الرئيسية
    try:

        if request.user.is_authenticated:
            return redirect('todo')  

        if request.method == 'POST': 
            login_form = AuthenticationForm(request, data=request.POST)  
            
            if login_form.is_valid():  
                username = login_form.cleaned_data['username'] 
                password = login_form.cleaned_data['password']

                my_user = authenticate(request,username=username , password=password)
                print(my_user)
                
                if my_user is not None : 
                    login(request, my_user)
                    return redirect('todo')  

                # ✅ دعم إعادة التوجيه إلى الصفحة السابقة بعد تسجيل الدخول
                    next_url = request.GET.get('next', 'todo')
                    return redirect(next_url)

            messages.error(request, "❌ Invalid username or password.")  # ✅ عرض رسالة خطأ

        else: 
            login_form = AuthenticationForm()
    except Exception as error : 
        messages.error(request  ,  f"{error}"  )

    return render(request, 'login.html', {'login_form': login_form})  

def todo_view (request )  :
    if request.method == 'POST' : 
        text = request.POST.get('text')
        
        new_task =  Task( text=text  , user=request.user  )
        if  new_task.text   ==  ""  :
            messages.error(request,"no thing to save it")
            return  redirect('todo')
        new_task.save()
        
        res = Task.objects.filter(user=request.user).order_by('-date')
        return  redirect( 'todo')
        
    res = Task.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'todo.html', {'res': res}  )



def todo_edit_view(request, task_serno):
    try:
        # ✅ استخدم get_object_or_404 لتجنب الأخطاء في حالة عدم وجود المهمة
        task = get_object_or_404(Task.objects.select_for_update('text') , srno=task_serno)

        if request.method == 'POST':
            text = request.POST.get('text')
            task.text = text
            task.save()
            messages.success(request, "✅ Task updated successfully!")
            return redirect('todo')

        return render(request, 'todo_edit.html', {'task': task})

    except Exception as error:
        messages.error(request, f"❌ Error: {error}")
        return redirect('todo')
    
@csrf_exempt

def update_task_status(request, task_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task = get_object_or_404(Task, srno=task_id)
            task.status = data.get("status", False)
            task.save()
            return JsonResponse({"message": "✅ Task status updated!", "status": task.status})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_task_view(request, task_srno):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to delete tasks")
        return redirect('login')
        
    if request.method == 'POST':
        try:
            # Get the task and ensure it belongs to the current user
            task = get_object_or_404(Task, srno=task_srno, user=request.user)
            task.delete()
            messages.success(request, f'✅ Task {task_srno} has been deleted successfully')
            return redirect('todo')
        
        except Task.DoesNotExist:
            messages.error(request, '❌ Task not found or you do not have permission to delete it')
            return redirect('todo')
            
        except Exception as error:
            messages.error(request, f'❌ An error occurred: {str(error)}')
            return redirect('todo')
    
    # If not POST request, redirect to todo page
    return redirect('todo')

