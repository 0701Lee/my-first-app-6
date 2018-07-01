from django.urls import path
from .views import *
app_name='Blog'
urlpatterns=[
    path('',index.as_view(),name='index'),
    path('/<int:post_id>/',detail,name='detail'),
    path('posting/',posting,name='posting'),
    path('search',searchP,name='searchP')
    ]