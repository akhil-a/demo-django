from django import forms
from .models import ProjectList


class ProjectForm(forms.Form):
    project_name = forms.ModelChoiceField(queryset=ProjectList.objects.all(), to_field_name='project_name',
                                          widget=forms.Select(), empty_label='Select Project', required=False)
