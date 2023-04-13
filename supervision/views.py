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
    trips_current = BusinessTrip.objects.filter(activ__exact=True)
    trips_completed = BusinessTrip.objects.filter(activ__exact=False)


    return render(
        request,
        'supervision/business_trip.html',
        context={
            'title': 'Командировки', 'trips_current': trips_current,
            'trips_completed': trips_completed
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
            'title': 'Несоответствия', 'mismatches': mismatches, 'palce': palce
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