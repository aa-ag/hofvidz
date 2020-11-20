from .models import Video
from django import forms
from captcha.fields import CaptchaField

class VideoForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Video
        fields = ['url']
        labels = {'url': 'url'}

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search YouTube')
