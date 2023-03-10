from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics, status, mixins
from rest_framework.renderers import JSONRenderer

from .models import Person, Record, AWSImage
from .serializers import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services import aws
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.core import serializers


class RecordList(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['person']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Record.objects.all()
        person = self.request.query_params.get('Person')
        if person is not None:
            queryset = queryset.filter(person=person)
            return queryset
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


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    permission_classes = [IsAuthenticated]


@api_view(['GET', 'POST'])
def rekognition(request):
    if request.method == 'GET':
        print(request.data)
        res = aws.match(request.data["file"])
        try:
            person = Person.objects.get(pk=int(res))
        except:
            return Response({'error': res}, status=status.HTTP_404_NOT_FOUND)
        return Response(PersonSerializer(person).data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        item = AWSImage.objects.create(image=request.data["file"], person=Person.objects.get(id=request.data["id"]))
        aws.upload([request.data])
        return Response("", status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
def gate(request, pk):
    person = Person.objects.get(pk=pk)
    records = Record.objects.filter(person=pk)
    if request.method == 'POST':
        if person.on_campus:
            return Response({'error': 'person with id {} is already on campus'.format(pk)},
                            status=status.HTTP_400_BAD_REQUEST)
        record = Record.objects.create(person=person)
        person.on_campus = True
        person.save()
        # data = JSONRenderer().render(GateSerializer(record).data)
        data = GateSerializer(record).data
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        if not person.on_campus:
            return Response({'error': 'person with id {} should not be on campus'.format(pk)},
                            status=status.HTTP_400_BAD_REQUEST)
        last_record = records.last()
        last_record.datetime_exit = timezone.now()
        last_record.save()
        person.on_campus = False
        person.save()
        # data = JSONRenderer().render(GateSerializer(last_record).data)
        data = GateSerializer(last_record).data
        return Response(data, status=status.HTTP_200_OK)
