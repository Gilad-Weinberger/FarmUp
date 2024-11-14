from django.contrib import admin
from .models import *

admin.site.register(Field)
admin.site.register(FieldActivity)
admin.site.register(Line)
admin.site.register(LineActivity)
admin.site.register(UserActivity)