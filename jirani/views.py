from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
from .forms import *
from peewee import DoesNotExist


# Create your views here.
# def welcome(request):
#     return HttpResponse('Welcome to the Keller Jirani')


@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    hood_name = current_user.profile.hood
    if current_user.profile.hood is None:
        # hoods = Hood.objects.all()
        return redirect('communities')

    try:
        posts = Post.objects.all()
        form = NewComment(instance=request.user)
        comments = Comment.objects.all()
    except DoesNotExist:
        raise Http404()

    return render(request, 'index.html', {'posts': posts, 'hood_name': hood_name, 'comment_form': form, 'comm': comments})


def communities(request):
    current_user = request.user
    hoods = Hood.objects.all()

    return render(request, 'communities.html', {'hoods': hoods})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    hood_name = current_user.profile.hood
    profile = Profile.objects.get(user=current_user)
    print(profile)
    # profile = Profile.objects.filter(user=request.user.id)
    businesses = Business.objects.filter(owner=current_user)

    return render(request, 'profile.html', {'profile': profile, 'businesses': businesses,
                                            'hood_name': hood_name})


@login_required(login_url='/accounts/login/')
@transaction.atomic
def update(request):
    # current_user = User.objects.get(pk=user_id)
    current_user = request.user
    hood_name = current_user.profile.hood
    if request.method == 'POST':
        user_form = EditUser(request.POST, request.FILES, instance=request.user)
        profile_form = EditProfile(request.POST, request.FILES, instance=current_user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
        return redirect('profile')

    else:
        user_form = EditUser(instance=request.user)
        profile_form = EditProfile(instance=current_user.profile)
    return render(request, 'update_profile.html', {
        "user_form": user_form,
        "profile_form": profile_form,
        'hood_name': hood_name
    })


def comment(request, id):
    post = Post.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        comm = NewComment(request.POST)
        if comm.is_valid():
            comment = comm.save(commit=False)
            comment.commentator = request.user
            comment.comment_post = post
            comment.save()
            return redirect('index')
    return redirect('index')


@login_required(login_url='/accounts/login/')
def hood(request, hood_id):
    current_user = request.user
    hood_name = current_user.profile.hood
    # if current_user.profile.hood is None:
    #     return redirect('update')
    # else:
    hood = Post.get_hood_posts(id=hood_id)
    comments = Comment.objects.all()
    form = NewComment(instance=request.user)

    return render(request, 'hood.html',
                  {'hood': hood, 'hood_name': hood_name, 'comments': comments, 'comment_form': form})


@login_required(login_url='/accounts/login/')
def choosehood(request):
    return render(request, 'choosehood.html')


@login_required(login_url='/accounts/login/')
def business(request, id):
    current_user = request.user
    businessing = Business.objects.get(id=id)
    hood_name = current_user.profile.hood

    return render(request, 'business.html', {'business': businessing, 'hood_name': hood_name})


@login_required(login_url='/accounts/login/')
def search(request):
    current_user = request.user
    hood_name = current_user.profile.hood
    if 'business' in request.GET and request.GET["business"]:
        search_query = request.GET.get("business")
        searched_business = Business.get_business(name=search_query)
        print(search_query)
        message = f"{search_query}"
        print(searched_business)

        return render(request, 'search.html', {"message": message, "businesses": searched_business})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message,
                                               'hood_name': hood_name})


@login_required(login_url='/accounts/login/')
def newbiz(request):
    current_user = request.user
    hood_name = current_user.profile.hood
    if request.method == 'POST':
        addBizForm = AddBusiness(request.POST, request.FILES)
        if addBizForm.is_valid():
            bizform = addBizForm.save(commit=False)
            bizform.owner = current_user
            bizform.locale = current_user.profile.hood
            bizform.save()
        return redirect('index')

    else:
        addBizForm = AddBusiness()
    return render(request, 'add_business.html', {"addBusinessForm": addBizForm,
                                                 'hood_name': hood_name})


@login_required(login_url='/accounts/login/')
def newpost(request):
    current_user = request.user
    hood_name = current_user.profile.hood
    hood = request.user.profile.hood
    if request.method == 'POST':
        newPostForm = NewPost(request.POST, request.FILES)
        if newPostForm.is_valid():
            new_post = newPostForm.save(commit=False)
            new_post.poster = request.user
            new_post.hood = hood
            new_post.save()
        return redirect('index')

    else:
        newPostForm = NewPost()
    return render(request, 'newpost.html', {"newPostForm": newPostForm,
                                            'hood_name': hood_name})


@login_required(login_url='/accounts/login/')
def newhood(request):
    current_user = request.user
    hood_name = current_user.profile.hood
    if request.method == 'POST':
        NewHoodForm = NewHood(request.POST)
        if NewHoodForm.is_valid():
            hoodform = NewHoodForm.save(commit=False)
            hoodform.admin = current_user
            current_user.profile.hoodpin = True
            hoodform.save()
            print('saved')

            # request.session.modified = True
            # current_user.profile.hood = hoodform.id
        # return redirect('profilehood',hoodform.name)
        return redirect('index')


    else:
        NewHoodForm = NewHood()
    return render(request, 'newhood.html', {"newHoodForm": NewHoodForm,
                                            'hood_name': hood_name})


def profilehood(request, name):
    current_user = request.user
    hood_name = current_user.profile.hood
    hoodform = Hood.objects.get(name=name)
    current_user.profile.hood = hoodform.id
    current_user.profile.hoodpin = True

    return redirect('index')


def join(request, id):
    current_user = request.user
    hood_name = current_user.profile.hood
    hood = Hood.objects.get(id=id)
    current_user.profile.hood = hood
    current_user.profile.save()

    return redirect('index')


def exit(request, id):
    current_user = request.user
    # hood_name = current_user.profile.hood
    # hood = Hood.objects.get(id=id)
    current_user.profile.hood = None
    current_user.profile.save()

    return redirect('index')
