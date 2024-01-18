import folium
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
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


class MainPosts(DataMixin, ListView):
    model = Post
    template_name = 'main/posts.html'
    context_object_name = 'publications'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Posts")
        return {**context, **c_def}

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class MainCategory(DataMixin, ListView):
    model = Post
    template_name = 'main/posts.html'
    context_object_name = 'publications'

    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Category: {context['publications'][0].cat}",
                                      cat_selected=context['publications'][0].cat_id)
        return {**context, **c_def}


class ShowPost(DataMixin, DetailView, CreateView):
    model = Post
    template_name = 'main/post_details.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = AddCommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        c_def['comments'] = Comment.objects.filter(post=self.get_object())
        return {**context, **c_def}

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        # like dislike system
        try:
            evaluation_entry = EvaluationController.objects.get(user=self.request.user, post=post)

        except EvaluationController.DoesNotExist:
            evaluation_entry = 'zero'

        if evaluation_entry == 'zero':

            if 'like' in request.POST:
                post.like_post(flag=True)
                EvaluationController.objects.create(user=self.request.user, post=post, evaluation='like')
            elif 'dislike' in request.POST:
                post.dislike_post(flag=True)
                EvaluationController.objects.create(user=self.request.user, post=post, evaluation='dislike')
        else:

            if 'like' in request.POST:

                if evaluation_entry.evaluation == 'like':
                    post.like_post(False)
                    EvaluationController.objects.update(user=self.request.user, post=post, evaluation='zero')
                elif evaluation_entry.evaluation == 'dislike':
                    post.dislike_post(False)
                    post.like_post(True)
                    EvaluationController.objects.update(user=self.request.user, post=post, evaluation='like')
                else:
                    EvaluationController.objects.update(user=self.request.user, post=post, evaluation='like')
                    post.like_post(True)
            elif 'dislike' in request.POST:
                if evaluation_entry.evaluation == 'dislike':
                    post.dislike_post(False)
                    EvaluationController.objects.update(user=self.request.user, post=post, evaluation='zero')
                elif evaluation_entry.evaluation == 'like':
                    post.dislike_post(True)
                    post.like_post(False)
                    EvaluationController.objects.update(user=self.request.user, post=post, evaluation='dislike')
                else:
                    EvaluationController.objects.update(user=self.request.user, post=post, evaluation='dislike')
                    post.dislike_post(True)

        return redirect('main:post_detail', post_slug=post.slug)


class AddCommentView(CreateView):
    model = Comment
    form_class = AddCommentForm
    template_name = 'main/add_comment.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        return super().form_valid(form)


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/add_post.html'
    login_url = reverse_lazy('users:login')  # redirect if user is not authorized

    def form_valid(self, form):
        form.instance.user = self.request.user
        counter = Post.objects.filter(user=self.request.user).count()+1

        form.instance.slug = f"{self.request.user}-post{counter}"
        form.instance.like = 0
        form.instance.dislike = 0
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Post")
        return {**context, **c_def}


def map_view(request):
    title = 'Map'
    form = folium.Figure(height=1000, width=1100)
    m = folium.Map(location=[-0.43, 0.32], tiles="openstreetmap", zoom_start=2.2, min_zoom=2,
                   max_bounds=True).add_to(form)
    for branch in Search.objects.filter(active=True):
        folium.Marker([branch.lng, branch.lat], tooltip='Click for more', popup=branch.name).add_to(m)

    # Get HTML Representation of Map Object
    map_html = m._repr_html_()

    context = {
        'title': title,  # Corrected title assignment
        'map': map_html
    }
    return render(request, 'main/map.html', context=context)


def custom_404(request, exception):
    return render(request, 'main/ErrorPage.html', status=404)
