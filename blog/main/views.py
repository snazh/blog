from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import *
from .models import *
from .utils import *


def index(request):
    context = {
        'title': "Home",
    }
    return render(request, 'main/index.html', context=context)


def about(request):
    context = {
        'title': "About us",
    }
    return render(request, 'main/about.html', context=context)


def login(request):
    context = {
        'title': "Login",
    }
    return render(request, 'main/new_login.html', context=context)


def contacts(request):
    context = {
        'title': "Contacts",
    }
    return render(request, 'main/contacts.html', context=context)


class MainPosts(DataMixin, ListView):
    model = Post
    template_name = 'main/posts.html'
    context_object_name = 'publications'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Posts")  # словарь для передачи данных с "миксина"
        return {**context, **c_def}

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class MainCategory(DataMixin, ListView):
    model = Post
    template_name = 'main/posts.html'
    context_object_name = 'publications'

    allow_empty = False  # отображение ошибки если в массив пустой

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Category: {context['publications'][0].cat}",
                                      cat_selected=context['publications'][0].cat_id)
        return {**context, **c_def}


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'main/post_details.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return {**context, **c_def}

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        try:
            evaluation_entry = EvaluationController.objects.get(user=self.request.user, post=post)
        except EvaluationController.DoesNotExist:
            evaluation_entry = None

        if evaluation_entry is None:
            if 'like' in request.POST:
                post.like_post(True)
                EvaluationController.objects.create(user=self.request.user, post=post, evaluation='like')
            elif 'dislike' in request.POST:
                post.dislike_post(True)
                EvaluationController.objects.create(user=self.request.user, post=post, evaluation='dislike')
        else:
            evaluation_entry.delete()
            if 'like' in request.POST:
                post.like_post(False)
                EvaluationController.objects.create(user=self.request.user, post=post, evaluation='like')
            elif 'dislike' in request.POST:
                post.dislike_post(False)
                EvaluationController.objects.create(user=self.request.user, post=post, evaluation='dislike')

        return redirect('main:post_detail', post_slug=post.slug)


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/add_post.html'
    login_url = reverse_lazy('login')  # redirect if user is not authorized
    raise_exception = True  # access is forbidden

    def form_valid(self, form):
        form.instance.user = self.request.user
        titleSlug = form.instance.title.replace(' ', '').lower()
        form.instance.slug = f"{self.request.user}-{titleSlug}"
        form.instance.like = 0
        form.instance.dislike = 0
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Post")
        return {**context, **c_def}


def add_comment(request):
    publications = Post.objects.all()
    categories = Category.objects.all()
    context = {
        'publications': publications,
        'categories': categories,
        'title': "",

    }
    return render(request, 'main/post_details.html', context=context)


def pageNotFound(request, exception):
    return render(request, 'main/ErrorPage.html')


'''
def add_post(request):
    if request.method == 'POST':  # для того чтобы данные оставались после отправки
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = AddPostForm()

    context = {
        'title': 'Add page',
        'form': form,
    }
    return render(request, 'main/add_post.html', context=context)

def posts(request):
    publications = Post.objects.all()
    categories = Category.objects.all()
    context = {
        'publications': publications,
        'categories': categories,
        'title': "Posts",
        'cat_selected': 0,
    }
    return render(request, 'main/posts.html', context=context)

def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    context = {
        'post': post,
        'title': "Post details",
        'cat_selected': post.cat_id,

    }

    return render(request, 'main/post_details.html', context=context)


def show_category(request, cat_id):
    publications = Post.objects.filter(cat_id=cat_id)
    categories = Category.objects.all()

    if len(publications) == 0:
        raise Http404()

    context = {
        'publications': publications,
        'categories': categories,
        'title': 'Categories',
        'cat_selected': cat_id,
    }

    return render(request, 'main/posts.html', context=context)
'''
