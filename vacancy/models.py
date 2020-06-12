from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    location = models.CharField(max_length=30, verbose_name="Город")
    logo = models.ImageField(upload_to='company_images', blank=True)
    description = models.TextField(verbose_name="Информация")
    employee_count = models.IntegerField(verbose_name="Количество персонала", default=1)
    owner = models.OneToOneField(User, verbose_name="Владелец", related_name="company", on_delete=models.CASCADE,
                                 default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_user_company(user):
        return Company.objects.all().get(owner=user)


class Speciality(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='MEDIA_SPECIALITY_IMAGE_DIR', blank=True)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название вакансии")
    speciality = models.ForeignKey(Speciality, related_name="vacancies", on_delete=models.PROTECT, null=True,
                                   blank=True)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.PROTECT, null=True, blank=True)
    skills = models.TextField("Требуемые навыки")
    description = models.TextField(verbose_name="Описание вакансии")
    salary_min = models.IntegerField(verbose_name="Зарплата от")
    salary_max = models.IntegerField(verbose_name="Зарплата до")
    published_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('vacancy_detail', args=[str(self.pk)])

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(verbose_name="Имя", max_length=50)
    written_phone = models.CharField(verbose_name="Телефон для связи", max_length=20)
    written_cover_letter = models.TextField(verbose_name="Сопроводительное письмо")
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.PROTECT)
