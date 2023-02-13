from rest_framework import generics
from .models import Person, Record
from .serializers import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class RecordList(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    filter_fields = ('id', 'person', 'datetime_entry', 'datetime_exit')
    search_fields = ('id', 'person', 'datetime_entry', 'datetime_exit')

    def get_queryset(self):
        queryset = Record.objects.all()
        Person = self.request.query_params.get('Person')
        if Person is not None:
            queryset = queryset.filter(Person = Person)
            return queryset

class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()

class PersonList(generics.ListCreateAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ('id', 'name', 'surname', 'phone_number', 'on_campus', 'created_at', 'role', 'gender')
    search_fields = ('id', 'name', 'surname', 'phone_number', 'on_campus', 'created_at', 'role', 'gender')

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

class PersonFilterList(generics.ListAPIView):
    serializer_class = PersonSerializer
    filter_fields = ('id', 'name', 'surname', 'phone_number', 'on_campus', 'created_at', 'role', 'gender')

    def get_queryset(self):
        queryset = Person.objects.all()
        
        for i in self.filter_fields:
            if self.request.query_params.get(i) is not None:
                queryset = queryset.filter(**{i+'__icontains': self.request.query_params.get(i)})
        return queryset

class RecordFilterList(generics.ListAPIView):
    serializer_class = RecordSerializer
    filter_fields = ('id', 'person', 'datetime_entry', 'datetime_exit')

    def get_queryset(self):
        id = self.request.query_params.get('person')
        if id is not None:
            queryset = Record.objects.filter(person = id)
            return queryset
        return Record.objects.none()