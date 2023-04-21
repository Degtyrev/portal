from django import forms

from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
import datetime
from .models import *

class ExtensionBusinessTripForm(forms.Form):

    extension_date = forms.DateField(help_text="введите новую дату командировки", label="Дата продления")

    def clean_extension_date(self):
        data = self.cleaned_data['extension_date']
        # Проверка того, что дата не позднее чем сегодня.
        if data < datetime.date.today():
            raise ValidationError('Дата не может быть позже сегодняшней даты')
        # Помните, что всегда надо возвращать "очищенные" данные.
        return data


from django.forms import ModelForm, Textarea, DateField, Select,CheckboxSelectMultiple,\
    CheckboxInput


class CreateBusinessTripModelForm(forms.ModelForm):
    class Meta:
        model = BusinessTrip
        fields = ('place', 'user', 'start', 'end', 'purpose', 'activ')
        labels = {'place': 'Объект', 'user': 'сотрудник',
                  'start': 'С', 'end': 'По', 'purpose': 'Цель',
                  'activ': 'дайствующая'}
        widgets = {
            # 'start': forms.DateField(attrs={'class': 'form-cont'}),
            # 'end': forms.DateField(attrs={'class': 'form-cont'}),
            'purpose': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
        help_texts = {'place': 'введите объект'}


class CreateMismatchForm(forms.Form):
    place = forms.ChoiceField()
    user = forms.ChoiceField()
    unit = forms.ChoiceField()
    status = forms.ChoiceField()
    element = forms.ChoiceField()
    title = forms.CharField(help_text=' Краткое описание')
    text = forms.CharField(help_text=' Полное описание')
    type = forms.CharField()
    letter = forms.CharField(help_text='Номер служебного письма')
    answer = forms.CharField(help_text='Ответ служебное письмо')
    solution = forms.CharField(help_text='Принятое решени')
    corrected = forms.CharField(help_text='Кем устранено')
    date_finding = forms.DateField(help_text='Дата')
    factory = forms.CharField(help_text='Изготовитель')
    pack = forms.CharField(help_text='Грузовое место')
    amount = forms.IntegerField(help_text='Количество')
    file = forms.FileField()
    image = forms.ImageField()



