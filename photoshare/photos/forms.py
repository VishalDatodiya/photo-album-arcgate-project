from django.forms import ModelForm

from .models import Photo, User
from django.contrib.auth.forms import UserCreationForm


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
        exclude = ['user',]


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email', 'bio', 'avatar', 'password1','password2']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','name', 'email','bio', 'avatar']

    