from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.services import aws

def user_directory_path(instance, filename):
    return "static/uploads/profile_pictures/{0}_{1}".format(instance.name.lower(), instance.surname.lower())

class Person(models.Model):
    roles = [
        (0,    "Student"),
        (2023, "Student-2023"),
        (2024, "Student-2024"),
        (2025, "Student-2025"),
        (2026, "Student-2026"),
        (2027, "Student-2027"),
        (2028, "Student-2028"),
        (2029, "Student-2029"),
        (2030, "Student-2030"),
        (2031, "Student-2031"),
        (2032, "Student-2032"),
        (2033, "Student-2033"),
        (2034, "Student-2034"),
        (2035, "Student-2035")
    ]
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=128,null=False, blank=False,                    verbose_name="Name|Имя")
    surname = models.CharField(max_length=128,null=False, blank=False,                 verbose_name="Surname|Фамилия")
    phone_number = PhoneNumberField(null=False, blank=False, unique=True,              verbose_name="Phone Number|Номер телефона")
    profile_pic = models.ImageField(upload_to="static/uploads/profile_pictures/",      verbose_name="Profile Picture|Аватарка")
    on_campus = models.BooleanField(default=False, null=False, blank=False,            verbose_name="On Campus|На Кампусе")
    created_at = models.DateTimeField(auto_now_add=True,                               verbose_name="Created At|Создано")
    role = models.IntegerField(choices=roles, default=0, null=False, blank=False, verbose_name="Role|Роль")
    email = models.EmailField(max_length=128, null=False, blank=False,                 verbose_name="Gmail|Почта")
    gender = models.IntegerField(choices=[(0, 'Male|Мужской'), (1, 'Female|Женский')], verbose_name="Gender|Пол")
    major = models.IntegerField(choices=[(0, 'CS'), (1, 'CM')], null=True,            verbose_name="Major|Факультет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Person|Человек"
        verbose_name_plural = "People|Люди"
    

class Record(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT,     verbose_name="Person|Человек")
    datetime_entry = models.DateTimeField(auto_now_add=timezone.now, verbose_name="Datetime Entry|Время входа")
    datetime_exit = models.DateTimeField(null=True, blank=True,      verbose_name="Datetime Exit|Время выхода")

    class Meta:
        verbose_name = "Record|Запись"
        verbose_name_plural = "Records|Записи"

def awsimagedir(instance, filename):
    return "static/uploads/AWSImages/{}/{}".format(instance.person.id, instance.image.name)

class AWSImage(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE,  verbose_name="Person|Человек")
    image = models.ImageField(upload_to=awsimagedir,     verbose_name="Images|Фотография")

@receiver(post_save, sender=AWSImage, dispatch_uid="update_aws_server")
def update(sender, instance, **kwargs):
    instance.image.file.name = "{}/{}.jpg".format(instance.person.id, instance.id)
    aws.upload([{'file': instance.image.file, 'name': str(instance.id)}])
