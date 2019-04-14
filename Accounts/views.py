from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import get_user_model
import os
import subprocess
from .models import Github_model, User
import requests
from django.contrib import messages 
import datetime
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class ProfileUserView(DetailView):
	model = get_user_model()
	template_name = 'Accounts/profile_user.html'

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def get_context_data(self, *args, **kwargs):
		context = super(ProfileUserView, self).get_context_data(**kwargs)
		context['object'] = User.objects.get(pk = self.kwargs.get('pk') if self.kwargs.get('pk') else self.request.user.id)
		context['repos'] = Github_model.objects.filter(user = self.kwargs.get('pk') if self.kwargs.get('pk') else self.request.user.id).order_by('-stars', 'name')[:5]
		return context

class CreateUserView(AnonymousRequiredMixin, CreateView):
	model = get_user_model()
	fields = ['email', 'name']
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
	next_page = reverse_lazy('Accounts-login')

class UpdateUserView(LoginRequiredMixin, UpdateView):
	model = get_user_model()
	success_url = reverse_lazy('Accounts-login')
	fields = ['email', 'name', 'github_name','image', ]
	template_name = 'Accounts/update_user.html'

	def form_valid(self, form,  *args, **kwargs):
		# Remove old image
		image = self.request.FILES.get('image')
		if image:
			image_old = (self.image)[1:]

			if not image_old == "media/profile/default.jpg":
				try:
					os.remove(image_old)
				except FileNotFoundError as e:
					print(e)

		return super(UpdateUserView, self).form_valid(form, *args, **kwargs)


	def get_object(self, queryset=None):
		user = self.request.user 
		self.image = user.image.url 
		return user

class DeleteUserView(LoginRequiredMixin, DeleteView):
	model = get_user_model()
	template_name = 'Accounts/delete_user.html'
	success_url = reverse_lazy('Accounts-login')

	def delete(self, *args, **kwargs):
		os.remove((self.request.user.image.url)[1:])
		return super(DeleteUserView, self).delete(self,*args, **kwargs)

	def get_object(self, queryset=None):
		user = self.request.user 
		return user

@login_required
def Check_git_hub(request):
	print(request.user.github_name)
	if request.user.github_name:

		try:
			req = requests.get(f"https://api.github.com/users/{request.user.github_name}/repos")
			json = req.json()
			json[0]['description']

			for i in Github_model.objects.filter(user = request.user):
				i.delete()

			for i in json:
				crtd = i['created_at']
				created_at = datetime.datetime.strptime(crtd, "%Y-%m-%dT%H:%M:%SZ")

				Github_model.objects.create(user=request.user, name=i['name'], 
				url=i['svn_url'], discription=i['description'] or '', languages=i['language'] or '',
				created_at=created_at, stars=i['stargazers_count'])
		except KeyError as e:
			messages.error(request, "You are out of requests for this hour")
			print(e)

	else:
		messages.error(request, "User has not set github name")

	return redirect(reverse_lazy('Accounts-profile', args=[request.user.id,]))