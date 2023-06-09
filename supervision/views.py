from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .models import *
import datetime

from django.urls import include

def pageNotFound(request, exception):
    return render(request, 'supervision/page404.html', context={'title': 'Страницы не существует'})
    # return redirect ('home', permanent=True) перенаправление на главную страницу , постоянный редирект,
    # если на выполняется условие или ошибка на станице



menu = (
    {'title': 'Главная', 'url_menu': 'index', 'image': 'supervision/image/home.png'},
    {'title': 'Командировки', 'url_menu': 'busines_trip', 'image': 'supervision/image/trippng'},
    {'title': 'Несоответствия', 'url_menu': 'mismatch_list', 'image': 'supervision/image/miath.png'},
    {'title': 'Сотрудники', 'url_menu': 'employee_list', 'image': 'supervision/image/employee.png'},
    {'title': 'Объекты', 'url_menu': 'place_detail', 'image': 'supervision/image/place.png'},

)

#----------- Главная Main -----------
def index(request):
    num_employeer = User.objects.filter(is_active=1).count()
    num_place = Place.objects.filter(status='Действующий').count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    # request.GET - список параметров передаваемых GET запросом /?name=gggg&age=233
    # request.POST - список параметров передаваемых POST запросом

    context = {
        'title': "Портал",
        'num_employeer': num_employeer,
        'num_place': num_place,
        'menu': menu
    }


    return render(
        request,
        'index.html',
        context=context,
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

def mismatch_list(request):
    mismatches = Mismatch.objects.all()
    place = Place.objects.filter(status__exact='prs')

    return render(
        request,
        'supervision/mismatch/mismatch.html',
        context={
            'title': 'Список несоответствий', 'mismatches': mismatches, 'place': place
        },
    )


#----------- карточка Наосоответствия  -----------

def mismatch_detail(request, pk):
    mismatch = Mismatch.objects.get(pk=pk)
    status = Tracking.objects.filter(mismatch=mismatch.pk)

    return render(
            request,
        'supervision/mismatch/mismatch_detail.html',
            context={
                'title': 'Карточка Неоответствия', 'mismatch': mismatch, 'status': status
            },
        )



#--- ФОРМЫ------
from .forms import *

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


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


# class MismatchCreate(CreateView):
#     model = Mismatch
#     fields = '__all__'

def mismatch_create(request):
    if request.method == 'POST':
        form = CreateMismatchForm(request.POST, request.FILES)

        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Mismatch.objects.create(**form.cleaned_data)
                return redirect('mismatch_list')
            except:
                form.add_error(None, "ошибка добавления несоответстия")
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        form = CreateMismatchForm()

    return render(request, 'supervision/mismatch/mismatch_create.html',
                      {'form': form, 'title': 'Несоответстиве'})

class MismatchUpdate(UpdateView):
    model = Mismatch
    fields = '__all__'

class MismatchDelete(DeleteView):
    model = Mismatch
    success_url = reverse_lazy('mismatch')


#--------------- Объекты----------------


def place_list(request):
    place_list = Place.objects.filter(status__exact='Действующий')

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

# class PlaceCreate(CreateView):
#     model = Place
#     fields = '__all__'

def place_create(request):
    if request.method == 'POST':
        form = CreatePlaceForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('place_list')
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        form = CreatePlaceForm()
    return render(request, 'supervision/place/place_create.html',
                      {'form': form, 'title': 'Несоответстиве'})


class PlaceUpdate(UpdateView):
    model = Place
    fields = '__all__'
    template_name = 'supervision/place/place_create.html'

class PlaceDelete(DeleteView):
    model = Place
    success_url = reverse_lazy('place_list')



#--------------- Группы  ----------------
def group_list(request, pk):
    group_list = Group.objects.filter(place_id__exact=pk)
    place_pk = pk
    return render(
        request,
        'supervision/group/group_list.html',
        context={
            'title': 'Список Групп', 'group_list': group_list, "place_pk": place_pk
        },
    )

def group_detail(request, pk):
    group_detail = Group.objects.get(pk=pk)

    return render(
        request,
        'supervision/group/group_detail.html',
        context={
            'title': 'Группа', 'group_detail': group_detail
        },
    )

# --------- Редактирование, обновление, удаление  формы Узла

class GroupCreate(CreateView):
    model = Group
    fields = '__all__'

class GroupUpdate(UpdateView):
    model = Group
    fields = '__all__'

class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')



#--------------- Чертежи----------------

def drawing_list(request):
    drawing_list = Drawing.objects.all()

    return render(
        request,
        'supervision/drawing/drawing_list.html',
        context={
            'title': 'Список Чертежей', 'drawing_list': drawing_list
        },
    )

def drawing_detail(request, pk):
    drawing_detail = Drawing.objects.get(pk=pk)

    return render(
        request,
        'supervision/drawing/drawing_detail.html',
        context={
            'title': 'Чертёж', 'drawing_detail': drawing_detail
        },
    )

# --------- Редактирование, обновление, удаление  формы чертеж

class DrawingCreate(CreateView):
    model = Drawing
    fields = '__all__'

class DrawingUpdate(UpdateView):
    model = Drawing
    fields = '__all__'

class DrawingDelete(DeleteView):
    model = Drawing
    success_url = reverse_lazy('drawing_list')


#--------------- Детали----------------

def detail_list(request):
    detail_list = Detail.objects.all()

    return render(
        request,
        'supervision/detail/detail_list.html',
        context={
            'title': 'Список Деталей', 'detail_list': detail_list
        },
    )

def detail_detail(request, pk):
    detail_detail = Detail.objects.get(pk=pk)

    return render(
        request,
        'supervision/detail/detail_detail.html',
        context={
            'title': 'Деталь', 'detail_detail': detail_detail
        },
    )

# --------- Редактирование, обновление, удаление  формы чертеж

class DetailCreate(CreateView):
    model = Detail
    fields = '__all__'

class DetailUpdate(UpdateView):
    model = Detail
    fields = '__all__'

class DetailDelete(DeleteView):
    model = Detail
    success_url = reverse_lazy('detail_list')


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
    current_position = Career.objects.filter(user_id=pk, end_date__exact=None)
    context = {
        'title': 'Сотрудник', 'employee_detail': employee_detail,
        'career_list': career_list, 'current_position': current_position[0].position
    }
    return render(
        request,
        'supervision/employee/employee_detail.html',
        context=context,
    )

# --------- Редактирование, обновление, удаление  формы сотрудники
class EmployeeCreate(CreateView):
    form_class = AddEmployeeForm # форма создания
    template_name = 'supervision/employee/employee_create.html' # адрес шаблона
    success_url = reverse_lazy('employee_list') # переадресация на страницу при успешном добавлении записи

    model = Profile

    fields = '__all__'
    # template_name =
    # выборка данных из модели в коллекции  -> object_list, для задания своей переменной использовать
    # context_object_name = 'имя переменной'
    # extra_context = {'title': 'Главная страница'}- для передачи статических доп. данных

    # def get_context_data(self, *, object_list=None, **kwargs):- для передачи динамических доп. данных
    #     context = super().get_context_data(**kwargs)
    #     context['menu'] = menu
    #     context = {'title': 'Главная страница'}
    #     return context

    # для получения конкртеных данных из модели
    # def get_queryset(self):
    #     return Profile.objects.filter(параметы выборки)




class EmployeeUpdate(UpdateView):
    model = Profile
    fields = '__all__'

class EmployeeDelete(DeleteView):
    model = Profile
    success_url = reverse_lazy('employee_list')


#--------------- Служебные письма----------------

def letter_list(request):
    letter_list = Letter.objects.all()

    return render(
        request,
        'supervision/letter/letter_list.html',
        context={
            'title': 'Список Служебных писем', 'letter_list': letter_list
        },
    )

def letter_detail(request, pk):
    letter_detail = Letter.objects.get(pk=pk)

    return render(
        request,
        'supervision/letter/letter_detail.html',
        context={
            'title': 'Служебное письмо', 'letter_detail': letter_detail
        },
    )

# --------- Редактирование, обновление, удаление  формы служебных писем

class LetterCreate(CreateView):
    model = Letter
    fields = '__all__'

class LetterUpdate(UpdateView):
    model = Letter
    fields = '__all__'

class LetterDelete(DeleteView):
    model = Letter
    success_url = reverse_lazy('letter_list')


#--------------- Технические решения----------------

def solution_list(request):
    solution_list = Solution.objects.all()

    return render(
        request,
        'supervision/solution/solution_list.html',
        context={
            'title': 'Список Технических решений', 'solution_list': solution_list
        },
    )

def solution_detail(request, pk):
    solution_detail = Solution.objects.get(pk=pk)

    return render(
        request,
        'supervision/solution/solution_detail.html',
        context={
            'title': 'Техническое решение', 'solution_detail': solution_detail
        },
    )

# --------- Редактирование, обновление, удаление  формы чертеж

class SolutionCreate(CreateView):
    model = Solution
    fields = '__all__'

class SolutionUpdate(UpdateView):
    model = Solution
    fields = '__all__'

class SolutionDelete(DeleteView):
    model = Solution
    success_url = reverse_lazy('solution_list')