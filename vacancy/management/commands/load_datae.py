from vacancy.models import Company, Speciality, Vacancy
import vacancy.data as data
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime


class Command(BaseCommand):
    help = 'Load data from data.py file to DB'

    def handle(self, *args, **options):

        for company in data.companies:
            Company.objects.create(name=company['title'])

        for specialty in data.specialties:
            Speciality.objects.create(code=specialty['code'],
                                      title=specialty['title'],
                                      picture='https://place-hold.it/100x60')

        for job in data.jobs:
            company = Company.objects.get(name=job['company'])
            speciality = Speciality.objects.get(code=job['cat'])
            Vacancy.objects.create(
                title=job['title'],
                speciality=speciality,
                company=company,
                description=job['desc'],
                salary_min=int(job['salary_from']),
                salary_max=int(job['salary_to']),
                published_at=datetime.strptime(job['posted'], '%Y-%m-%d'))

        self.stdout.write(self.style.SUCCESS('Ok'))
