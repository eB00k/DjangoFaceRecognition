from rest_framework import generics
from .models import Person, Record
from .serializers import *

class RecordList(generics.ListCreateAPIView):
    serializer_class = RecordSerializer

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

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()