from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class RegisterationForm(UserCreationForm):
    contact_number = forms.CharField(max_length=20)
    IAM_CHOICES = [
        ('agent', 'AGENT'),
        ('buyer', 'BUYER'),
        ('owner', 'OWNER'),
        ('builder', 'BUILDER'),
    ]

    iam_name = forms.CharField(label='What is your iam choice?', widget=forms.Select(choices=IAM_CHOICES))


    class Meta:
        model = User
        fields = ('username','contact_number',  'password1', 'password2', )



