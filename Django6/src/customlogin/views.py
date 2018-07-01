from django.shortcuts import render
from .forms import *
from django.contrib.auth import login, authenticate
from urllib.request import HTTPRedirectHandler
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect
# Create your views here.
def signup(request):
    if request.method == "GET":
        form = UserForm()
        return render(request,"customlogin/templates/signup.html",{'form' :form})
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                    
                #new_user = User.objects.create_user(**form.cleaned_data)#**딕션어리 형태로 여러가지 형태를 넣을수 있음 폼객체에 저장된 값을 꺼낼대 사용
                new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
                #login(request,new_user) : 해당요청을 보낸 클라이언트가 user객체로 로그인하는 작업을 함
                login(request,new_user)
                return HttpResponseRedirect(reverse('vote:index'))
            else :
                error = "비밀변호가 맞지 않음"
        else:
            error = "유요하지 않은 값이 입력됨"
        return render(request,"customlogin/templates/signup.html",{'form' :form, 'error' :error})
def signin(request):
    if request.method =="GET":
        form = LoginForm()
        return render(request,"customlogin/templates/signin.html",{'form' :form})
    elif request.method =="POST":
            form = LoginForm(request.POST)
            username1 = request.POST.get('username')
            password1 = request.POST.get('password')
            user = authenticate(username=username1,password=password1)
            #(값,변수) is 타입 : (값,변수)가 타입과 동일한지 True,False반환
            if user is not None:
                login(request, user)#로그인
                return HttpResponseRedirect( reverse("vote:index") )
            else :#id와 비번 엇는경우
                error="아이디 또는 비밀번호가 틀렸습니다."
    return render(request, "customlogin/templates/signin.html",{'form' :form, 'error' :error})
            