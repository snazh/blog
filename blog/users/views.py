from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import RegistrationForm, LoginForm, UpdateProfileForm
from .models import UserProfile
from .utils import DataMixin
from main.models import Post, EvaluationController


class SignUp(DataMixin, CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/new_reg.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_user_context(title="Registration")
        return {**context, **title}


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'users/new_login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_user_context(title="Login")
        return {**context, **title}

    def get_success_url(self):
        return reverse_lazy('main:home')


class ShowUser(DataMixin, DetailView):
    template_name = 'users/profile.html'
    model = UserProfile
    slug_url_kwarg = 'user_slug'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        user_profile = get_object_or_404(self.model.objects.select_related('user'),
                                         slug=self.kwargs[self.slug_url_kwarg])
        if user_profile.user != self.request.user:
            raise Http404("You do not have permission to view this profile.")
        return user_profile

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post_info = {

            'title': 'Profile',
            'posts': Post.objects.filter(user=self.request.user),

        }

        context['posts'] = Post.objects.filter(user=self.request.user)
        return {**context, **post_info}


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UpdateProfileForm
    template_name = 'users/update_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        response = super().form_valid(form)
        print(self.slug_url_kwarg, self.slug_url_kwarg)
        return response

    def get_success_url(self):

        return reverse_lazy('users:user_profile', kwargs={'user_slug': self.object.slug})


def logout_user(request):
    logout(request)
    return redirect('main:home')
