from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .models import Profile, Career, Objects, BusinessTrip, Unit, Element, Mismatch, Status

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
    trip = BusinessTrip.objects.all()

    return render(
        request,
        'supervision/business_trip.html',
        context={
            'title': 'Командировки', 'trip': trip
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