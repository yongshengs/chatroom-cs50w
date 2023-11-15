from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("chats", views.chats, name="chats"),
    path("members", views.members, name="members"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/edit/<int:user_id>", views.edit_profile, name="edit_profile"),
    path('get_chat_history/<int:chat_id>/', views.chat_history, name='get_chat_history'),
    path('get_chat_previews/', views.chat_preview, name='get_chat_preview'),
    path('send_message/<int:chat_id>', views.send_message, name='send_message'),
    path('start_chat/<int:other_user_id>/', views.start_chat, name='start_chat'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)