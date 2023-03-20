from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics, status, mixins
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        is_user = request.data.get("is_user", default=False)
        username = request.data.get("user.username", default="")
        password = request.data.get("user.password", default="")
        user = None
        if (is_user != False and username != "" and password != ""):
            user = User(username=username, password=password, first_name=data['name'],
                        last_name=data['surname'], email=data['email'],
                        is_staff=True)
            user.save()
        serializer.save(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save()


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
def rekognition(request):
    if request.method == 'POST':
        item = AWSImage.objects.create(image=request.data["file"], person=Person.objects.get(id=request.data["id"]))
        return Response("", status=status.HTTP_200_OK)

@api_view(['POST'])
def rekognition_get(request):
    if request.method == 'POST':
        print(request.data)
        res = aws.match(request.data["file"])
        try:
            i = AWSImage.objects.get(pk=int(res))
        except:
            return Response({'error': res}, status=status.HTTP_404_NOT_FOUND)
        return Response(PersonSerializer(i.person).data, status=status.HTTP_200_OK)



@api_view(['POST', 'PATCH'])
def gate(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except:
        return Response("No person with id {}".format(pk), status=status.HTTP_404_NOT_FOUND)
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
        data = GateSerializer(last_record).data
        return Response(data, status=status.HTTP_200_OK)
