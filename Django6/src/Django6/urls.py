"""Django6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#해당 파일이 view 함수를 알아야되므로 from~import로 함수추가
#urls와 views가 다른 파일 위치이므로 절대경로로 표현

from vote.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('vote/', include('vote.urls')),
    path('login/', include('customlogin.urls') ),
    path('auth/', include('social_django.urls',namespace='social') ),
    path('blog/',include('Blog.urls'))

]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)