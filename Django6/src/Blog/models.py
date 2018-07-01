from django.db import models
from django.conf import settings
# Create your models here.
# 글 종류 : PostType
class PostType(models.Model):
    name = models.CharField('구분',max_length=50)
    def __str__(self):
        return self.name
# 글 : Post
class Post(models.Model):
    type = models.ForeignKey(PostType,on_delete=models.CASCADE)
    headline = models.CharField('제목',max_length=200)
    #blank : 사용자 입력양식
    #null : 데이터베이스에 저장
    content = models.TextField('내용', blank=True, null=True)
    pub_date = models.DateField('날짜', auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#이미지,파일을 저장 관리하기 위해서 Django에서 'pillow'라이브러리 사용
#글에 포함된 이미지 : Image
class Image(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField('이미지 파일', upload_to='images/%Y/%m/%d')
    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        return models.Model.delete(self, using=using, keep_parents=keep_parents)

#글에 포함된 파일 : File
class File(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    file = models.FileField('파일', upload_to="files/%Y/%m/%d")
    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        return models.Model.delete(self, using=using, keep_parents=keep_parents) 