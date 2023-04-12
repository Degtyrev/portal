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
    trips_current = BusinessTrip.objects.filter(end__gt=date_today)
    trips_completed = BusinessTrip.objects.filter(end__lt=date_today)


    return render(
        request,
        'supervision/business_trip.html',
        context={
            'title': 'Командировки', 'trips_current': trips_current,
            'trips_completed': trips_completed
        },
    )

def trip(request, pk):

    trip = BusinessTrip.objects.get(pk=pk)
    date_today = datetime.date.today()
    return render(
        request,
        'supervision/business_trip_detail.html',
        context={
            'title': 'Командировка', 'trip': trip, 'date_today': date_today
        },
    )

def mismatch(request):
    mismatches = Mismatch.objects.all()
    # for i in mismatches:
    #     print(i)
    # status = Status.objects.get(pk=mismatches.pk)

    return render(
        request,
        'supervision/mismatch.html',
        context={
            'title': 'Несоответствия', 'mismatches': mismatches
        },
    )

def mismatch_detail(request, pk):
    mismatch = Mismatch.objects.get(pk=pk)

    return render(
            request,
            'supervision/mismatch_detail.html',
            context={
                'title': 'Несоответствие', 'mismatch': mismatch
            },
        )