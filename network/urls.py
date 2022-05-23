from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("following/<int:user_id>", views.following, name="following"),
    path("edit_entry/<int:post_id>", views.edit, name="edit"),
    path("delete_entry/<int:post_id>", views.delete, name="delete"),
    path("user_following/<int:user_id>", views.user_following, name="user_following"),
    path("user_follwers/<int:user_id>", views.user_followers, name="user_followers"),
    # API Routes
    path("like_entry", views.like, name="like"),
]
