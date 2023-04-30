from django import forms

from django.core.exceptions import ValidationError
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


# class CreateBusinessTripForm(forms.Form):
#     place = forms.ModelChoiceField(queryset=Place.objects.filter(status__exact=2),
#                                    label='Оъект', empty_label='Выберите Объект')
#     user = forms.ModelChoiceField(queryset=Profile.objects.all(), label='Cотрудник',
#                                   empty_label='Выберите Сотрудника')
#     start = forms.DateField(label='Дата начала командировки')
#     end = forms.DateField(label='Дата окончания командировки')
#     purpose = forms.CharField(max_length=250,
#                               widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
#                               label='Цель командировки')

# initial=datetime.date.today()

class CreateBusinessTripForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place'].empty_label = 'Выберите Объект'
        self.fields['user'].empty_label = 'Сотрудник не выбран'

    class Meta:
        model = BusinessTrip
        fields = ['place', 'user', 'start', 'end', 'purpose', 'status']
        labels = {'place': 'Объект', 'user': 'Cотрудник',
                  'start': 'Дата начала командировки',
                  'end': 'Дата окончания командировки',
                  'purpose': 'Цель командировки',
                  'status': 'Состояние командировки'}
        widgets = {
            'place': forms.Select(attrs={'class': 'form_input'}),
            'user': forms.Select(attrs={'class': 'form_input'}),
            'start': forms.DateInput(attrs={'class': 'form_input'}),
            'end': forms.DateInput(attrs={'class': 'form_input'}),
            'purpose': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form_input'}),
            'status': forms.Select(attrs={'disabled': True, 'class': 'form_input'}),
        }


# Проверка на недопущения даты начала и конца в прошлом
    # def clean_start(self):
    #     start = self.cleaned_data['start']
    #
    #     if start < datetime.date.today():
    #         raise ValidationError('Начало командировки не может быть в прошлом')
    #     return start
    #
    # def clean_end(self):
    #     end = self.cleaned_data['end']
    #     if end < datetime.date.today():
    #         raise ValidationError('Окончание командировки не может быть в прошлом')
    #     return end


class CreateMismatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place'].empty_label = 'Выберите Объект'

    class Meta:
        model = Mismatch
        fields = ['place', 'type',  'title', 'text', 'file', 'image']
        labels = {'place': 'Объект',
                  'type': 'Тип несоответстия',
                  'details': 'Деталь',
                  'title': 'Короткое описание',
                  'text': 'Описание',
                  'file': 'Файлы',
                  'image': 'Фото',
                  }
        widgets = {
            'place': forms.Select(attrs={'class': 'form_input', 'autocomplete': 'on'}),
            'type': forms.RadioSelect(attrs={'class': 'form_input radio_input', 'checked':1}),
            # 'details': forms.Select(attrs={'class': 'form_input', 'required': 'False'}),
            'title': forms.TextInput(attrs={'class': 'form_input'}),
            'text': forms.Textarea(attrs={'class': 'form_input', 'cols': 80, 'rows': 5}),
            'file': forms.FileInput(attrs={'class': 'form_input'}),
            'image': forms.FileInput(attrs={'class': 'form_input'}),
        }

    # place = forms.ModelChoiceField(queryset=Place.objects.all(),
    #                                label='объект', empty_label='выберите объект',
    #                                widget=forms.Select(attrs={'class': 'form_input', 'autocomplete': 'on'}))
    # type = forms.ChoiceField(label='тип несоответстия', widget=forms.RadioSelect(attrs={'class': 'form_input'}))
    # status = forms.ModelChoiceField(queryset=Status.objects.all(), label='статус',
    #                                 widget=forms.Select(attrs={'class': 'form_input'}),
    #                                 empty_label=None)
    # details = forms.ModelChoiceField(queryset=Detail.objects.all(), label='детали',
    #                                  widget=forms.Select(attrs={'class': 'form_input'}),
    #                                  empty_label='выберите деталь', required=False)
    # title = forms.CharField(label='кратко', widget=forms.TextInput(attrs={'class': 'form_input'}))
    # text = forms.CharField(label='описание', widget=forms.Textarea(attrs={'class': 'form_input'}))
    # quantity = forms.IntegerField(label='количество', widget=forms.NumberInput(attrs={'class': 'form_input'}))
    # file = forms.FileField(label='файлы', widget=forms.FileInput(attrs={'class': 'form_input'}), required=False)
    # image = forms.ImageField(label='фото', widget=forms.FileInput(attrs={'class': 'form_input'}), required=False)



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
            'status': forms.Select(attrs={'class': 'form_input'}),
        }

