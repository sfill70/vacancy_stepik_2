from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from .forms import CompanyForm, AuthUserForm, RegisterUserForm, VacancyForm, ApplicationForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from logging import getLogger
from vacancy.models import Speciality, Company, Vacancy, Application

_logger = getLogger(__name__)

def custom_handler404(request, exception):
    return HttpResponseNotFound('Запрашеваемая страница не существует.')


def custom_handler500(request, exception):
    return HttpResponseNotFound('Сервер не отвечает.')


class MyprojectLoginView(LoginView):
    template_name = 'authorization/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('vacancy:home')

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    model = User
    template_name = 'authorization/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('vacancy:home')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('vacancy:home')


class MainView(View):
    def get(self, request):
        specialties = Speciality.objects.annotate(count=Count('vacancies'))
        companies = Company.objects.annotate(count=Count('vacancies'))
        get_url = str(self.request.META.get('HTTP_REFERER', '/'))
        context = {'specialties': specialties,
                   'companies': companies,
                   'get_url': get_url}
        return render(request, 'vacancies/index.html', context)


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        context = {'vacancies': vacancies,
                   'page_title': 'Все вакансии'}
        return render(request, 'vacancies/vacancies.html', context)


class VacanciesByCategoryView(View):
    def get(self, request, category):
        category = get_object_or_404(Speciality, code=category)
        context = {'vacancies': category.vacancies.all(),
                   'page_title': category.title}
        return render(request, 'vacancies/vacancies.html', context)


class VacancyView(View):
    def get(self, request, pk):
        get_url = self.request.META.get('HTTP_REFERER', '/')
        # request.session['return_path'] = self.request.META.get('HTTP_REFERER', '/')
        # return_path = self.request.session['return_path']
        vacancy = get_object_or_404(Vacancy, pk=pk)
        context = {'vacancy': vacancy,
                   'get_url': get_url,}
        return render(request, 'vacancies/vacancy.html', context)

    def post(self, request, pk):
        get_vacancy = Vacancy.objects.get(pk=pk)
        application = Application()
        application.vacancy = get_vacancy
        application.user = request.user
        get_application = application
        form = ApplicationForm(request.POST, instance=get_application)
        if form.is_valid():
            application.save()
            return HttpResponseRedirect(reverse('vacancy:vacancy_id', args=[get_vacancy.pk]))



class CompaniesView(View):
    def get(self, request):
        companies = Company.objects.annotate(count=Count('vacancies'))
        context= {'companies': companies}
        return render(request, 'company/companies.html', context)

class CompanyView(View):
    def get(self, request, pk):
        get_url = self.request.META.get('HTTP_REFERER', '/')
        company = get_object_or_404(Company, pk=pk)
        context = {'company': company,
                   'vacancies': company.vacancies.all(),
                   'get_url': get_url}
        return render(request, 'company/company.html', context)

