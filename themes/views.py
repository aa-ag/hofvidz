from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Theme

def home(request):
    '''
    Renders home page, before and after login/singup
    '''
    return render(request, 'themes/home.html')


def dashboard(request):
    '''
    Renders dashboard page, after login/singup
    '''
    return render(request, 'themes/dashboard.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateTheme(generic.CreateView):
    model = Theme
    fields = ['title', 'description']
    template_name = 'themes/create_theme.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateTheme, self).form_valid(form)
        return redirect('home')


class DetailTheme(generic.DetailView):
    model = Theme
    template_name = 'themes/detail_theme.html'


class UpdateTheme(generic.UpdateView):
    model = Theme
    template_name = 'themes/update_theme.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('dashboard')


class DeleteTheme(generic.DeleteView):
    model = Theme
    template_name = 'themes/delete_theme.html'
    success_url = reverse_lazy('dashboard')