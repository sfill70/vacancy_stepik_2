
from django.urls import path
from .views import custom_handler404, MainView, VacanciesView, VacanciesByCategoryView, VacancyView, CompanyView, \
    MyprojectLoginView, RegisterUserView, MyProjectLogout, CompaniesView

app_name = 'vacancy'

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', VacanciesByCategoryView.as_view(), name='category'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy_id'),
    path('companies/', CompaniesView.as_view(), name='companies'),
    path('companies/<int:pk>/', CompanyView.as_view(), name='company_id'),
    path('login/', MyprojectLoginView.as_view(), name='login_page'),
    path('register_page/', RegisterUserView.as_view(), name='register_page'),
    path('logout/', MyProjectLogout.as_view(), name='logout'),
]

handler404 = custom_handler404