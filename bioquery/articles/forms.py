from django import forms
from django.core.exceptions import ValidationError

from bioquery.core.models import Category, DNA, Photo

from .models import Article


class ArticleForm(forms.ModelForm):
    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=tuple([(category.pk, category.name) for category in Category.objects_db.all()]),
    )
    dnas = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        choices=tuple([(dna.pk, dna.name) for dna in DNA.objects_db.all()]),
    )
    photos = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        choices=tuple([(photo.pk, photo.file) for photo in Photo.objects_db.all()]),
    )

    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o conteúdo'
            })
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        words = [w.capitalize() for w in title.split()]
        return ' '.join(words)

    def clean(self):
        self.cleaned_data = super().clean()

        if not self.cleaned_data.get('title'):
            raise ValidationError('Informe um título.')

        if not self.cleaned_data.get('content'):
            raise ValidationError('Informe o conteúdo.')

        return self.cleaned_data


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file']