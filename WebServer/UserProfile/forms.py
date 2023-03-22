__author__ = 'varun'
from django import forms


class UserProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    old_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    repeat_new_password = forms.CharField(widget=forms.PasswordInput, required=False)