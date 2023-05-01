import os.path

from django.contrib.auth.views import LoginView
from django.db.models import Max
from django.shortcuts import render, redirect
from .models import *
import datetime

from django.urls import include


# ___ for forms
from .forms import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime



def pageNotFound(request, exception):
    return render(request, 'supervision/page404.html', context={'title': 'Страницы не существует'})
    # return redirect ('home', permanent=True) перенаправление на главную страницу , постоянный редирект,
    # если на выполняется условие или ошибка на станице



menu = [
    {'title_menu': 'Главная', 'url_menu': 'index', 'image': 'supervision/image/home.png'},
    {'title_menu': 'Командировки', 'url_menu': 'business_trip', 'image': 'supervision/image/trip.png'},
    {'title_menu': 'Несоответствия', 'url_menu': 'mismatch', 'image': 'supervision/image/mismatch.png'},
    {'title_menu': 'Сотрудники', 'url_menu': 'employee', 'image': 'supervision/image/employee.png'},
    {'title_menu': 'Объекты', 'url_menu': 'place', 'image': 'supervision/image/place.png'},

]

#----------- Главная Main -----------
def index(request):
    num_employeer = User.objects.filter(is_active=1).count()
    num_place = Place.objects.filter(status=2).count()  # Метод 'all()' применён по умолчанию.

    activ_trip = BusinessTrip.objects.filter(user_id__exact=request.user.pk, status_id__exact=2)
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    # request.GET - список параметров передаваемых GET запросом /?name=gggg&age=233
    # request.POST - список параметров передаваемых POST запросом

    context = {
        'title': "Портал",
        'num_employeer': num_employeer,
        'num_place': num_place,
        'activ_trip': activ_trip[0]
    }

    return render(
        request,
        'index.html',
        context=context,
    )

#----------- Страница добавления админка -----------
def admin_page(request):

    context = {
        'title': "Административная страница",
    }

    return render(
        request,
        'supervision/settings/admin_page.html',
        context=context,
    )



#----------- Командировки  -----------

def business_trip(request):
    date_today = datetime.date.today()
    trips_user = BusinessTrip.objects.filter(status__exact=2).filter(user_id__exact=request.user.pk)
    trips = BusinessTrip.objects.filter(status__exact=2)
    conditions = ConditionTrip.objects.all()

    return render(
        request,
        'supervision/business_trip/business_trip.html',
        context={
            'title': 'Список Командировок',
            'trips_user': trips_user,
            'trips': trips,

            'conditions': conditions,
            'condition_selected': 2,
        },
    )


def condition_show(request, pk):
    trips_user = BusinessTrip.objects.filter(status__exact=pk).filter(user_id__exact=request.user.pk)
    trips = BusinessTrip.objects.filter(status__exact=pk)
    conditions = ConditionTrip.objects.all()

    # day_now = date.today()
    # new={}
    # for tu in trips_user:
    #     new[tu.pk]=tu
    #     new[tu.pk].balans = tu.end - day_now



    return render(
        request,
        'supervision/business_trip/business_trip.html',
        context={
            'title': 'Список Командировок',
            'trips_user': trips_user,
            'trips': trips,
            'conditions': conditions,
            'condition_selected': pk,

        },
    )


#----------- Карточка Командировки  -----------

