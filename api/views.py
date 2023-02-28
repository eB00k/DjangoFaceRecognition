from rest_framework import generics, status
from .models import Person, Record
from .serializers import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services import aws
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class RecordList(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Record.objects.all()
        Person = self.request.query_params.get('Person')
        if Person is not None:
            queryset = queryset.filter(Person = Person)
            return queryset

class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
    permission_classes = [IsAuthenticated]

class PersonList(generics.ListCreateAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user', 'name', 'surname', 'on_campus', 'role']
    search_fields = ('id', 'name', 'surname', 'phone_number', 'on_campus', 'created_at', 'role', 'email', 'gender')
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request.data)
        aws.upload([self.request.data])
        return super().perform_create(serializer)

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if 'file' in self.request.data:
            res = aws.match(self.request.data["file"])
            if res == None: return None
            return get_object_or_404(Person, pk=int(res))
        elif 'pk' in self.request:
            return get_object_or_404(Person, pk=self.request.pk)

# class PersonFilterList(generics.ListAPIView):
#     serializer_class = PersonSerializer
#     filter_fields = ('id', 'name', 'surname', 'phone_number', 'on_campus', 'created_at', 'role', 'gender')

#     def get_queryset(self):
#         queryset = Person.objects.all()
        
#         for i in self.filter_fields:
#             if self.request.query_params.get(i) is not None:
#                 queryset = queryset.filter(**{i+'__icontains': self.request.query_params.get(i)})
#         return queryset

# class RecordFilterList(generics.ListAPIView):
#     serializer_class = RecordSerializer
#     filter_fields = ('id', 'person', 'datetime_entry', 'datetime_exit')

#     def get_queryset(self):
#         id = self.request.query_params.get('person')
#         if id is not None:
#             queryset = Record.objects.filter(person = id)
#             return queryset
#         return Record.objects.none()

@api_view(['GET', 'POST'])
def rekognition(request):
    if request.method == 'GET':
        print(request.data)   
        res = aws.match(request.data["file"])
        return Response(res, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        aws.upload([request.data])
        return Response("", status=status.HTTP_200_OK)