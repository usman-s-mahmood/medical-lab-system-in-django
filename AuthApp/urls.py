# created manually!
from . import views
from django.urls import path

urlpatterns = [
    path('login', views.login_user, name='auth-login'),
    path('logout', views.logout_user, name='auth-logout'),
    path('register', views.register_user, name='auth-register'),
    path('edit-user', views.edit_user, name='auth-edit-user'),
    path('edit-password', views.edit_password, name='auth-edit-password'),
    path('delete-user', views.delete_user, name='auth-delete-user'),
    path('create-profile', views.create_profile, name='auth-create-profile'),
    path('edit-profile', views.edit_profile, name='auth-edit-profile'),
    path('dashboard', views.user_dashboard, name='auth-dashboard'),
    path('liked-posts', views.liked_posts, name='auth-liked-posts'),
    path('posted-content', views.posted_content, name='auth-posted-content'),
]