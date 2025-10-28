from django.contrib import admin
from .models import bus, route, schedule
# Register your models here.
admin.site.register(bus)
admin.site.register(route)
admin.site.register(schedule)
