from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

def user_directory_path(instance, filename):
    return "uploads/profile_pictures/{0}_{1}_{2}".format(instance.id, instance.name.lower(), instance.surname.lower())

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=128,null=False, blank=False)
    surname = models.CharField(max_length=128,null=False, blank=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    profile_pic = models.ImageField(upload_to=user_directory_path)
    on_campus = models.BooleanField(default=False, null=False, blank=False)

class Attandes(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    time_entry = models.TimeField(null=False, blank=False)
    time_exit = models.TimeField(null=True)