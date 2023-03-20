from django.urls import path
from .views import *

urlpatterns = [
    path('person/', PersonList.as_view()),
    path('person/<int:pk>', PersonDetail.as_view()),
    path('record/', RecordList.as_view()),
    path('record/<int:pk>', RecordDetail.as_view()),
    path('rekognition/', rekognition),
    path('rekognition/get/', rekognition_get),
    path('gate/<int:pk>', gate),
    path('avatar/<int:pk>', get_profile_image),
    path('aws/<int:pk>', get_aws_image),
]
