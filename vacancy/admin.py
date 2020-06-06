from django.contrib import admin
from .models import Company, User, Vacancy, Speciality, Application
# Register your models here.

# admin.site.register(User)
admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Speciality)
admin.site.register(Application)
