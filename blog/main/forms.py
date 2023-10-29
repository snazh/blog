from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import *


class AddPostForm(forms.ModelForm):
    # category displaying
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Category not selected"

    class Meta:
        model = Post  # name of model
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']  # fields which were retrieved
        # widgets for style of form elements
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-blue', 'id': 'title', 'name': 'title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form-control-blue', 'id': 'slug', 'name': 'slug'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control form-control-blue', 'cols': 60, 'rows': 10, 'id': 'content',
                       'name': 'content'}),

        }

    def clean_title(self):  # custom validator
        title = self.cleaned_data['title']
        if 1 > len(title) > 250:
            raise ValidationError('Title length exceeds')
        return title

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if not slug:
            title = self.cleaned_data['title']
            slug = slugify(title)
        return slug
