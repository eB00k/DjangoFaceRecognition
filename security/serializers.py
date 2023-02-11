from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User

class SignUpSerializer(serializer.ModelSerializer):