from rest_framework import generics
from .models import Student, Attendance
from .serializers import *

class AttendanceList(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.all()
        student = self.request.query_params.get('student')
        if student is not None:
            queryset = queryset.filter(student = student)
            return queryset

class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()

class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()