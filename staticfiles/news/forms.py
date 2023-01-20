from django import forms
from django.forms import forms, Textarea, ModelForm
from .models import News
from django.template.defaultfilters import slugify


class NewsForm(ModelForm):

    class Meta:
        model = News
        exclude = ['slug']

    def clean(self):
        cleaned_data = super(NewsForm, self).clean()
        getslug = cleaned_data.get('title')
        slug = slugify(getslug)

        if News.objects.filter(slug=slug).exists():
            raise forms.ValidationError(
                "Title or content is already exists", code="")

        return cleaned_data
