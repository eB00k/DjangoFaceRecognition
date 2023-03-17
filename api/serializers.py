from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
import traceback

from api.models import Person, Record

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class RecordSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    class Meta:
        model = Record
        fields = '__all__'

class GateSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(many=False, queryset=Person.objects.all())
    entry = serializers.DateTimeField(required=False)
    exit = serializers.DateTimeField(required=False)

    class Meta:
        model = Record
        fields = "__all__"
