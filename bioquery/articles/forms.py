from django import forms
from django.core.exceptions import ValidationError

from bioquery.core.models import Category, DNA, Photo, Reference

from .models import Article


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ["name", "title", "date_access"]


class DNAForm(forms.ModelForm):
    class Meta:
        model = DNA
        fields = ["name", "sequence"]


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["category"].choices = tuple(
            [(category.pk, category.name) for category in Category.objects_db.all()]
        )
        self.fields["dnas"].choices = tuple(
            [(dna.pk, dna.name) for dna in DNA.objects_db.all(user_id=user.id)]
        )
        self.fields["photo"].choices = tuple(
            [(photo.pk, photo.file) for photo in Photo.objects_db.all(user_id=user.id)]
        )
        self.fields["references"].choices = tuple(
            [
                (reference.pk, reference.name)
                for reference in Reference.objects_db.all(user_id=user.id)
            ]
        )

    photo = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(),
    )
    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(),
    )
    dnas = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        choices=(),
    )
    references = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        choices=(),
    )

    class Meta:
        model = Article
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite o título"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Digite o conteúdo"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        words = [w.capitalize() for w in title.split()]
        return " ".join(words)

    def clean(self):
        self.cleaned_data = super().clean()

        if not self.cleaned_data.get("title"):
            raise ValidationError("Informe um título.")

        if not self.cleaned_data.get("content"):
            raise ValidationError("Informe o conteúdo.")

        return self.cleaned_data


class PhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = False

    class Meta:
        model = Photo
        fields = ["file"]
