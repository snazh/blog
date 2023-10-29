from django.contrib.auth import logout
from django.http import Http404
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from .forms import RegistrationForm, LoginForm, UpdateProfileForm
from .models import UserProfile
from .utils import DataMixin


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

        title = self.get_user_context(title="Profile")
        return {**context, **title}


class UpdateProfileView(DataMixin, View):
    template_name = 'users/update_profile.html'

    def get(self, request, *args, **kwargs):
        # Fetch user profile using ORM
        profile = UserProfile.objects.get(user=request.user)

        # Populate form with user profile data
        form = UpdateProfileForm(instance=profile)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES)

        if form.is_valid():
            # Update user profile using ORM
            profile = UserProfile.objects.get(user=request.user)
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.bio = form.cleaned_data['bio']
            profile.avatar = form.cleaned_data['avatar']
            profile.save()

            # Redirect to a success page
            return reverse_lazy('main:success_reg')

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_user_context(title="Update profile")
        return {**context, **title}


def logout_user(request):
    logout(request)
    return redirect('users:login')