def trip(request, pk):
    date_today = datetime.date.today()
    trip = BusinessTrip.objects.get(pk=pk)

    context = {
                'title': 'Командировка',
                'trip': trip,
                'date_today': date_today,
              }

    return render(
        request,
        'supervision/business_trip/businesstrip_detail.html',
        context=context,
    )
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
def business_trip_create(request):

    if request.method == 'POST':
        form = CreateBusinessTripForm(request.POST)

        # print(form.cleaned_data['end'])
        if form.is_valid():
            start = datetime.datetime.strptime(request.POST['start'], '%d.%m.%Y').date()
            end = datetime.datetime.strptime(request.POST['end'], '%d.%m.%Y').date()
            user = request.POST['user']
            # print(start)
            # print(end)
            # print(user)
            carent_trip = BusinessTrip.objects.filter(user__exact=user).filter(status__exact=2)

            date_end_carent_trip = carent_trip[0].end
            try:
                if start < date_end_carent_trip: # если дата следующей командировки раньще конца текущей
                    raise Exception(form.add_error(None, f'Сотрудник находится в командировке до {date_end_carent_trip}'))

                if start > end :# если дата начала позже даты завершения
                    raise Exception(form.add_error(None, 'Дата начала командировки позже даты завершения'))

                form.save()
                return redirect('business_trip')
                    # BusinessTrip.objects.create(**form.cleaned_data)

            except Exception:
                 form.add_error(None, error='')
    else:
        form = CreateBusinessTripForm()
    return render(request, 'supervision/business_trip/businesstrip_form.html',
                  {'title': 'Добавление командировки', 'form': form})


# class BusinessTripCreate(CreateView):
#     model = BusinessTrip
#     template_name = 'supervision/business_trip/businesstrip_form.html'
#     # fields = ['name', 'equipment', 'equipment_type', 'contract',
#     #           'project_manager', 'chief_engineer', 'order', 'status']
#     # success_url = reverse_lazy('business_trip_detail')
#     fields = "__all__"


class BusinessTripUpdate(UpdateView):
    model = BusinessTrip
    template_name = 'supervision/business_trip/businesstrip_form.html'
    # fields = ['name', 'equipment', 'equipment_type', 'contract',
    #           'project_manager', 'chief_engineer', 'order', 'status']
    fields = "__all__"
    # success_url = reverse_lazy('business_trip_detail')


class BusinessTripDelete(DeleteView):
    model = BusinessTrip
    template_name = 'supervision/business_trip/businesstrip_confirm_delete.html'
    success_url = reverse_lazy('business_trip')


#----------- Список Наосоответствий  -----------

def mismatch_list(request):
    mismatches = Mismatch.objects.select_related().all()
    # n = {}
    # for mismatche in mismatches:
    #     track = Tracking.objects.filter(mismatch_id__exact=mismatche.id)
    #     n['track'] = track
    #     n = mismatche
    print(mismatches)
    place = Place.objects.filter(status__exact=2)


    return render(
        request,
        'supervision/mismatch/mismatch.html',
        context={
            'title': 'Список несоответствий',
            'mismatches': mismatches,
            'place': place,

        },
    )


#----------- карточка Наосоответствия  -----------

def mismatch_detail(request, pk):
    mismatch = Mismatch.objects.get(pk=pk)
    status = Tracking.objects.filter(mismatch=mismatch.pk)
    letters = Letter.objects.filter(mismatch=mismatch.pk)
    solutions = Solution.objects.filter(mismatch=mismatch.pk)

    return render(
            request,
        'supervision/mismatch/mismatch_detail.html',
            context={
                'title': 'Карточка Неоответствия',
                'mismatch': mismatch,
                'status': status,
                'letters': letters,
                'solutions': solutions,
            },
        )

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
    place_list = Place.objects.filter(status__exact=2)
    place_status = PlaceStatus.objects.all()
    return render(
        request,
        'supervision/place/place_list.html',
        context={
            'title': 'Список Объектов',
            'place_list': place_list,
            'place_status': place_status,
            'place_selected': 2,
        },
    )

def place_detail(request, pk):
    place_detail = Place.objects.get(pk=pk)

    return render(
        request,
        'supervision/place/place_detail.html',
        context={
            'title': 'Объект',
            'place_detail': place_detail,
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
        form = CreatePlaceForm(initial={'status': 1})
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
            'title': 'Список Групп',
            'group_list': group_list,
            "place_pk": place_pk,
            'menu': menu
        },
    )

