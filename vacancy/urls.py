
from django.urls import path
from .views import custom_handler404, MainView, VacanciesView, VacanciesByCategoryView, VacancyView, CompanyView, \
    MyProjectLoginView, RegisterUserView, MyProjectLogout, CompaniesView, MyCompanyCreateView,MyCompanyUpdateView, \
    MyCompanyControlView, MyVacancyCreateView, MyVacancyListView, MyVacancyUpdateView, ApplicationsView, SearchVacancyView

app_name = 'vacancy'

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', VacanciesByCategoryView.as_view(), name='category'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy_id'),
    path('companies/', CompaniesView.as_view(), name='companies'),
    path('companies/<int:pk>/', CompanyView.as_view(), name='company_id'),
    path('login/', MyProjectLoginView.as_view(), name='login_page'),
    path('register_page/', RegisterUserView.as_view(), name='register_page'),
    path('logout/', MyProjectLogout.as_view(), name='logout'),
    path('company_control/', MyCompanyControlView.as_view(), name='company_control'),
    path('add_company/', MyCompanyCreateView.as_view(), name='add_company'),
    path('edit_company/', MyCompanyUpdateView.as_view(), name='edit_company'),
    path('vacancies/<int:pk>/applications/', ApplicationsView.as_view(), name='applications'),
    path('my_vacancies/', MyVacancyListView.as_view(), name='my_vacancies'),
    path('add_vacancies/', MyVacancyCreateView.as_view(), name='add_vacancies'),
    path('edit_vacancies/<int:pk>', MyVacancyUpdateView.as_view(), name='edit_vacancies'),
    path('search_vacancy', SearchVacancyView.as_view(), name='search_vacancy'),
]


handler404 = custom_handler404