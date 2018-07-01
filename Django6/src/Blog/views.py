from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from .models import *
from django.contrib.auth.decorators import login_required
from Blog.forms import *
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
#재네릭뷰 : 장고에서 제공하는 여러가지 기능으로 나눈 뷰 클래스
# Create your views here.
#클래스 기반의 뷰
#class 뷰이름(기능별 뷰클래스):
#LlistView : 특정 객체의 목록을 다루는 기능을 가진 뷰 클래스
class index(ListView):
    template_name = "Blog/templates/index.html"
    model = Post
    context_object_name = 'list'
    paginate_by = 5


def detail(request, post_id):
    obj = get_object_or_404(Post,pk=post_id)
    return render(request, 'blog/templates/detail.html',{'post' : obj})


@login_required
def posting(request):
    if request.method == "GET":
        form = PostForm
        return render(request,"blog/templates/posting.html",{"form":form})
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            #Image 캑체 생성및 저장
            for f in request.FILES.getlist('images'):
                image = Image(post=obj, image=f)
                image.save()
            for f in request.FILES.getlist('files'):
                file = File(post=obj,file=f)
                file.save()
                
                
            return HttpResponseRedirect( reverse('Blog:detail',args=(obj.id) ) )
        
        
        
def searchP(request):
    q = request.GET.get('q','')
    type = request.GET.get('type','0')
    if type=='0':
        list = Post.objects.filter(headline__contains=q)
        return render(request,"Blog/templates/searchP.html",{'list':list})
    elif type =='1':
        user = User.objects.get(username = q )
        list = Post.objects.filter(author = user)
        return render(request, "Blog/templates/searchP.html",{'list':list})