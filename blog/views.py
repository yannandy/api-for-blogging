from django.shortcuts import render
from .models import Post
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'message':'Login successful'}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def RegistrationView(request):
    if request.method=='POST':
        data = json.loads(request.body)
        username = data.get('username')
        if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        user=User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        if user:
            return JsonResponse({'message':'Registration succeed'}, status=200)
        return JsonResponse({'message':'failed to register'}, status=401)

@csrf_exempt
def post_creation(request):
     if request.method == 'POST':
          data = json.loads(request.body)
          if not request.user.is_authenticated:
               return JsonResponse({'message':'Authentification required'}, status=401)
          author = request.user
          title = data.get('title')
          content = data.get('content')
          Post.objects.create(author=author, title=title, content=content)
          return JsonResponse({'message':'Post created successfully'}, status=201)
    
def retrieve_all_post(request):
     data_to_retrieve = [{'author':post.author.username, 'title':post.title, 'content':post.content, "created":post.created_at} for post in Post.objects.all()]
     #print(Post.objects.all())
     return JsonResponse({'alldata': data_to_retrieve})
# Create your views here.
