'''
Created on 2018. 6. 23.

@author: soooo
'''
from django.forms.models import ModelForm
from . import models
#form : HTML코드에서 사용할 입력방식을 모델클래스에 맞게 자동으로 만들어주는 기능 or 커스텀  입력양식을 만드는 기능을 제공함
#class 폼클래스면(ModelForm): 모델 클래스에 관한 폼을 정의
#class 폼클래스명(Form): HTML에서 사용할 커스텀 폼을 정의

class QuestionForm(ModelForm):
    class Meta: #Meta클레스 ㅓㅇ의를 통해 모델 클래스에 관한 정보 입력
        #model : 모델 클래스명(해당폼이 매칭할 모델클래스 작성)
        #fields or exclude 중 1개 사용
        #fields : 해당 모델폼을 통해 클라이언트가 입력할수 있는 데이터 종류를 작성
        #exclude : 모델클래스의 속성중 명시한 속성을 제외한 속성 사용자 작성
        model = models.Question
        fields = ['question_text']
        #exclude = ['pub_date']  = 속성 제외한 모든 속성을 사용자가 지정
        
        
        
        
        #choice에 대한 모델폼 정의
        #'choice_text', 'question' 속성자만 사용자가 입력하도록 허용
class ChoiceForm(ModelForm):
    class Meta:
        model = models.Choice
        fields = ['choice_text']
        #exclude = ['votes']
        