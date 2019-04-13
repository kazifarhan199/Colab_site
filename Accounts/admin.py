from django.contrib import admin
from .models import User
from .models import  Github_model
# Register your models here.
admin.site.register(Github_model)
admin.site.register(User)
