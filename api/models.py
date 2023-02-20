from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

def user_directory_path(instance, filename):
    return "uploads/profile_pictures/{0}_{1}".format(instance.name.lower(), instance.surname.lower())

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=128,null=False, blank=False,                    verbose_name="Name|Имя")
    surname = models.CharField(max_length=128,null=False, blank=False,                 verbose_name="Surname|Фамилия")
    phone_number = PhoneNumberField(null=False, blank=False, unique=True,              verbose_name="Phone Number|Номер телефона")
    profile_pic = models.ImageField(upload_to=user_directory_path,                     verbose_name="Profile Picture|Аватарка")
    on_campus = models.BooleanField(default=False, null=False, blank=False,            verbose_name="On Campus|На Кампусе")
    created_at = models.DateTimeField(auto_now_add=True,                               verbose_name="Created At|Создано")
    role = models.CharField(max_length=128, null=False, blank=False,                   verbose_name="Role|Роль")
    email = models.EmailField(max_length=128, null=False, blank=False,                 verbose_name="Gmail|Почта")
    gender = models.IntegerField(choices=[(0, 'Male|Мужской'), (1, 'Female|Женский')], verbose_name="Gender|Пол")

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