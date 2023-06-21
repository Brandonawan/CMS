from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db import IntegrityError
from .models import *

# Create your views here.

def home(request):
    posts = Post.objects.order_by('-created_at')  # Retrieve posts in reverse order based on the 'created_at' field
    page_name = "CMS Home"
    return render(request, 'blog/home.html', {'posts': posts, 'page_name': page_name})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Admin user functionality
        # You can perform operations like deleting users, posts, etc.
        users = User.objects.all()
        posts = Post.objects.all()
        page_name = "Admin Dashboard"
        return render(request, 'blog/admin_dashboard.html', {'users': users, 'posts': posts, 'page_name': page_name})
    else:
        # Regular user functionality
        # Display only the user's posts
        posts = Post.objects.filter(author__user=request.user)
        page_name = "User Dashboard"
        return render(request, 'blog/user_dashboard.html', {'posts': posts, 'page_name': page_name})


# def delete_user(request, user_id):
#     if request.user.is_superuser: # Ensure only the admin can delete users
#         User.objects.filter(id=user_id).delete()
#     return redirect('blog/admin_dashboard')

def delete_user(request, user_id):
    if request.user.is_superuser: # Ensure only the admin can delete users
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            user.delete()
            return redirect('dashboard')
        return render(request, 'blog/delete_user.html', {'user': user})
    return redirect('dashboard')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user is the author or an admin
    if request.user == post.author.user or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('dashboard')
        return render(request, 'blog/delete_post.html', {'post': post})
    
    # Redirect to the dashboard if the user is not authorized
    return redirect('dashboard')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard page upon successful login
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'blog/login.html', {'error_message': error_message})
    
    return render(request, 'blog/login.html')
    
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            try:
                # Create a new user object
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('login')  # Redirect to the login page after successful registration
            except IntegrityError:
                error_message = 'Username is already taken. Please choose a different username.'
                return render(request, 'blog/register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords do not match. Please try again.'
            return render(request, 'blog/register.html', {'error_message': error_message})
    
    return render(request, 'blog/register.html')

    
    return render(request, 'blog/register.html')

def check_username_availability(request):
    username = request.GET.get('username')
    if User.objects.filter(username=username).exists():
        data = {'available': False, 'message': 'Username is already taken.'}
    else:
        data = {'available': True, 'message': 'Username is available.'}
    return JsonResponse(data)

@login_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        author, created = Author.objects.get_or_create(user=request.user)
        
        post = Post(title=title, content=content, author=author)
        post.save()
        
        page_name = "Compose Post"
        return redirect('home')
        
    return render(request, 'blog/add_post.html')

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user is the author or an admin
    if request.user == post.author.user or request.user.is_superuser:
        if request.method == 'POST':
            # Retrieve the updated title and content from the form
            title = request.POST.get('title')
            content = request.POST.get('content')
            
            # Update the post with the new data
            post.title = title
            post.content = content
            post.save()
            return redirect('dashboard')
        
        return render(request, 'blog/edit_post.html', {'post': post})
    
    # Redirect to the dashboard if the user is not authorized
    return redirect('dashboard')

