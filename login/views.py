from django.contrib.auth.views import LoginView
# from django.forms import Form
# from django import forms
# from django.forms import ModelForm
# from .models import Team


# class CommentForm(Form):
#     name = forms.CharField(label='Your name')
#     url = forms.URLField(label='Your website', required=False)
#     comment = forms.CharField()


# class TeamForm(ModelForm):
#     class Meta:
#         model = Team
#         fields = '__all__'


class Register(LoginView):
    pass
