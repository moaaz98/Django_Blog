from django import forms
from django.contrib.auth.models import User
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'pic', ]


class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

		widgets = {
			"password": forms.PasswordInput(),
		}

class SigninForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())