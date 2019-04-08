from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import get_user_model

class ProfileUserView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'Accounts/profile_user.html'

    def get_object(self, queryset=None):
        user = self.request.user 
        return user

class CreateUserView(AnonymousRequiredMixin, CreateView):
	model = get_user_model()
	fields = ['email', 'username']
	template_name = 'Accounts/create_user.html'
	success_url = reverse_lazy('Accounts-login')

	def form_valid(self, form,  *args, **kwargs):
		email = self.request.POST.get('email').lower()
		password1 = self.request.POST.get('password1')
		password2 = self.request.POST.get('password2')

		if password1 != password2:
			form.errors["error"]="Password and Re-Password don't match"
			return super(CreateUserView, self).form_invalid(form, *args, **kwargs)

		if get_user_model().objects.filter(email=email).exists():
			form.errors["error"]="A user with that email already exists."
			return super(CreateUserView, self).form_invalid(form, *args, **kwargs)

		form.instance.set_password(password1)

		return super(CreateUserView, self).form_valid(form, *args, **kwargs)
    
class LoginUserView(AnonymousRequiredMixin, LoginView):
    template_name = 'Accounts/login.html'

class LogoutUserView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'
    next_page = reverse_lazy('Projects-list')
    success_url = reverse_lazy('Projects-list')


class UpdateUserView(LoginRequiredMixin, UpdateView):
	model = get_user_model()
	success_url = reverse_lazy('Accounts-login')
	fields = ['email', 'username']
	template_name = 'Accounts/update_user.html'

	def get_object(self, queryset=None):
		user = self.request.user 
		return user

	def form_valid(self, form,  *args, **kwargs):
		email = self.request.POST.get('email').lower()
		if get_user_model().objects.filter(email=email).exists():
			form.errors["error"]="A user with that email already exists."
			return super(CreateUserView, self).form_invalid(form, *args, **kwargs)
		return super(CreateUserView, self).form_valid(form, *args, **kwargs)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'Accounts/delete_user.html'
    success_url = reverse_lazy('Accounts-login')
    
    def get_object(self, queryset=None):
        user = self.request.user 
        return user
