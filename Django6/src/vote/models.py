from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    #models.CharFied  : ���ڼ������� �ִ� ���ڿ��� �����ϴ� Ŭ����
    question_text=models.CharField('질문 제목',max_length=200)
    #��¥�� �ð� ����
    pub_date = models.DateTimeField('생성 일자')
    #��ü�� ǥ���Ҷ� ������ ���ڿ�
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField('답변 제목',max_length=100)
    #�� ǥ�� �޾Ѵ��� ������ �޴°� 0���� �ޱ� ������
    votes = models.IntegerField('투표 수',default=0)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    def __str__(self):
        return self.choice_text