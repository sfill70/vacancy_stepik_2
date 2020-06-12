from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from vacancy.models import Speciality
from django.utils import timezone
from vacancy.data import EducationChoices, GradeChoices, WorkStatusChoices


class Resume(models.Model):

    user = models.OneToOneField(User, verbose_name="Владелец", related_name="resume", on_delete=models.CASCADE,
                                 default=None, blank=True)
    name = models.CharField(max_length=200, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    status = models.CharField(max_length=255, choices=WorkStatusChoices.choices(), verbose_name="Статус")
    salary = models.IntegerField(verbose_name="Зарплата")
    speciality = models.ForeignKey(Speciality, verbose_name="специализация", related_name="resume", on_delete=models.PROTECT, blank=True)
    grade = models.CharField(max_length=255, choices=GradeChoices.choices(), verbose_name="Квалификация ")
    education = models.CharField(max_length=255, choices=EducationChoices.choices(), verbose_name="Образование")
    experience = models.CharField(max_length=100, verbose_name='Квалификация')
    portfolio = models.URLField(verbose_name='portfolio', blank=True)

    def __str__(self):
        return self.surname


    def get_user_company(user):
        return Resume.objects.all().get(user=user)