from django.urls import path
from . import views

urlpatterns =[
    path('',views.login,name='login'),
    path('processor/',views.processor,name='processor'),
    path('video_edit/',views.video_edit,name='video_edit'),
    path('video_stream/',views.video_stream,name='video_stream'),
]