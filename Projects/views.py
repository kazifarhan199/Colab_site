from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Projects_model
from django.db.models import Q
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from django.contrib import messages 
from django.contrib.auth import get_user_model
from Accounts.models import Github_model
from django.shortcuts import render

def Home_Page(request):
    return render(request, "index.html")

class Projects_List(ListView):
    model = Projects_model
    template_name = 'Projects/list_view.html'

    def get_queryset(self):
        context = self.model.objects.filter(published=True).order_by('-id')
        return context

    def get_context_data(self, *args, **kwargs):
        context =  super(Projects_List, self).get_context_data(**kwargs)
        context['users'] = get_user_model().objects.all().order_by('id')
        return context

class Projects_Dashboard_List(LoginRequiredMixin, ListView):
    model = Projects_model
    template_name = 'Projects/dashboard_list_view.html'

    def get_queryset(self):
        context = self.model.objects.filter(user=self.request.user).order_by('-id')
        return context

class Projects_detail_view(DetailView):
    model = Projects_model
    template_name = 'Projects/detail_view.html'

class Projects_create_view(LoginRequiredMixin ,CreateView):
    model = Projects_model
    fields = ['title', 'body', 'published']  
    template_name = 'Projects/create_view.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Projects_create_view, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Projects-dashboard')

class Projects_delete_view(LoginRequiredMixin, DeleteView):
    model = Projects_model
    template_name = 'Projects/delete_view.html'
    success_url = reverse_lazy('Projects-list')		


class Projects_Dashboard_Edit(LoginRequiredMixin, UpdateView):
    model = Projects_model
    template_name = 'Projects/create_view.html'
    fields = ['title', 'body', 'published']   

    def get_success_url(self):
        url = self.request.META['HTTP_REFERER'].rsplit('/',1)[1]
        return reverse_lazy('Projects-detail', args=[url,])

    def form_valid(self, form, *args, **kwargs):
        if form.instance.user != self.request.user:
            form.errors["error"]="Can't edit otherse title"
            return super(Projects_Dashboard_Edit, self).form_invalid(form, *args, **kwargs)

        return super(Projects_Dashboard_Edit, self).form_valid(form)