def group_detail(request, pk):
    group_detail = Group.objects.get(pk=pk)

    return render(
        request,
        'supervision/group/group_detail.html',
        context={
            'title': 'Группа',
            'group_detail': group_detail,
            'menu': menu
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
            'title': 'Список Чертежей',
            'drawing_list': drawing_list,
            'menu': menu
        },
    )

def drawing_detail(request, pk):
    drawing_detail = Drawing.objects.get(pk=pk)

    return render(
        request,
        'supervision/drawing/drawing_detail.html',
        context={
            'title': 'Чертёж',
            'drawing_detail': drawing_detail,
            'menu': menu
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
            'title': 'Список Деталей',
            'detail_list': detail_list,
            'menu': menu
        },
    )

def detail_detail(request, pk):
    detail_detail = Detail.objects.get(pk=pk)

    return render(
        request,
        'supervision/detail/detail_detail.html',
        context={
            'title': 'Деталь',
            'detail_detail': detail_detail,
            'menu': menu
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
    employee_list = User.objects.all()

    return render(
        request,
        'supervision/employee/employee_list.html',
        context={
            'title': 'Список Сотрудников',
            'employee_list': employee_list,

        },
    )

def employee_detail(request, pk):
    employee_detail = User.objects.get(id=pk)
    # profile_detail = Profile.objects.get(id=pk)
    career_list = Career.objects.filter(user_id=pk)
    current_position = Career.objects.filter(user_id=pk, end_date__exact=None)
    context = {
        'title': 'Сотрудник', 'employee_detail': employee_detail,
        'career_list': career_list, 'current_position': current_position
    }
    return render(
        request,
        'supervision/employee/employee_detail.html',
        context=context,
    )

# --------- Редактирование, обновление, удаление  формы сотрудники

# -----   СОТРУДНИКА ДОБАВЛЯЕТ АДМИН!!!!
#  ----   СОТРУДНИКА НЕЛЬЗЯ УДАЛИТЬ!!!

# class EmployeeCreate(CreateView):
#     form_class = AddEmployeeForm # форма создания
#     template_name = 'supervision/employee/employee_create.html' # адрес шаблона
#     success_url = reverse_lazy('employee_list') # переадресация на страницу при успешном добавлении записи
#
#     model = Profile
#
#     fields = '__all__'
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


#--------------- Служебные письма----------------

def letter_list(request):
    letter_list = Letter.objects.all()

    return render(
        request,
        'supervision/letter/letter_list.html',
        context={
            'title': 'Список Служебных писем',
            'letter_list': letter_list,

        },
    )

def letter_detail(request, pk):
    letter = Letter.objects.get(pk=pk)

    return render(
        request,
        'supervision/letter/letter_detail.html',
        context={
            'title': 'Служебное письмо',
            'letter': letter,
        },
    )

# --------- Редактирование, обновление, удаление  формы служебных писем

# class LetterCreate(CreateView):
#     model = Letter
#     fields = '__all__'
def letter_create(request):
    if request.method == 'POST':
        form = CreateLetterForm(request.POST, request.FILES)

        if form.is_valid():
            # print(form.cleaned_data)
            try:
                form.save()
                return redirect('letter_list')
            except:
                form.add_error(None, "Ошибка добавления Служебного письма")
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        mismatch_id = request.GET['mismatch_id']
        form = CreateLetterForm(initial={'user': request.user, 'mismatch': mismatch_id})

    return render(request, 'supervision/letter/letter_create.html',
                      {'form': form, 'title': 'Служебное письмо в ОШМ'})


class LetterUpdate(UpdateView):
    model = Letter
    fields = '__all__'
    template_name = 'supervision/letter/letter_create.html'
    success_url = reverse_lazy('letter_list')

# class LetterDelete(DeleteView):
#     model = Letter
#     success_url = reverse_lazy('letter_list')


#--------------- Технические решения----------------

def solution_list(request):
    solution_list = Solution.objects.all()

    return render(
        request,
        'supervision/solution/solution_list.html',
        context={
            'title': 'Список Технических решений',
            'solution_list': solution_list,

        },
    )

def solution_detail(request, pk):
    solution_detail = Solution.objects.get(pk=pk)

    return render(
        request,
        'supervision/solution/solution_detail.html',
        context={
            'title': 'Техническое решение',
            'solution_detail': solution_detail,

        },
    )

# --------- Редактирование, обновление, удаление  формы чертеж

def solution_create(request):
    if request.method == 'POST':
        form = CreateLetterForm(request.POST, request.FILES)

        if form.is_valid():
            # print(form.cleaned_data)
            try:
                form.save()
                return redirect('letter_list')
            except:
                form.add_error(None, "Ошибка добавления Служебного письма")
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        mismatch_id = request.GET['mismatch_id']
        form = CreateLetterForm(initial={'user': request.user, 'mismatch': mismatch_id})

    return render(request, 'supervision/letter/letter_create.html',
                      {'form': form, 'title': 'Служебное письмо в ОШМ'})

class SolutionUpdate(UpdateView):
    model = Solution
    fields = '__all__'

# class SolutionDelete(DeleteView):
#     model = Solution
#     success_url = reverse_lazy('solution_list')



#--------------- Статус объекта ----------------

def place_status_list(request):
    place_status_list = PlaceStatus.objects.all()

    return render(
        request,
        'supervision/place/place_status_list.html',
        context={
            'title': 'Список статусов Объектов',
            'place_status_list': place_status_list,

        },
    )

# def place_status_detail(request, pk):
#     place_status_detail = PlaceStatus.objects.get(pk=pk)
#
#     return render(
#         request,
#         'supervision/place/place_status_detail.html',
#         context={
#             'title': 'Статус объекта',
#             'place_status_detail': place_status_detail,
#
#         },
#     )

def place_status_show(request, pk):
    place_list = Place.objects.filter(status__exact=pk)
    place_status = PlaceStatus.objects.all()

    return render(
        request,
        'supervision/place/place_list.html',
        context={
            'title': 'Список Объектов',
            'place_list': place_list,
            'place_status': place_status,
            'place_selected': pk,
        },
    )

# --------- Редактирование, обновление, удаление  формы чертеж

class PlaceStatusCreate(CreateView):
    model = PlaceStatus
    template_name = 'supervision/place/placestatus_form.html'
    fields = ['name']
    success_url = reverse_lazy('place_status_list')




class PlaceStatusUpdate(UpdateView):
    model = PlaceStatus
    template_name = 'supervision/place/placestatus_form.html'
    fields = ['name']
    success_url = reverse_lazy('place_status_list')

class PlaceStatusDelete(DeleteView):
    model = PlaceStatus
    template_name = 'supervision/place/placestatus_confirm_delete.html'
    success_url = reverse_lazy('place_status_list')


#--------------- Типы несоответствий ----------------

def type_mismatch_list(request):
    type_mismatch_list = TypeMismatch.objects.all()

    return render(
        request,
        'supervision/mismatch/type_mismatch_list.html',
        context={
            'title': 'Список Типов носооветствий',
            'type_mismatch_list': type_mismatch_list,

        },
    )

# def type_mismatch_detail(request, pk):
#     type_mismatch_detail = PlaceStatus.objects.get(pk=pk)
#
#     return render(
#         request,
#         'supervision/mismatch/type_mismatch_detail.html',
#         context={
#             'title': 'Тип несоответствия',
#             'type_mismatch_detail': type_mismatch_detail,
#
#         },
#     )

def type_mismatch_show(request, status_id):
    # type_mismatch_list = Place.objects.filter(status__exact=status_id)
    # place_status = PlaceStatus.objects.all()
    #
    # return render(
    #     request,
    #     'supervision/place/place_list.html',
    #     context={
    #         'title': 'Список Объектов',
    #         'place_list': place_list,
    #         'place_status': place_status,
    #         'place_selected': status_id,
    #     },
    # )
    pass

# --------- Редактирование, обновление, удаление  формы чертеж

class TypeMismatchCreate(CreateView):
    model = TypeMismatch
    template_name = 'supervision/mismatch/typemismatch_form.html'
    fields = ['name']
    success_url = reverse_lazy('type_mismatch_list')

class TypeMismatchUpdate(UpdateView):
    model = TypeMismatch
    template_name = 'supervision/mismatch/typemismatch_form.html'
    fields = ['name']
    success_url = reverse_lazy('type_mismatch_list')

class TypeMismatchDelete(DeleteView):
    model = TypeMismatch
    template_name = 'supervision/mismatch/typemismatch_confirm_delete.html'
    fields = ['name']
    success_url = reverse_lazy('type_mismatch_list')


#--------------- Должности ----------------

def position_list(request):
    position_list = Position.objects.all()

    return render(
        request,
        'supervision/position/position_list.html',
        context={
            'title': 'Список Должностей',
            'position_list': position_list,
        },
    )


# --------- Редактирование, обновление, удаление  формы чертеж
class PositionCreate(CreateView):
    model = Position
    template_name = 'supervision/position/positino_form.html'
    fields = ['name']
    success_url = reverse_lazy('position_list')

class PositionUpdate(UpdateView):
    model = Position
    template_name = 'supervision/position/positino_form.html'
    fields = ['name']
    success_url = reverse_lazy('position_list')

class PositionDelete(DeleteView):
    model = Position
    template_name = 'supervision/position/position_confirm_delete.html'
    fields = ['name']
    success_url = reverse_lazy('position_list')




#--------------- Состояние командировки ----------------

def condition_trip_list(request):
    condition_trip_list = ConditionTrip.objects.all()

    return render(
        request,
        'supervision/business_trip/condition_trip_list.html',
        context={
            'title': 'Список Состояний Командировки',
            'condition_trip_list': condition_trip_list,
        },
    )


# --------- Редактирование, обновление, удаление  формы чертеж
class ConditionTripCreate(CreateView):
    model = ConditionTrip
    template_name = 'supervision/business_trip/conditiontrip_form.html'
    fields = ['name']
    success_url = reverse_lazy('condition_trip_list')

class ConditionTripUpdate(UpdateView):
    model = ConditionTrip
    template_name = 'supervision/business_trip/conditiontrip_form.html'
    fields = ['name']
    success_url = reverse_lazy('condition_trip_list')

class ConditionTripDelete(DeleteView):
    model = ConditionTrip
    template_name = 'supervision/business_trip/conditiontrip_confirm_delete.html'
    fields = ['name']
    success_url = reverse_lazy('condition_trip_list')


#--------------- Статусы носоответствия ----------------

def status_mismatch_list(request):
    status_mismatch_list = Status.objects.all()

    return render(
        request,
        'supervision/mismatch/status_mismatch_list.html',
        context={
            'title': 'Статусы несоответствий',
            'status_mismatch_list': status_mismatch_list,
        },
    )


# --------- Редактирование, обновление, удаление  формы чертеж
class StatusMismatchCreate(CreateView):
    model = Status
    template_name = 'supervision/mismatch/statusmismatch_form.html'
    fields = ['name']
    success_url = reverse_lazy('status_mismatch_list')

class StatusMismatchUpdate(UpdateView):
    model = Status
    template_name = 'supervision/mismatch/statusmismatch_form.html'
    fields = ['name']
    success_url = reverse_lazy('status_mismatch_list')

class StatusMismatchDelete(DeleteView):
    model = Status
    template_name = 'supervision/mismatch/statusmismatch_confirm_delete.html'
    fields = ['name']
    success_url = reverse_lazy('status_mismatch_list')