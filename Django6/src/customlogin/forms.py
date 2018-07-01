from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput
class UserForm(ModelForm):
    password2 = forms.CharField(max_length=200,widget=forms.PasswordInput())
    class Meta:
        #django 에서 자동으로 생성된 사용자 모델클래스
        model = User
        #widgets: 각 속성의 입력 스타일 설정
        widgets={
            'password' : forms.PasswordInput(),
            'email' : forms.EmailInput()
            }
        fields = ['username','email','password']
class LoginForm(ModelForm):
    class Meta:
        model = User
        widgets={
            'password':forms.PasswordInput()
            }
        fields=['username','password']