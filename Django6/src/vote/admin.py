#관리자 사이트에서 모델클래스를 조회 삽입 삭제 수정 하고자 할때 쓰는 파일

from django.contrib import admin
#해당 파일에서 모델클래스를 알아야되므로 from~import 사용
from .models import Question, Choice #form .models import*
#관리자 페이지에서 효과적으로 객체정보를 볼수있는 ModelAdmin클래스 상속
class ChoiceAdmin(admin.ModelAdmin):
    fields = ['choice_text','votes','question']
    list_display = ('choice_text','votes','question')
#admin.site.register(클래스명)
#해당모델클래스를 관리자 사이트에 등록
# Register your models here.

admin.site.register(Question)# ��Ŭ������ ������ ���������� �� �� �ֵ��� ���
admin.site.register(Choice,ChoiceAdmin)