from django import forms
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('SJ', 'پیشنهاد'),
        ('CR', 'انتقاد'),
        ('BG', 'گزارش مشکل'),
    )

    name = forms.CharField(max_length=250, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=11, required=True)
    email = forms.EmailField(required=False)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!")
            else:
                return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'body': forms.Textarea(attrs={'placeholder': 'متن کامنت شما'}),
            'email': forms.Textarea(attrs={'style': 'display: none;'}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]

        if name:
            if name.isnumeric():
                raise forms.ValidationError("نام نمیتواند عددی باشد!")
            else:
                return name

    def clean_body(self):
        body = self.cleaned_data["body"]

        if body:
            if not (10 < len(body) < 100):
                raise forms.ValidationError("طول متن کامنت باید بین 10 تا 100 کاراکتر باشد!")
            else:
                return body


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data["title"]

        if title:
            if len(title) < 10:
                raise forms.ValidationError("موضوع نمیتواند کمتر از 10 کاراکتر باشد")
            else:
                return title

    def clean_description(self):
        description = self.cleaned_data["description"]

        if description:
            if len(description) < 50:
                raise forms.ValidationError("نوشته (توضیحات) پست نمیتواند کمتر از 50 کاراکتر باشد")
            else:
                return description


class SearchForm(forms.Form):
    query = forms.CharField()
