from django.urls import path
from .views import *

urlpatterns = [
    path('person/', PersonList.as_view()),
    path('personfilter/', PersonFilterList.as_view()),
    path('person/<int:pk>', PersonDetail.as_view()),
    path('record/', RecordList.as_view()),
    path('record/<int:pk>', RecordDetail.as_view()),
    path('recordfilter/', RecordFilterList.as_view()),
    path('recognition/', recognition)
]
