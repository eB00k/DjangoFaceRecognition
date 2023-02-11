from django.contrib import admin
from .models import Person, Record
# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    pass

class RecordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Record, RecordAdmin)
