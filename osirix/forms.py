from django import forms
from django.core import validators

class FormName(forms.Form):

    USER_CHOICES = (
        ('Travis', 'Travis'),
        ('Jeff', 'Jeff'),
        ('Howard', 'Howard')
    )

    input_user = forms.ChoiceField(choices=USER_CHOICES)
    file = forms.FileField(required=False)
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])


