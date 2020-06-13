from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
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

# -----Для придожения authorizaion- Я переписать с приложениями не успеваю-----------
class MyProjectLoginView(LoginView):
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

# --------------Для придожения vacancy-----------
class MainView(View):
    def get(self, request):
        specialties = Speciality.objects.annotate(count=Count('vacancies'))
        companies = Company.objects.annotate(count=Count('vacancies'))
        context = {'specialties': specialties,
                   'companies': companies}
        return render(request, 'vacancies/index.html', context)


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        request.session['return_path'] = self.request.get_full_path()
        context = {'vacancies': vacancies,
                   'page_title': 'Все вакансии'}
        return render(request, 'vacancies/vacancies.html', context)


class VacanciesByCategoryView(View):
    def get(self, request, category):
        category = get_object_or_404(Speciality, code=category)
        request.session['return_path'] = self.request.get_full_path()
        context = {'vacancies': category.vacancies.all(),
                   'page_title': category.title}
        return render(request, 'vacancies/vacancies.html', context)


class VacancyView(LoginRequiredMixin, View):
    login_url = reverse_lazy('vacancy:login_page')

    def get(self, request, pk):
        get_url = self.request.META.get('HTTP_REFERER', '/')
        return_path = self.request.session['return_path']
        vacancy = get_object_or_404(Vacancy, pk=pk)
        users = [i['user'] for i in vacancy.applications.all().values('user')]
        message = ''
        if request.user.pk in users:
            message = "Вы отправили отзыв на вакансию"
        context = {'vacancy': vacancy,
                   'users': users,
                   'message': message,
                   'get_url': get_url,
                   'return_path': return_path}
        return render(request, 'vacancies/vacancy.html', context)

    def post(self, request, pk):
        get_vacancy = Vacancy.objects.get(pk=pk)
        users = [i['user'] for i in get_vacancy.applications.all().values('user')]
        # Если у vacancy нет owner это не работает ??????
        # user = ''
        # try:
        #     user = get_vacancy.applications.all().values('user').get(user=request.user)
        # except:
        #     pass
        if request.user.pk in users:
            return HttpResponseRedirect(reverse('vacancy:vacancy_id', args=[get_vacancy.pk]))
        else:
            application = Application()
            application.vacancy = get_vacancy
            application.user = request.user
            form = ApplicationForm(request.POST, instance=application)
            if form.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('vacancy:vacancy_id', args=[get_vacancy.pk]))
            else:
                return HttpResponseRedirect(reverse('vacancy:vacancy_id', args=[get_vacancy.pk]))

# --------------Для придожения company-----------
class CompaniesView(View):

    def get(self, request):
        companies = Company.objects.annotate(count=Count('vacancies'))
        context = {'companies': companies}
        return render(request, 'company/companies.html', context)


class CompanyView(View):

    def get(self, request, pk):
        get_url = self.request.META.get('HTTP_REFERER', '/')
        request.session['return_path'] = self.request.get_full_path()
        company = get_object_or_404(Company, pk=pk)
        context = {'company': company,
                   'vacancies': company.vacancies.all(),
                   'get_url': get_url}
        return render(request, 'company/company.html', context)


class MyCompanyControlView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('vacancy:login_page')
    template_name = 'company/company-create.html'

    def dispatch(self, request, *args, **kwargs):
        company = ''
        try:
            # company = Company.objects.all().get(owner=self.request.user)
            company = Company.get_user_company(self.request.user)
        except:
            pass
        if company:
            return redirect('vacancy:edit_company')
        return super().dispatch(request, *args, **kwargs)

class MyCompanyCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('vacancy:login_page')
    model = Company
    form_class = CompanyForm
    template_name = 'company/company-edit.html'
    success_url = reverse_lazy('vacancy:edit_company')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
        # isinstance: Company = form.save(commit=False)
        # isinstance.owner = self.request.user
        # isinstance.save()


class MyCompanyUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('vacancy:login_page')
    model = Company
    form_class = CompanyForm
    template_name = 'company/company-edit.html'

    def get_object(self, queryset=None):
        company = ''
        try:
            company = Company.get_user_company(self.request.user)
        except:
            pass
        if not company:
            return redirect('vacancy:add_company')
        return company

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Информация о компании сохранена')
        return redirect('vacancy:edit_company')

    def get_context_data(self, **kwargs):
        context = super(MyCompanyUpdateView, self).get_context_data(**kwargs)
        return context

# --------------Для придожения vacansy-----------
class ApplicationsView(View):

    def get(self, request, pk):
        get_url = self.request.META.get('HTTP_REFERER', '/')
        vacancy = get_object_or_404(Vacancy, pk=pk)
        if not vacancy.company.owner == request.user:
            messages.success(self.request, 'Информация только для владельца вакансии')
            return HttpResponseRedirect(reverse('vacancy:vacancy_id', args=[vacancy.pk]))
        applications = vacancy.applications.all()
        context = {'vacancy': vacancy,
                   'get_url': get_url,
                   'applications': applications, }
        return render(request, 'vacancies/applications.html', context)


class MyVacancyListView(ListView):
    
    def dispatch(self, request, *args, **kwargs):
        company = ''
        try:
            company = Company.objects.all().get(owner=self.request.user)
            # company = Company.get_user_company(self.request.user)
        except:
            pass
        if not company:
            return redirect('vacancy:add_company')
        return super().dispatch(request, *args, **kwargs) 
    
    model = Vacancy
    template_name = 'company/vacancy-list.html'

    def get_context_data(self, **kwargs):
        company = self.request.user.company
        context = super(MyVacancyListView, self).get_context_data(**kwargs)
        self.request.session['return_path'] = self.request.get_full_path()
        context['vacancies'] = company.vacancies.all().annotate(count=Count('applications'))
        return context


class MyVacancyCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('vacancy:login_page')
    model = Vacancy
    form_class = VacancyForm
    template_name = 'company/vacancy-edit.html'
    success_url = reverse_lazy('vacancy:my_vacancies')

    def form_valid(self, form):
        form.instance.company = Company.get_user_company(self.request.user)
        return super().form_valid(form)


class MyVacancyUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('vacancy:login_page')
    model = Vacancy
    form_class = VacancyForm
    template_name = 'company/vacancy-edit.html'

    def get_context_data(self, **kwargs):
        kwargs['vacancy:edit_vacancies'] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        pk = self.object.pk
        form.save()
        messages.success(self.request, 'Информация о вакансии обновлена')
        # return redirect('vacancy:my_vacancies')
        return HttpResponseRedirect(reverse('vacancy:edit_vacancies', args=[pk]))


class SearchVacancyView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'
    successful_search = False

    def get_context_data(self, **kwargs):
        if self.successful_search:
            kwargs['page_title'] = "Поиск вакансий"
        else:
            kwargs['page_title'] = "Вакансий не найдено"
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        query = self.request.GET.get('name')
        vacancies = Vacancy.objects.filter(
            Q(title__icontains=query) | Q(title__icontains=query.lower()) | Q(title__icontains=query.upper()) |
            Q(title__icontains=query.title()) | Q(description__icontains=query.lower()) |
            Q(description__icontains=query) | Q(description__icontains=query.upper()) |
            Q(description__icontains=query.title()) | Q(skills__icontains=query.lower()) |
            Q(skills__icontains=query) | Q(skills__icontains=query.upper()) |
            Q(skills__icontains=query.title()))
        if vacancies:
            self.successful_search = True
        return vacancies
