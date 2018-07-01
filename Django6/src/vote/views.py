from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
#reverse(문자열 args=튜플)
#문자열에 해당하는 url 별침을 찾고, 매개변수가 필요한 URL일경우
#args 매개 변수에 있는값을 튜플로 자동으로 매김

from .models import Question, Choice
from django.http.response import HttpResponseRedirect

import datetime#파이썬 내장 모듈 시간 확인
from . forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#views.py : 내부적으로 동작할때 행동들을 정의
#HTML 파일 전달 검색 등록 삭제 수정
#함수 or 클래스 형태로 뷰 구분
#함수형태로 구현시 반드시 첫번째 매개변수로 request 사용
# Create your views here.
#�Լ� or Ŭ����
def index(request):
    print("index 함수호출")
    #question ��ü ã��
    #��Ŭ����.objects.all() : �ش� ��ÿ Ŭ������ ����� ��� ��ü ����
    list = Question.objects.all()
    #���ø��� ���� �����ϱ�
    #render(request, html���� ��� , html���Ϸ� ������ ������-������)
    return render(request,"vote/templates/index.html",{'question_list':list})
    
def detail(request, question_id):
    #get_object_or_404 모델클래스에 id 값으로 객체 1개를 반환 함수
    #만약 객체를 못찾는 경우 클라이언트에게 404에러 메시지를 전달
    p = get_object_or_404(Question, pk = question_id)
    return render(request,"vote/templates/detail.html",
                  {'question' : p})
    
def vote(request,question_id):
    #request.method : 클라이언트의 요청 방식이 저장된 변수
    #GET POST 문자열과 비교 대소문자 구분O
    if request.method =="POST":
        #request.POST : POST방식으로 들어온 데이터들
        #request.POST.get(문자열) : POST방식으로 들이온 데이터 중
        #name 속성의 값이 문자열과 같은 데이터 추출
        #get 함수가 반환하는 데이터는 무조건 문자열
        id = request.POST.get('choice')
        obj = get_object_or_404(Choice,pk=id)
        obj.votes += 1
        obj.save()#모델 클래스의 객체.save() : 변동 사항 저장
        #튜플을 만들때 요소순위가 한개면 사칙연산에 사용ㅎ는 우선순위 괄호로 판단함.
        #때문에 튜플 요소 개수가 한개일경우 쉼표 입력
        return HttpResponseRedirect( reverse('vote:result', args=( question_id, ) )  )
        #redirect(문자열) : 문자열에 해당하는 URL주소로 변경
        #return redirect('/result/%s/' % (question_id))
    
def result(request,question_id):
    #모델클래스.objects.get(조건) : 조건에 밪는 객체를 1개 찾아 반환
    data = Question.objects.get(id=question_id)
    return render(request, "vote/templates/result.html",
                  {'obj' :data} )
@login_required # 그뷰를 호출하기 전에 함수를 호출
def registerQ(request):
    if request.method =="GET":
        form = QuestionForm()# <- 객체 생성,사용하는 속성들이 공란으로 되어있음
        return render(request,"vote/templates/registerQ.html",{'form' : form} )
    elif request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            #name = request.POST.get('question_text')
            #obj = Question()
            #obj.question_text = name
            user = User.objects.get(username=request.user.get_username())
            obj.pub_date = datetime.datetime.now()
            obj.author=user
            obj.save()
            return HttpResponseRedirect(reverse('vote:detail',args=(obj.id, ) ) )
        else:
            #템플릿으로 form 전달하면 사용자가 이전에 작성한 내용이 들어있는 상태로 전달함
            return render(request, "vote/templates/registerQ.html",{'form' : form, 'error' : "입력이 잘못됬습니다."})
@login_required
def deleteQ(request, question_id):
    
    #pk = id
    obj = get_object_or_404(Question, pk = question_id)
    if obj.author.username != request.usr.get_username():
        return render(request,"vote/templates/error.html",{'error':"잘못된 접근 입니다.",'returnURL' : reverse('vote:detail',args=(question_id,) )} )
    
    
    
    
    obj.delete() # 해당 객체를 데이터베이스에서 삭제
    return HttpResponseRedirect(reverse('vote:index'))
@login_required
def deleteC(request, choice_id):
    obj = get_object_or_404(Choice, pk = choice_id)
    if request.user.get_username() != obj.question.author.username:
        return render(request,"vote/templates/error.html",{'error':"잘못된 접근 입니다.",'returnURL' : reverse('vote:detail',args=(obj.question_id,) )} )
    id = obj.question.id
    obj.delete()
    return HttpResponseRedirect(reverse("vote:detail", args=(id,) ))
    
    
    
    
    pass


def registerC(request, question_id):
    obj = get_object_or_404(Question, pk = question_id)
    #해당 질문을 쓴 글쓴이 이르과 로그인된 유저의 이름을 비교
    if request.user.get_username() != obj.author.username:
        return render(request,"vote/templates/error.html",{'error':"본인이 작성한 글이 아님니다.",'returnURL':reverse('vote:detail', args=(question_id,) ) })
    if request.method == "GET":
        #폼객체 생성
        form = ChoiceForm()
        return render(request,"vote/templates/registerC.html",{'form' : form, 'name': obj.question_text})
        #render함수로 HTML 파일 로드 + 탬플릿에 폼객체 전달
    elif request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            obj1 = form.save(commit=False)
            obj1.question = obj
            obj1.save()
            return HttpResponseRedirect(reverse('vote:detail',args=(obj1.question.id, ) ))
        else:
            return render(request,"vote/templates/registerC.html",{'form' : form, 'error' : "입력에 오류가 있음",'name' : obj.question_text})
@login_required
def updateQ(request, question_id):
    obj = get_object_or_404(Question, pk = question_id)
    #해당 질문을 쓴 글쓴이 이르과 로그인된 유저의 이름을 비교
    if request.user.get_username() != obj.author.username:
        return render(request,"vote/templates/error.html",{'error':"본인이 작성한 글이 아님니다.",'returnURL':reverse('vote:detail', args=(question_id,) ) })
    if request.method == "GET":
        form = QuestionForm(instance = obj)
        return render(request,"vote/templates/updateQ.html", {'form' :form})
    elif request.method == "POST":
        form = QuestionForm(request.POST,instance=obj)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = datetime.datetime.now()
            question.save()
            return HttpResponseRedirect(reverse("vote:detail", args=(question.id,) ))
        else:
            return render(request,"vote/templates/updateQ.html", {'form' :form, 'error' :"유효하지 안ㅎ는 데이터"})