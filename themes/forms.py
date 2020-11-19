from .models import Video
from django import forms
from captcha.fields import ReCaptchaField


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['url']
        labels = {'url': 'url'}
        captcha = ReCaptchaField()

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search YouTube')
