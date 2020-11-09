from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import secret
from .models import Theme, Video
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
import urllib
import requests
from django.forms.utils import ErrorList

# GENERAL
def home(request):
    '''
    Renders home page, before and after login/singup
    '''
    recent_themes = Theme.objects.all().order_by('-id')[:3]
    context = {'recent_themes': recent_themes}
    return render(request, 'themes/home.html', context)


@login_required
def dashboard(request):
    '''
    Renders dashboard page, after login/singup
    '''
    current_user = request.user
    themes = Theme.objects.filter(user=current_user.id)
    context = {'themes': themes}
    return render(request, 'themes/dashboard.html', context)


@login_required
def userthemes(request, id):
    '''
    Renders user profile view
    '''
    themes = Theme.objects.filter(id=id)
    context = {'themes': themes}
    return render(request, 'themes/userthemes.html', context)


# REGISTRATION
class SignUp(generic.CreateView):
    '''
    Creates users
    '''
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        '''
        Logs in users right after sign up
        '''
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


# THEMES CRUD OPERATIONS
class CreateTheme(LoginRequiredMixin, generic.CreateView):
    '''
    Creates Themes in database
    '''
    model = Theme
    fields = ['title', 'description']
    template_name = 'themes/create_theme.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateTheme, self).form_valid(form)
        return redirect('dashboard')


class DetailTheme(generic.DetailView):
    '''
    Reads Themes in database
    '''
    model = Theme
    template_name = 'themes/detail_theme.html'


class UpdateTheme(LoginRequiredMixin, generic.UpdateView):
    '''
    Updates Themes in database
    '''
    model = Theme
    template_name = 'themes/update_theme.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        theme = super(UpdateTheme, self).get_object()
        if not theme.user == self.request.user:
            raise Http404
        return theme


class DeleteTheme(LoginRequiredMixin, generic.DeleteView):
    '''
    Deletes Themes in database
    '''
    model = Theme
    template_name = 'themes/delete_theme.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        theme = super(DeleteVideo, self).get_object()
        if not theme.user == self.request.user:
            raise Http404
        return theme


# VIDEO CRUD
@login_required
def add_video(request, pk):
    '''
    Validates url input from users and adds videos to database
    '''
    form = VideoForm()
    search_form = SearchForm()
    theme = Theme.objects.get(pk=pk)

    if not theme.user == request.user:
        raise Http404

    if request.method == 'POST':
        form = VideoForm(request.POST)

        if form.is_valid():
            video = Video()
            video.theme = theme
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={secret.KEY}').json()
                title = response['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detail_theme', pk)
            else:
                errors = form.errors.setdefault('url', ErrorList())
                errors.append('Needs to be a valid YouTube url')

    context = {'form': form, 'search_form': search_form, 'theme': theme}
    return render(request, 'themes/addvideo.html', context)


@login_required
def video_search(request):
    '''
    Accepts user input, searches YouTube & returns results
    '''
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={secret.KEY}').json()
        return JsonResponse(response)
    return JsonResponse({'error': 'something went wrong... please try again'})


class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    '''
    Deletes Videos from database
    '''
    model = Video
    template_name = 'themes/deletevideo.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.theme.user == self.request.user:
            raise Http404
        return video