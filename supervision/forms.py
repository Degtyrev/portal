from django import forms

from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.


class ExtensionBusinessTripForm(forms.Form):

    extension_date = forms.DateField(help_text="введите новую дату командировки", label="Дата продления")

    def clean_extension_date(self):
        data = self.cleaned_data['extension_date']
        # Проверка того, что дата не позднее чем сегодня.
        if data < datetime.date.today():
            raise ValidationError('Дата не может быть позже сегодняшней даты')
        # Помните, что всегда надо возвращать "очищенные" данные.
        return data