from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .models import Profile, Career, Plaсe, BusinessTrip, Unit, Element, Mismatch, Status
import datetime

#----------- Главная Main -----------
def index(request):
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    return render(
        request,
        'index.html',
        context={'title': "Портал"},
    )
#----------- Командировки  -----------

def business_trip(request):
    date_today = datetime.date.today()
    trips_current_user = BusinessTrip.objects.filter(activ__exact=True).filter(user_id__exact=request.user.pk)
    trips_completed_user = BusinessTrip.objects.filter(activ__exact=False).filter(user_id__exact=request.user.pk)
    trips_current = BusinessTrip.objects.filter(activ__exact=True)
    trips_completed = BusinessTrip.objects.filter(activ__exact=False)


    return render(
        request,
        'supervision/business_trip/business_trip.html',
        context={
            'title': 'Командировки', 'trips_current': trips_current,
            'trips_completed': trips_completed,
            'trips_current_user': trips_current_user,
            'trips_completed_user': trips_completed_user
        },
    )


#----------- Карточка Командировки  -----------

def trip(request, pk):
    date_today = datetime.date.today()
    trip = BusinessTrip.objects.get(pk=pk)


    return render(
        request,
        'supervision/business_trip/businesstrip_detail.html',
        context={
            'title': 'Командировка', 'trip': trip, 'date_today': date_today
        },
    )


#----------- Список Наосоответствий  -----------

def mismatch(request):
    mismatches = Mismatch.objects.all()
    palce = Plaсe.objects.filter(status__exact='a')

    return render(
        request,
        'supervision/mismatch.html',
        context={
            'title': 'Перечень несоответствий', 'mismatches': mismatches, 'palce': palce
        },
    )


#----------- карточка Наосоответствия  -----------

def mismatch_detail(request, pk):
    mismatch = Mismatch.objects.get(pk=pk)

    return render(
            request,
            'supervision/mismatch_detail.html',
            context={
                'title': 'Карточка Неоответствия', 'mismatch': mismatch
            },
        )



#---ФОРМЫ------
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import ExtensionBusinessTripForm

# @permission_required('catalog.can_mark_returned')

# Обработка формы продления командировки

def extension_business_trip(request, pk):
    trip_extens = get_object_or_404(BusinessTrip, pk=pk)

# If this is a POST request then process the Form data
    if request.method == 'POST':
        form = ExtensionBusinessTripForm(request.POST)
        if form.is_valid():
            # присваиваем значение их формы полю "end"
            trip_extens.end = form.cleaned_data['extension_date']
            trip_extens.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('business_trip'))
    else:

        form = ExtensionBusinessTripForm(initial={'extension_date': datetime.date.today()})

    return render(request, 'supervision/business_trip/business_trip_extension.html',
                  {'form': form, 'tripextens': trip_extens,'title':'Продление командировки'})

# ----------------Редактирование, обновление, удаление формы  командировки

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class BusinessTripCreate(CreateView):
    model = BusinessTrip
    fields = '__all__'

    class Meta:
        labels = {'plaсe': 'Объект', 'user': 'сотрудник',
                  'start': 'С', 'end': 'По', 'purpose': 'Цель',
                  'activ': 'дайствующая', }

class BusinessTripUpdate(UpdateView):
    model = BusinessTrip
    fields = '__all__'

class BusinessTripDelete(DeleteView):
    model = BusinessTrip
    success_url = reverse_lazy('business_trip')


# --------- Редактирование, обновление, удаление  формы  несоответствия
class MismatchCreate(CreateView):
    model = Mismatch
    fields = '__all__'

class MismatchUpdate(UpdateView):
    model = Mismatch
    fields = '__all__'

class MismatchDelete(DeleteView):
    model = Mismatch
    success_url = reverse_lazy('mismatch')


#--------------- Объекты----------------


def place_list(request):
    place_list = Plaсe.objects.all()

    return render(
        request,
        'supervision/place/place_list.html',
        context={
            'title': 'Список Объектов', 'place_list': place_list
        },
    )

def place_detail(request, pk):
    place_detail = Plaсe.objects.get(pk=pk)

    return render(
        request,
        'supervision/place/place_detail.html',
        context={
            'title': 'Объект', 'place_detail': place_detail
        },
    )

# --------- Редактирование, обновление, удаление  формы Объекта
class PlaсeCreate(CreateView):
    model = Plaсe
    fields = '__all__'

class PlaсeUpdate(UpdateView):
    model = Plaсe
    fields = '__all__'

class PlaсeDelete(DeleteView):
    model = Plaсe
    success_url = reverse_lazy('place_list')




#--------------- Узлы----------------
def unit_list(request):
    pass

def unit_detail(request):
    pass

# --------- Редактирование, обновление, удаление  формы Узла
class UnitCreate(CreateView):
    model = Unit
    fields = '__all__'

class UnitUpdate(UpdateView):
    model = Unit
    fields = '__all__'

class UnitDelete(DeleteView):
    model = Unit
    success_url = reverse_lazy('utin_list')



#--------------- Детали----------------
def element_list(request):
    pass

def element_detail(request):
    pass
# --------- Редактирование, обновление, удаление  формы чертеж
class ElementCreate(CreateView):
    model = Element
    fields = '__all__'

class ElementUpdate(UpdateView):
    model = Element
    fields = '__all__'

class ElementDelete(DeleteView):
    model = Element
    success_url = reverse_lazy('element_list')