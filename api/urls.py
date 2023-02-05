from django.urls import path
from .views import *

urlpatterns = [
    path('student/', StudentList.as_view()),
    path('student/<int:pk>', StudentDetail.as_view()),
    path('attendance/', AttendanceList.as_view()),
    path('attendance/<int:pk>', AttendanceDetail.as_view()),
]
