from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .models import Profile, Career, Plaсe, BusinessTrip, Unit, Element, Mismatch, Status
import datetime


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

def business_trip(request):
    date_today = datetime.date.today()
    trips_current_user = BusinessTrip.objects.filter(activ__exact=True).filter(user_id__exact=request.user.pk)
    trips_completed_user = BusinessTrip.objects.filter(activ__exact=False).filter(user_id__exact=request.user.pk)
    trips_current = BusinessTrip.objects.filter(activ__exact=True)
    trips_completed = BusinessTrip.objects.filter(activ__exact=False)


    return render(
        request,
        'supervision/business_trip.html',
        context={
            'title': 'Командировки', 'trips_current': trips_current,
            'trips_completed': trips_completed,
            'trips_current_user': trips_current_user,
            'trips_completed_user': trips_completed_user
        },
    )

def trip(request, pk):
    date_today = datetime.date.today()
    trip = BusinessTrip.objects.get(pk=pk)


    return render(
        request,
        'supervision/business_trip_detail.html',
        context={
            'title': 'Командировка', 'trip': trip, 'date_today': date_today
        },
    )

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

    return render(request, 'supervision/business_trip_extension.html',
                  {'form': form, 'tripextens': trip_extens,'title':'Продление командировки'})