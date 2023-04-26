from django import forms

from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
import datetime
from .models import *

class ExtensionBusinessTripForm(forms.Form):

    extension_date = forms.DateField(help_text="введите новую дату командировки",
                                    widget=forms.TextInput(attrs={'class': 'form_input input_date'}),
                                    label="Продлить до:")

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
    place = forms.ModelChoiceField(queryset=Place.objects.all(),
                                   label='объект', empty_label='выберите объект',
                                   widget=forms.Select(attrs={'class': 'form_input', 'autocomplete': 'on'}))
    type = forms.ChoiceField(label='тип несоответстия', widget=forms.RadioSelect(attrs={'class': 'form_input'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='статус',
                                    widget=forms.Select(attrs={'class': 'form_input'}),
                                    empty_label=None)
    details = forms.ModelChoiceField(queryset=Detail.objects.all(), label='детали',
                                     widget=forms.Select(attrs={'class': 'form_input'}),
                                     empty_label='выберите деталь', required=False)
    title = forms.CharField(label='кратко', widget=forms.TextInput(attrs={'class': 'form_input'}))
    text = forms.CharField(label='описание', widget=forms.Textarea(attrs={'class': 'form_input'}))
    quantity = forms.IntegerField(label='количество', widget=forms.NumberInput(attrs={'class': 'form_input'}))
    file = forms.FileField(label='файлы', widget=forms.FileInput(attrs={'class': 'form_input'}), required=False)
    image = forms.ImageField(label='фото', widget=forms.FileInput(attrs={'class': 'form_input'}), required=False)



class CreatePlaceForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['status'].empty_lable = 'Категория не выбрана'
    class Meta:
        model = Place
        fields = ['name', 'equipment', 'equipment_type', 'contract', 'project_manager',
                  'chief_engineer', 'order', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
            'equipment': forms.TextInput(attrs={'class': 'form_input'}),
            'equipment_type': forms.TextInput(attrs={'class': 'form_input'}),
            'contract': forms.TextInput(attrs={'class': 'form_input'}),
            'project_manager': forms.TextInput(attrs={'class': 'form_input'}),
            'chief_engineer': forms.TextInput(attrs={'class': 'form_input'}),
            'order': forms.NumberInput(attrs={'class': 'form_input'}),
            'status': forms.Select(attrs={'class': 'form_input', 'autocomplete': 'on'}),
        }


class AddEmployeeForm(forms.Form):
    pass
