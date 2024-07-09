from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Q
from .forms import updateform
from django.contrib import messages
from django.core.mail import send_mail



# Create your views here.

def signup(request):
    #to redirect to pages if logged in
    if request.user.is_superuser:
        return redirect(admin)
    elif request.user.is_authenticated:
        return redirect(index)

    # to create users
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        print(username)

        if len(username.strip()) < 4:
            messages.info(request, 'Username must be at least 4 characters')
        elif len(password.strip()) < 4:
            messages.info(request, 'Password must be at least 4 characters')
        else:
            subject = "Greetings!"
            message = f"Your Account at Xiagio has been created with the username {username}"
            from_email = 'your_email@example.com'  # Replace with your sender's email address

            try:
                send_mail(subject, message, from_email, [email], fail_silently=False)
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully. Check your email for details.')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')

            return redirect(user_login)

    return render(request, 'signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    #to redirect to pages if logged in
     if request.user.is_superuser:
         return redirect(admin)
     elif request.user.is_authenticated:
         return redirect(index)
         
     
    
# to authenticate
     if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
# to redirect admin and users
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect(admin)
            else:
                return redirect(index)
        else:
            messages.info(request,'invalid username or password')
     return render(request,'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    return redirect(user_login)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin(request):
    
    if request.user.is_superuser:
        if 'q' in request.GET:
            search=request.GET['q']
            data=User.objects.filter(username__icontains=search,is_superuser=False)
        else:
            data=User.objects.filter(is_superuser=False)
        return render(request,'admin.html',{'data':data})
    return redirect (user_login)
        
        
 
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(user_login)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_user(request):
    if request.user.is_superuser:
     if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        user=User.objects.create_user(username=username,password=password,email=email)
        user.save()
        messages.info(request, 'User created successfully')
        return redirect(admin)
     return render(request,'add.html')
    else:
        return redirect(user_login)
    

def delete(request,id):
    if request.user.is_superuser:
        dele=User.objects.get(id=id)
        if dele.is_superuser:
            return redirect(admin)
        else:
            dele.delete()
    return redirect(admin)

def edit(request, id):
    if request.user.is_superuser:
        data = get_object_or_404(User, id=id)
        form = updateform(instance=data)
        
        if request.method == 'POST':
            form = updateform(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.info(request, 'User updated successfully')
                return redirect('admin')  # Assuming 'admin' is the name of the URL pattern
        
        return render(request, 'update.html', {'form': form})
    else:
        messages.error(request, 'You do not have permission to edit users.')
        return redirect('user_login')




    
    
        
        



        
    
