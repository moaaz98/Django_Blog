from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, JsonResponse
from .models import Article
from .forms import ArticleForm, SignupForm, SigninForm
from django.db.models import Q

# Create your views here.

###### Authentication ######

# signup view
def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.set_password(user_obj.password)
            user_obj.save()
            login(request, user_obj)
            return redirect('article-list')
    context = {
        "signup_form": form,
    }
    return render(request, 'signup.html', context)

# Sign in View
def signin(request):
    form = SigninForm()
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            my_username = form.cleaned_data['username']
            my_password = form.cleaned_data['password']
            user_obj = authenticate(username=my_username, password=my_password)
            if user_obj is not None:
                login(request, user_obj)
                return redirect('article-list')
    context = {
        "signin_form": form,
    }
    return render(request, 'signin.html', context)

# Signout View
def signout(request):
    logout(request)
    return redirect('signin')

# bad access
def no_access(request):
    return render(request, 'no_access.html')

######### List and Detail Views #######
#list view
def article_list(request):
    articles = Article.objects.all()

    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(author__username__icontains=query)
            ).distinct()

    context = {
        "article_objects": articles,
    }
    return render(request, 'list.html', context)

#detail view
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)

    context = {
        "article_object": article,
    }
    return render(request, 'detail.html', context)


######## CRUD ########
#creat view
def article_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES or None)
        if form.is_valid():
            article_obj = form.save(commit=False)
            article_obj.author = request.user
            article_obj.save()
            return redirect('article-list')
    context = {
        "article_form": form,
    }
    return render(request, 'create.html', context)

#update view
def article_update(request, article_id):
    article = Article.objects.get(id=article_id)
    if not (article.author == request.user or request.user.is_staff):
        # raise Http404
        return redirect('no_access')
    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES or None, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article-list')
    context = {
        "article_form": form,
        "article_obj":article,
    }
    return render(request, 'update.html', context)
#delete view
def article_delete(request, article_id):
    Article.objects.get(id=article_id).delete()
    return redirect('article-list')
