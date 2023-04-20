from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .models import Profile, Career, Place, BusinessTrip, Unit, Element, Mismatch, Status, User
import datetime

from django.urls import include

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
    place = Place.objects.filter(status__exact='a')

    return render(
        request,
        'supervision/mismatch/mismatch.html',
        context={
            'title': 'Перечень несоответствий', 'mismatches': mismatches, 'place': place
        },
    )


#----------- карточка Наосоответствия  -----------

def mismatch_detail(request, pk):
    mismatch = Mismatch.objects.get(pk=pk)

    return render(
            request,
        'supervision/mismatch/mismatch_detail.html',
            context={
                'title': 'Карточка Неоответствия', 'mismatch': mismatch
            },
        )



#--- ФОРМЫ------
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


# @permission_required('catalog.can_mark_returned')

# Обработка формы продления командировки
from .forms import ExtensionBusinessTripForm

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
                  {'form': form, 'tripextens': trip_extens, 'title':'Продление командировки'})

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

from .forms import MismatchForm

def mismatch_create(request):

    mismatch = Mismatch.objects.all()

    if request.method == 'POST':
        form = MismatchForm(request.POST)

        if form.is_valid():
            mismatch.place = form.cleaned_data['place']
            mismatch.user = form.cleaned_data['user']
            mismatch.unit = form.cleaned_data['unit']
            mismatch.status = form.cleaned_data['status']
            mismatch.element = form.cleaned_data['element']
            mismatch.title = form.cleaned_data['title']
            mismatch.text = form.cleaned_data['text']
            mismatch.type = form.cleaned_data['type']
            mismatch.letter = form.cleaned_data['letter']
            mismatch.answer = form.cleaned_data['answer']
            mismatch.solution = form.cleaned_data['solution']
            mismatch.corrected = form.cleaned_data['corrected']
            mismatch.date_finding = form.cleaned_data['date_finding']
            mismatch.factory = form.cleaned_data['factory']
            mismatch.pack = form.cleaned_data['pack']
            mismatch.amount = form.cleaned_data['amount']

            mismatch.save()

        return HttpResponseRedirect(reverse('mismatch'))
    else:
        place = BusinessTrip.objects.filter(user_id__exact=request.user.pk)
        # user = User.objects.filter(user_id__exact=request.user.pk)
        form = MismatchForm(initial={'place': place})

    return render(request, 'supervision/mismatch/mismatch_create_form.html',
                      {'form': form, 'place': place, 'title': 'Несоответстиве'})

class MismatchUpdate(UpdateView):
    model = Mismatch
    fields = '__all__'

class MismatchDelete(DeleteView):
    model = Mismatch
    success_url = reverse_lazy('mismatch')


#--------------- Объекты----------------


def place_list(request):
    place_list = Place.objects.all()

    return render(
        request,
        'supervision/place/place_list.html',
        context={
            'title': 'Список Объектов', 'place_list': place_list
        },
    )

def place_detail(request, pk):
    place_detail = Place.objects.get(pk=pk)

    return render(
        request,
        'supervision/place/place_detail.html',
        context={
            'title': 'Объект', 'place_detail': place_detail
        },
    )

# --------- Редактирование, обновление, удаление  формы Объекта
class PlaceCreate(CreateView):
    model = Place
    fields = '__all__'

class PlaceUpdate(UpdateView):
    model = Place
    fields = '__all__'

class PlaceDelete(DeleteView):
    model = Place
    success_url = reverse_lazy('place_list')



#--------------- Узлы----------------
def unit_list(request):
    unit_list = Unit.objects.all()

    return render(
        request,
        'supervision/unit/unit_list.html',
        context={
            'title': 'Список Узлов', 'unit_list': unit_list
        },
    )

def unit_detail(request, pk):
    unit_detail = Unit.objects.get(pk=pk)

    return render(
        request,
        'supervision/unit/unit_detail.html',
        context={
            'title': 'Узел', 'unit_detail': unit_detail
        },
    )

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
    element_list = Element.objects.all()

    return render(
        request,
        'supervision/element/element_list.html',
        context={
            'title': 'Список Деталей', 'element_list': element_list
        },
    )

def element_detail(request, pk):
    element_detail = Element.objects.get(pk=pk)

    return render(
        request,
        'supervision/element/element_detail.html',
        context={
            'title': 'Чертёж', 'element_detail': element_detail
        },
    )

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

#--------------- Сотрудники----------------
def employee_list(request):
    employee_list = Profile.objects.all()

    return render(
        request,
        'supervision/employee/employee_list.html',
        context={
            'title': 'Список Сотрудников', 'employee_list': employee_list
        },
    )

def employee_detail(request, pk):
    employee_detail = Profile.objects.get(user_id=pk)
    career_list = Career.objects.filter(user_id=pk)

    return render(
        request,
        'supervision/employee/employee_detail.html',
        context={
            'title': 'Сотрудник', 'employee_detail': employee_detail,
            'career_list': career_list
        },
    )

# --------- Редактирование, обновление, удаление  формы сотрудники
class EmployeeCreate(CreateView):
    model = Profile
    fields = '__all__'

class EmployeeUpdate(UpdateView):
    model = Profile
    fields = '__all__'

class EmployeeDelete(DeleteView):
    model = Profile
    success_url = reverse_lazy('employee_list')