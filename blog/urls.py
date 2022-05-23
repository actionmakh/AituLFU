from django.conf.urls.static import static
from django.urls import path

from aituBlog import settings
from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news', views.news, name='news'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('uraura', views.uraura, name='uraura'),
    path('news/<int:newsId>', views.newsPost),
    path('lfu/<int:lfuID>', views.lfuPost, name='lfuItem'),
    path('addReply/<int:lfuID>', views.addReply, name='addReply'),
    path('aituLFU', views.aituLFU, name='aituLFU'),
    path('addLFU', views.addLFU, name='addLFU'),
    path('register', views.register, name='register'),
    path('about-us', views.aboutUs, name='about-us'),
    path('sendFeedback', views.addFeedback, name='addFeedback'),
    path('followLFU/<int:lfuID>', views.followlFU, name='followLFU'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)