from django.urls import path

from . import views


urlpatterns = [
    # path('index/', views.index, name='index'),
    path('', views.Music.as_view(), name='list'),
    # re_path('(?P<name>.+)/', views.MusicDetail.as_view(), name='list'),
    path('lyr/<name>/', views.MusicLyr.as_view(), name='lyr'),
    path('<name>/', views.MusicMethod.as_view(), name='method'),
]
