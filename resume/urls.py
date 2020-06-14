
from django.urls import path
from .views import MyResumeControlView, MyResumeCreateView, MyResumeUpdateView, ResumeView, SearchResumeyView, ResumeViewOne
app_name = 'resume'

urlpatterns = [
    path('resume_control/', MyResumeControlView.as_view(), name='resume_control'),
    path('add_resume/', MyResumeCreateView.as_view(), name='add_resume'),
    path('edit_resume/', MyResumeUpdateView.as_view(), name='edit_resume'),
    path('resume_list/', ResumeView.as_view(), name='resume_list'),
    path('resume_search', SearchResumeyView.as_view(), name='resume_search'),
    path('resume_one/<int:pk>/', ResumeViewOne.as_view(), name='resume_one'),

]
