from django.contrib import admin
from . models import user_details, pan_db

# Register your models here.
admin.site.register(user_details)
admin.site.register(pan_db)
