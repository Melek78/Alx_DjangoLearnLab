from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class RegisterView(CreateView):
    template_name = 'blog/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile')
    login_url = 'login'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        messages.success(request, "Profile updated successfully")
        return super().post(request, *args, **kwargs)