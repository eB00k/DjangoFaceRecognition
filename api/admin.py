from django.contrib import admin
from .models import Student, Attendance
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    pass

class AttendanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
