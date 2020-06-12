from django.contrib import admin
from .models import Company, Vacancy, Speciality, Application


admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Speciality)
admin.site.register(Application)
