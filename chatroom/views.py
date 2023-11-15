from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import json

from .models import User, Message, Chat


def landing(request):
    return render(request, "chatroom/landing.html")


@login_required
def members(request):
    current_user = request.user
    members_list = User.objects.exclude(pk=current_user.id)
    chats = Chat.objects.filter(members=current_user)
    context = {
        "all_members": members_list,
        "chats": chats
    }
    return render(request, "chatapp/members.html", context)


@login_required
def profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    context = {
        "profile": user_profile
    }
    return render(request, "chatapp/profile.html", context)


@login_required
def edit_profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        if profile_picture:
            user_profile.profile_picture = profile_picture
        user_profile.email = email
        user_profile.bio = bio
        user_profile.save()
        return redirect('profile', user_id=user_id)
    context = {
        "profile": user_profile
    }
    return render(request, "chatapp/edit_profile.html", context)


@login_required
def start_chat(request, other_user_id):
    if request.method == "POST":
        user1 = User.objects.get(pk=request.user.id)
        user2 = User.objects.get(pk=other_user_id)

        selected_chat_id = check_chat(request.user.id, other_user_id)
        selected_chat = Chat.objects.get(pk=selected_chat_id)
        message_text = request.POST.get('message-field') 

        new_message = Message.objects.create(
            sender = user1,
            receiver = user2,
            content = message_text,
            chat = selected_chat
        )        
        return HttpResponseRedirect(reverse("chats"))


def check_chat(user1_id, user2_id):
    user1 = User.objects.get(pk=user1_id)
    user2 = User.objects.get(pk=user2_id)
    existing_chat = Chat.objects.filter(owner=user1, members=user2) | Chat.objects.filter(owner=user2, members=user1)

    if existing_chat.exists():
        chat_id = existing_chat.first().id 
        return chat_id
    else:
        chat_id = create_chat(user1_id, user2_id)
        return chat_id


def create_chat(user1_id, user2_id):
    user1 = User.objects.get(pk=user1_id)
    user2 = User.objects.get(pk=user2_id)
    chat_name = f"{user1.username} and {user2.username}"
    new_chat = Chat.objects.create(owner=user1, name=chat_name)
    new_chat.members.add(user2)
    return new_chat.id


@login_required
def chats(request):
    current_user = request.user
    chat_list = Message.get_chat_list(current_user)
    chats = Chat.objects.filter(models.Q(owner=current_user) | models.Q(members=current_user))
    context = {
        "username": request.user.username,
        "latest_chats": chat_list,
        "chats": chats
    }
    return render(request, "chatapp/base.html", context)


def chat_preview(request):
    current_user = request.user
    chat_list = Message.get_chat_list(current_user)
    context = {
        "username": request.user.username,
        "latest_chats": chat_list,
    }
    return render(request, "chatapp/chat_preview.html", context)


def chat_history(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    chat_history = Message.objects.filter(chat=chat).order_by('timestamp')
    chat_data = [
        {'sender': message.sender.username,
         'receiver': message.receiver.username,
         'content': message.content, 
         'timestamp': message.timestamp.strftime('%d %b %Y %I:%M %p')}          
         for message in chat_history
         ]
    return JsonResponse({'chat_history': chat_data})


def send_message(request, chat_id):
    selected_chat = get_object_or_404(Chat, pk=chat_id)
    current_user = request.user

    if current_user == selected_chat.owner:
        other_party = selected_chat.members.first()
    else:
        other_party = selected_chat.owner

    if request.method == 'POST':
        data = json.loads(request.body)
        message_content = data.get('content')
        chat_id = data.get('chat_id')
        new_message = Message.objects.create(
            sender = current_user,
            receiver = other_party,
            content = message_content,
            chat = selected_chat
        )        
        return JsonResponse({'success': 'Message sent'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    


''' Login, logout, register views'''
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("chats"))
        else:
            return render(request, "chatroom/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chatroom/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("landing"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chatroom/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chatroom/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("chats"))
    else:
        return render(request, "chatroom/register.html")
