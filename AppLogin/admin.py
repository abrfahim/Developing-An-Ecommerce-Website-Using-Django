from django.contrib import admin
from AppLogin.models import User, Profile, MyUserManager
# Register your models here.

admin.site.register(User)
admin.site.register(Profile)