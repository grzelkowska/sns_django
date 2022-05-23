from tempfile import TemporaryFile
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Like, Follow


def index(request):
    all_posts = Post.objects.all().order_by('-created_date')
    full_posts = []
    for post in all_posts:
        like_dict = count_like(post.id, request.user.id)
        full_posts.append({
            'id': post.id,
            'entry': post.entry,
            'creator': post.creator,
            'created_date': post.created_date,
            'image': post.image,
            'num_like': like_dict['num_like'],
            'user_like': like_dict['user_like'],
        }) 

    p = Paginator(full_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/index.html", {
        # "all_posts" : all_posts,
        "page_obj": page_obj,
    })


def profile(request, user_id):
    users_posts = Post.objects.filter(creator=user_id).order_by("-created_date")
    full_posts = []
    for post in users_posts:
        like_dict = count_like(post.id, user_id)
        full_posts.append({
            'id': post.id,
            'entry': post.entry,
            'creator': post.creator,
            'created_date': post.created_date,
            'image': post.image,
            'num_like': like_dict['num_like'],
            'user_like': like_dict['user_like'],
        })


    p = Paginator(full_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    self_login = False
    if user_id == request.user.id:
        self_login = True
    
    followers = Follow.objects.filter(following=user_id).count()
    user_follow = False
    if Follow.objects.filter(user=request.user):
        user_follow = True

    following = Follow.objects.filter(user=user_id).count()

    return render(request, "network/profile.html", {
        "user_profile": User.objects.get(id=user_id),
        # "posts": users_posts,
        "self_login": self_login,
        "followers": followers,
        "user_follow": user_follow,
        "following": following,
        "page_obj": page_obj,
    })


def count_like(post_id, user_id):
    like_dict = {
        'num_like': 0,
        'user_like': False,
    }
    try:
        like_dict['num_like'] = Like.objects.filter(post_id=post_id).count()
        try:
            if Like.objects.filter(user_id=user_id, post_id=post_id):
                like_dict['user_like'] = True
        except ObjectDoesNotExist:
            pass
    except ObjectDoesNotExist:
        pass

    return like_dict

@login_required
@csrf_exempt
def like(request):    
    data = json.loads(request.body)
    try:
        like_entry = Like.objects.get(user_id=data['user_id'], post_id=data['post_id'])
        like_entry.delete()
    except ObjectDoesNotExist:
        like_entry = Like(user_id=data['user_id'], post_id=data['post_id'])
        like_entry.save()
    
    return HttpResponse(status=204)


@login_required
def delete(request, post_id):
    if request.method == "POST":
        deleting_post = Post.objects.get(pk=post_id)
        deleting_post.delete()

        return HttpResponseRedirect(reverse('profile', args=(request.user.id, )))


@login_required
def edit(request, post_id):
    if request.method == "POST":        
        editedEntry = request.POST['editedEntry']
        editingPost = Post.objects.get(pk=post_id)
        editingPost.entry = editedEntry
        editingPost.save()
        # return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse('profile', args=(request.user.id, )))


def sort_list(e):
    return e.created_date


def following(request, user_id):
    following_posts_only = True
    following_posts = []
    user = User.objects.get(pk=user_id)
    followers = Follow.objects.filter(user=user).values_list('following', flat=True)

    for person in followers:
        following_posts += Post.objects.filter(creator=person).order_by("-created_date")
    
    following_posts.sort(reverse=True, key=sort_list)

    p = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)


    return render(request, "network/index.html", {
        "following": following_posts_only,
        # "all_posts": following_posts,
        "page_obj": page_obj,
    })


@login_required
def follow(request, user_id):    # user_id=profile_user / loggedin_user=request.user
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        if Follow.objects.filter(user=request.user, following=user):
            following = Follow.objects.filter(user=request.user)
            following.delete()
        else:
            follow_profile = Follow(user=request.user, following=user)
            follow_profile.save()

    return HttpResponseRedirect(reverse("profile", args=(user.id, )))

    
@login_required
def new_post(request):
    if request.method == "POST":
        entry = request.POST['entry']
        user = request.user
        image = request.FILES.get('image')
        new_posting = Post(creator=user, entry=entry, image=image)
        new_posting.save()
    
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")










# def is_liked(user_id):
#     is_liked = False
#     if Like.objects.filter(user=user_id):
#         is_liked = True
    
#     return is_liked

# def count_like(post_id):
#     num_like = Like.objects.filter(post=post_id).count()

#     return num_like