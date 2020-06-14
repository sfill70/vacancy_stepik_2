from logging import getLogger

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from resume.models import Resume
from .forms import ResumeForm

_logger = getLogger(__name__)


class MyResumeControlView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('vacancy:login_page')
    template_name = 'resume/resume-create.html'

    def dispatch(self, request, *args, **kwargs):
        resume = ''
        try:
            resume = Resume.objects.all().get(user=self.request.user)
        except:
            pass
        if resume:
            return redirect('resume:edit_resume')
        return super().dispatch(request, *args, **kwargs)


class MyResumeCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('vacancy:login_page')
    model = Resume
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'
    success_url = reverse_lazy('resume:edit_resume')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MyResumeUpdateView(LoginRequiredMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        resume = ''
        try:
            resume = self.request.user.resume
            # resume = Resume.objects.all().get(user=self.request.user)
        except:
            pass
        if not resume:
            return redirect('resume:add_resume')
        return super().dispatch(request, *args, **kwargs)

    login_url = reverse_lazy('vacancy:login_page')
    model = Resume
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'

    def get_object(self, queryset=None):
        resume = ''
        try:
            resume = Resume.get_user_company(self.request.user)
            # resume = self.request.user.resume
        except:
            pass
        return resume

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Резюме сохранено')
        return redirect('resume:edit_resume')

    def get_context_data(self, **kwargs):
        context = super(MyResumeUpdateView, self).get_context_data(**kwargs)
        return context


class ResumeView(View):

    def get(self, request):
        get_url = self.request.META.get('HTTP_REFERER', '/')
        resume = Resume.objects.all()
        context = {'resume': resume,
                   'get_url': get_url, }
        return render(request, 'resume/resume.html', context)


class SearchResumeyView(ListView):
    model = Resume
    template_name = 'resume/resume.html'
    context_object_name = 'resume'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = "Поиск вакансий"
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        query = self.request.GET.get('name')
        resume = Resume.objects.filter(
            Q(speciality__title__icontains=query) | Q(speciality__title__icontains=query.title()))
        return resume


# class ResumeViewOne(View):
#     from django.forms.models import model_to_dict
#
#     def get(self, request):
#         get_url = self.request.META.get('HTTP_REFERER', '/')
#         resume = Resume.objects.all()
#         context = {'resume': resume,
#                    'get_url': get_url, }
#         return render(request, 'resume/resume_one.html', context)

class ResumeViewOne(View):

    def get(self, request, pk):
        get_url = self.request.META.get('HTTP_REFERER', '/')
        resume = get_object_or_404(Resume, pk=pk)
        resume_dict = model_to_dict(resume)
        context = {'resume': resume,
                   'resume_dict': resume_dict,
                   'get_url': get_url}
        return render(request, 'resume/resume_one.html', context)
