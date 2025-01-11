from django.shortcuts import render
from .models import Post
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

def error_response(message, status=400):
    return JsonResponse({'error': message}, status=status)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            return error_response('Invalid credentials', 401)
        except json.JSONDecodeError:
            return error_response('Invalid JSON format')

    return error_response('Invalid HTTP method', 405)

@csrf_exempt
def RegistrationView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            if User.objects.filter(username=username).exists():
                return error_response('Username already exists', 400)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')

            if not all([username, first_name, last_name, email, password]):
                return error_response('All fields are required')

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            return JsonResponse({'message': 'Registration succeeded'}, status=200)
        except json.JSONDecodeError:
            return error_response('Invalid JSON format')

    return error_response('Invalid HTTP method', 405)

@csrf_exempt
def post_creation(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return error_response('Authentication required', 401)

        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')

            if not title or not content:
                return error_response('Both title and content are required')

            Post.objects.create(author=request.user, title=title, content=content)
            return JsonResponse({'message': 'Post created successfully'}, status=201)
        except json.JSONDecodeError:
            return error_response('Invalid JSON format')

    return error_response('Invalid HTTP method', 405)

def retrieve_all_post(request):
        data_to_retrieve = [
            {'author': post.author.username, 'title': post.title, 'content': post.content, "created": post.created_at}
            for post in Post.objects.all()
        ]
        return JsonResponse({'alldata': data_to_retrieve}, status=200)

@csrf_exempt
def update_post(request, post_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            if not request.user.is_authenticated:
                return error_response('Authentication required', 401)

            title = data.get('title')
            content = data.get('content')

            if not title or not content:
                return error_response('Both title and content are required')

            try:
                post_to_update = Post.objects.get(pk=post_id, author=request.user)
                post_to_update.title = title
                post_to_update.content = content
                post_to_update.save()
                return JsonResponse({'message': 'Post updated successfully'}, status=200)
            except Post.DoesNotExist:
                return error_response('Post not found or unauthorized', 404)
        except json.JSONDecodeError:
            return error_response('Invalid JSON format')

    return error_response('Invalid HTTP method', 405)

@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'DELETE':
        if not request.user.is_authenticated:
            return error_response('Authentication required', 401)

        try:
            post_to_delete = Post.objects.get(pk=post_id, author=request.user)
            post_to_delete.delete()
            return JsonResponse({'message': 'Post deleted successfully'}, status=200)
        except Post.DoesNotExist:
            return error_response('Post not found or unauthorized', 404)

    return error_response('Invalid HTTP method', 405)
