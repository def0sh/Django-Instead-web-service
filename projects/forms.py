from django.forms import ModelForm

from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'slug', 'image', 'tags', 'description', 'demo_link', 'source_link']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __int__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'
