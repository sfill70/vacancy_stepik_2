from django.forms import ModelForm
from .models import Resume


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'speciality', 'grade', 'education', 'experience',
                  'portfolio']
