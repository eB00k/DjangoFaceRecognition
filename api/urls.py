from django.urls import path
from .views import *

urlpatterns = [
    path('person/', PersonList.as_view()),
    path('person/<int:pk>', PersonDetail.as_view()),
    path('record/', RecordList.as_view()),
    path('record/<int:pk>', RecordDetail.as_view()),
    path('rekognition/', rekognition),
    path('gate/<int:pk>', gate),
]
