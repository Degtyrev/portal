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
        fields = ['place', 'type',  'title', 'text', 'file', 'image', 'details', 'correct','status']
        labels = {'place': 'Объект',
                  'type': 'Тип несоответстия',
                  'details': 'Детали',
                  'title': 'Короткое описание',
                  'correct': 'Предложения по устранению',
                  'text': 'Описание',
                  'file': 'Файлы',
                  'image': 'Фото',
                  }
        widgets = {
            'place': forms.Select(attrs={'class': 'form_input'}),
            'type': forms.RadioSelect(attrs={'class': 'form_input radio_input'}), #, 'checked': 1
            'details': forms.Textarea(attrs={'class': 'form_input', 'required': 'False', 'cols': 80, 'rows': 5}),
            'correct': forms.Textarea(attrs={'class': 'form_input', 'required': 'False', 'cols': 80, 'rows': 5}),
            'title': forms.TextInput(attrs={'class': 'form_input'}),
            'text': forms.Textarea(attrs={'class': 'form_input', 'cols': 80, 'rows': 5}),
            'file': forms.FileInput(attrs={'class': 'form_input'}),
            'image': forms.FileInput(attrs={'class': 'form_input'}),
            # 'status': forms.Select(attrs={'class': 'form_input', 'disabled': True, 'checked': 1}),
            'status': forms.HiddenInput(),
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



class CreateLetterForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['place'].empty_label = 'Выберите Объект'

    class Meta:
        model = Letter
        fields = ['number', 'date', 'title', 'text', 'user',
                  'to', 'mismatch', 'file', 'image']
        labels = {'number': 'Номер письма СП-',
                  'date': 'Дата',
                  'title': 'Тема',
                  'text': 'Текст письма',
                  'user': 'От кого',
                  'to': 'Кому',
                  'mismatch': 'Несоответстивие',
                  'file': 'Файлы',
                  'image': 'Фото',
                  }
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form_input'}),
            'date': forms.DateInput(attrs={'class': 'form_input'}),
            'title': forms.TextInput(attrs={'class': 'form_input'}),
            'text': forms.Textarea(attrs={'class': 'form_input', 'cols': 80, 'rows': 5}),
            'user': forms.Select(attrs={'class': 'form_input'}),
            'to': forms.TextInput(attrs={'class': 'form_input'}),
            'mismatch': forms.Select(attrs={'class': 'form_input'}), # 'disabled': True
            'file': forms.FileInput(attrs={'class': 'form_input'}),
            'image': forms.FileInput(attrs={'class': 'form_input'}),
        }


class CreateSolutionForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['place'].empty_label = 'Выберите Объект'

    class Meta:
        model = Solution
        fields = ['number', 'date', 'title', 'text', 'user',
                  'to', 'mismatch', 'file']
        labels = {'number': 'Номер письма СП-',
                  'date': 'Дата',
                  'title': 'Тема',
                  'text': 'Текст письма',
                  'user': 'От кого',
                  'to': 'Кому',
                  'mismatch': 'Несоответстивие',
                  'file': 'Файлы',
                  }
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form_input'}),
            'date': forms.DateInput(attrs={'class': 'form_input'}),
            'title': forms.TextInput(attrs={'class': 'form_input'}),
            'text': forms.Textarea(attrs={'class': 'form_input', 'cols': 80, 'rows': 5}),
            'user': forms.Select(attrs={'class': 'form_input'}), #, 'disabled': True
            'to': forms.TextInput(attrs={'class': 'form_input'}),
            'mismatch': forms.Select(attrs={'class': 'form_input'}),
            'file': forms.FileInput(attrs={'class': 'form_input'}),
        }

class CreateGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].empty_label = 'Выберите Родительскую Группу'

    class Meta:
        model = Group
        fields = ['place', 'parent', 'number', 'suffix', 'name']
        labels = {'place': 'Объект',
                  'parent': 'Номер родительской группы',
                  'number': 'Номер группы',
                  'suffix': 'Суффекс',
                  'name': 'Наименование группы',
                  }
        widgets = {
            'place': forms.Select(attrs={'class': 'form_input'}),
            'parent': forms.Select(attrs={'class': 'form_input'}),
            'number': forms.NumberInput(attrs={'class': 'form_input'}),
            'suffix': forms.TextInput(attrs={'class': 'form_input'}),
            'name': forms.TextInput(attrs={'class': 'form_input'}),

        }

# class CreateDrawingForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['group'].empty_label = 'Выберите Группу'
#
#     class Meta:
#         model = Drawing
#         fields = ['group', 'number', 'name', 'mass', 'steel', 'file']
#         labels = {'group': 'Группа',
#                   'number': 'Обозначение',
#                   'name': 'Наименование',
#                   'mass': 'Масса',
#                   'steel': 'Материал',
#                   'file': 'Файлы',
#                   }
#         widgets = {
#             'group': forms.Select(attrs={'class': 'form_input'}),
#             'number': forms.TextInput(attrs={'class': 'form_input'}),
#             'name': forms.TextInput(attrs={'class': 'form_input'}),
#             'mass': forms.NumberInput(attrs={'class': 'form_input'}),
#             'steel': forms.TextInput(attrs={'class': 'form_input'}),
#             'file': forms.FileInput(attrs={'class': 'form_input'}),
#
#         }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'username': 'Логин',
                  'first_name': 'Имя',
                  'last_name': 'Фималия',
                  'email': 'Почта',
                  }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_input'}),
            'first_name': forms.TextInput(attrs={'class': 'form_input'}),
            'last_name': forms.TextInput(attrs={'class': 'form_input'}),
            'email': forms.TextInput(attrs={'class': 'form_input'}),

        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['surname', 'birth_date', 'death_date', 'is_liner', 'photo']
        labels = {'surname': 'Отчество',
                  'birth_date': 'Дата рождения',
                  'death_date': 'Дата смерти',
                  'is_liner': 'Линейный',
                  'photo': 'Фото',
                  }
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form_input'}),
            'birth_date': forms.DateInput(attrs={'class': 'form_input input_date'}),
            'death_date': forms.DateInput(attrs={'class': 'form_input input_date'}),
            'is_liner': forms.CheckboxInput(attrs={'class': 'form_input checkbox_input'}),
            'photo': forms.FileInput(attrs={'class': 'form_input'}),
        }