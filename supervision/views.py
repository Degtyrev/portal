import os.path

from django.contrib.auth.views import LoginView
from django.db.models import Max
from django.shortcuts import render, redirect
from .models import *
import datetime
from django.core.paginator import Paginator
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




#установка статуса командировки
def change_status_trip(request):
    business_trip = BusinessTrip.objects.all()

    for trip in business_trip:
        if trip.end < datetime.date.today():
            BusinessTrip.objects.filter(pk=trip.pk).update(status_id=3) #завершена

        if trip.start == datetime.date.today():
            BusinessTrip.objects.filter(pk=trip.pk).update(status_id=2) #действующая

        if trip.start < datetime.date.today() and trip.end >= datetime.date.today():
            BusinessTrip.objects.filter(pk=trip.pk).update(status_id=2) #действующая

        if trip.start > datetime.date.today():
            BusinessTrip.objects.filter(pk=trip.pk).update(status_id=1)  # перспективная

    request.session['change_status'] = 1

#установка статуса несоответствия

def change_status_mismatch(request):
    mismatchs = Mismatch.objects.all()
    for mismatch in mismatchs:

        if Letter.objects.filter(mismatch=mismatch.pk) and mismatch.status_id != 4:
            Mismatch.objects.filter(pk=mismatch.pk).update(status_id=2)# запрос в отдел

        if Letter.objects.filter(mismatch=mismatch.pk) and Solution.objects.filter(mismatch=mismatch.pk) and mismatch.status_id != 4:
            Mismatch.objects.filter(pk=mismatch.pk).update(status_id=3)# Выдано Тех.решение

        if not Letter.objects.filter(mismatch=mismatch.pk) and not Solution.objects.filter(mismatch=mismatch.pk) and mismatch.status_id != 4:
            Mismatch.objects.filter(pk=mismatch.pk).update(status_id=1)# новое



#----------- Главная Main -----------
def index(request):
    num_mismatches_place = 0
    num_mismatches_order = 0

# проверка и изменение статуса командировок  если первый вход
    session_check = request.session.get('change_status', 0)
    if session_check == 0:
        change_status_trip(request)


# проверка и изменение статуса несоответствия
    change_status_mismatch(request)

    num_employeer = User.objects.filter(is_active=1).count()
    num_place = Place.objects.filter(status=2).count()  # Метод 'all()' применён по умолчанию.
    date_today = datetime.date.today()
    activ_trip = BusinessTrip.objects.filter(user_id__exact=request.user.pk, status_id__exact=2)
    # print(activ_trip)

    if activ_trip:
        request.session['activ_trip'] = activ_trip[0].pk
        request.session['activ_place'] = activ_trip[0].place_id
        activ_trip = activ_trip[0]
        balanse = activ_trip.end - date_today
        balanse = balanse.days
        mismatches_place = Mismatch.objects.filter(place_id__exact=activ_trip.place_id).filter(
            status__pk__in=[1, 2, 3]).order_by('status_id')
        num_mismatches_place = Mismatch.objects.filter(place_id__exact=activ_trip.place_id).filter(
            status__pk__in=[1, 2, 3]).count()
    else:
        activ_trip = False
        balanse = False
        mismatches_place = False



    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    # request.GET - список параметров передаваемых GET запросом /?name=gggg&age=233
    # request.POST - список параметров передаваемых POST запросом

    if request.session.get('activ_trip'):
        activ_tp = request.session.get('activ_trip')
    else:
        activ_tp=False

    if request.session.get('activ_place'):
        activ_plc = request.session.get('activ_place')
    else:
        activ_plc=False

    mismatches = Mismatch.objects.filter(status__pk__in=[2]).order_by('status_id')
    num_mismatches = Mismatch.objects.filter(status__pk__in=[2]).count()


    context = {
        'title': "Портал",
        'num_employeer': num_employeer,
        'num_place': num_place,
        'activ_trip': activ_trip,
        'pk': activ_plc,
        'mismatches': mismatches,
        "num_mismatches": num_mismatches,
        "num_mismatches_place": num_mismatches_place,
        'balanse': balanse,
        'mismatches_place': mismatches_place,
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
    change_status_trip(request)  # обновление статуса командировки
    date_today = datetime.date.today()
    trips_user = BusinessTrip.objects.filter(status_id__exact=2).filter(user_id__exact=request.user.pk)
    trips = BusinessTrip.objects.filter(status__exact=2)
    conditions = ConditionTrip.objects.all()
    # получени остатков командировки

    if trips_user:
        balanse = trips_user[0].end - date_today
        balanse = balanse.days
    else:
        balanse = False

    # print(trips_user[0].end)
    # print(date_today)
    #
    # print(balanse)

    return render(
        request,
        'supervision/business_trip/business_trip.html',
        context={
            'title': 'Список Командировок',
            'trips_user': trips_user,
            'trips': trips,
            'balanse': balanse,
            'conditions': conditions,
            'condition_selected': 2,
        },
    )


def condition_show(request, pk):
    trips_user = BusinessTrip.objects.filter(status__exact=pk).filter(user_id__exact=request.user.pk)
    trips = BusinessTrip.objects.filter(status__exact=pk)
    conditions = ConditionTrip.objects.all()

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
    trip = BusinessTrip.objects.get(pk=pk)

    context = {
                'title': 'Командировка',
                'trip': trip,
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
            # print(datetime.date.today())
            # print(start)
            # print(end)
            # print(user)

            carent_trip = BusinessTrip.objects.filter(user__exact=user).filter(status__exact=2)

            try:
                if carent_trip:
                    date_end_carent_trip = carent_trip[0].end

                    if start < date_end_carent_trip: # если дата следующей командировки раньще конца текущей
                        raise Exception(form.add_error(None, f'Сотрудник находится в командировке до {date_end_carent_trip}'))

                if start > end:# если дата начала позже даты завершения
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
    success_url = reverse_lazy('business_trip')


class BusinessTripDelete(DeleteView):
    model = BusinessTrip
    template_name = 'supervision/business_trip/businesstrip_confirm_delete.html'
    success_url = reverse_lazy('business_trip')


#----------- Список Несоответствий  -----------

def mismatch_list(request):
    global mismatches_place
    global paginator_l
    change_status_mismatch(request)

    mismatches = Mismatch.objects.filter(status__pk__in=[2]).order_by('status_id')

    place = Place.objects.filter(status__exact=2)
    user = request.user

    carent_trip = BusinessTrip.objects.filter(user__exact=user.pk).filter(status__exact=2)

    if carent_trip: # выбираем несоответствия для даного объекта
        mismatches_place = Mismatch.objects.filter(place_id__exact=carent_trip[0].place_id).filter(status__pk__in=[1, 2, 3]).order_by('status_id')
    else:
        mismatches_place = False

    # paginator_m = Paginator(mismatches, 3)
    # page_number = request.GET.get('page', 1)
    #
    # if mismatches_place:
    #     paginator_l = Paginator(mismatches_place, 3)
    #     mismatches_place = paginator_l.page(page_number)
    #
    # mismatches = paginator_m.page(page_number)


    return render(
        request,
        'supervision/mismatch/mismatch.html',
        context={
            'title': 'Список несоответствий',
            'mismatches': mismatches,
            'place': place,
            'mismatches_place': mismatches_place,
            'select': 1,
        },
    )


#----------- карточка Наосоответствия  -----------

def mismatch_detail(request, pk):
    mismatch = Mismatch.objects.get(pk=pk)
    statuses = Status.objects.all().order_by('id')
    letters = Letter.objects.filter(mismatch=mismatch.pk)
    solutions = Solution.objects.filter(mismatch=mismatch.pk)
    activ_status = mismatch.status.pk

    return render(
            request,
        'supervision/mismatch/mismatch_detail.html',
            context={
                'title': 'Карточка Неоответствия',
                'mismatch': mismatch,
                'statuses': statuses,
                'letters': letters,
                'solutions': solutions,
                'activ_status': activ_status,
            },
        )

# --------- Редактирование, обновление, удаление  формы  несоответствия

# class MismatchCreate(CreateView):
#     model = Mismatch
#     fields = '__all__'

def mismatch_create(request):
    if request.method == 'POST':
        form = CreateMismatchForm(request.POST, request.FILES)
        my_files = request.FILES.getlist("file")
        my_images = request.FILES.getlist("image")
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Mismatch.objects.create(**form.cleaned_data)
                return redirect('mismatch_list')
            except:
                form.add_error(None, "ошибка добавления несоответстия")
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        form = CreateMismatchForm(initial={'place': request.session['activ_place'], 'status': 1})

    return render(request, 'supervision/mismatch/mismatch_create.html',
                      {'form': form, 'title': 'Несоответстиве'})

class MismatchUpdate(UpdateView):
    model = Mismatch
    fields = '__all__'
    template_name = 'supervision/mismatch/mismatch_create.html'

class MismatchDelete(DeleteView):
    model = Mismatch
    success_url = reverse_lazy('mismatch')


def mismatch_close(request, pk):
    Mismatch.objects.filter(pk=pk).update(status_id=4)  # Закрыто

    return HttpResponseRedirect(reverse('mismatch_list'))



def mismatch_filter(request):
    mismatches=0
    mismatches_place=0
    # paginator_l = None

    place = Place.objects.filter(status__exact=2)
    user = request.user
    carent_trip = BusinessTrip.objects.filter(user__exact=user.pk).filter(status__exact=2)

    select = int(request.GET['select'])
    print(select)

    if select == 2:
        mismatches = Mismatch.objects.all().order_by('status_id')
    elif select == 1:
        mismatches = Mismatch.objects.filter(status__pk__in=[2]).order_by('status_id')
    print(mismatches)

    if carent_trip:  # выбираем несоответствия для даного объекта
        if select == 1:
            mismatches_place = Mismatch.objects.filter(place_id__exact=carent_trip[0].place_id).filter(status__pk__in=[1, 2, 3]).order_by('status_id')
        elif select == 2:
            mismatches_place = Mismatch.objects.filter(place_id__exact=carent_trip[0].place_id).order_by('status_id')
    else:
        mismatches_place = False
    print(mismatches_place)

    return render(
        request,
        'supervision/mismatch/mismatch.html',
        context={
            'title': 'Список несоответствий',
            'mismatches': mismatches,
            'place': place,
            'mismatches_place': mismatches_place,
            'select': select,
        },
    )

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
def group_list(request):
    pk = request.session.get('activ_place')
    group_list = Group.objects.filter(place_id__exact=pk).order_by('number')
    place_pk = pk
    return render(
        request,
        'supervision/group/group_list.html',
        context={
            'title': 'Список Групп',
            'group_list': group_list,
            "place_pk": place_pk,

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
        },
    )

# --------- Редактирование, обновление, удаление  формы Узла

# class GroupCreate(CreateView):
#     model = Group
#     fields = '__all__'

def group_create(request):
    activ_place_pk = request.session.get('activ_place')

    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('group_list')
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        form = CreateGroupForm(initial={'place': activ_place_pk})
    return render(request, 'supervision/group/groupcreate_form.html',
                  {'form': form, 'title': 'Группы чертежей'})


class GroupUpdate(UpdateView):
    model = Group
    fields = '__all__'
    template_name = 'supervision/group/groupcreate_form.html'
    success_url = reverse_lazy('group_list')

class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')



#--------------- Чертежи----------------

def drawing_list(request):
    activ_place_pk = request.session.get('activ_place')

    if activ_place_pk:
        drawing_list = Drawing.objects.filter(group__place_id=activ_place_pk)
    else:
        drawing_list=False

    return render(
        request,
        'supervision/drawing/drawing_list.html',
        context={
            'title': 'Список Чертежей',
            'drawing_list': drawing_list,
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
        },
    )

# --------- Редактирование, обновление, удаление  формы чертеж

def drawing_create(request):
    activ_place_pk = request.session.get('activ_place')

    if request.method == 'POST':
        form = CreateDrawingForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('drawing_list')
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        form = CreateDrawingForm()
    return render(request, 'supervision/drawing/drawingcreate_form.html',
                  {'form': form, 'title': 'Перечень чертежей'})

class DrawingUpdate(UpdateView):
    model = Drawing
    fields = '__all__'
    template_name = 'supervision/drawing/drawingcreate_form.html'
    success_url = reverse_lazy('drawing_list')

class DrawingDelete(DeleteView):
    model = Drawing
    success_url = reverse_lazy('drawing_list')


# #--------------- Детали----------------
#
# def detail_list(request):
#     detail_list = Detail.objects.all()
#
#     return render(
#         request,
#         'supervision/detail/detail_list.html',
#         context={
#             'title': 'Список Деталей',
#             'detail_list': detail_list,
#         },
#     )
#
# def detail_detail(request, pk):
#     detail_detail = Detail.objects.get(pk=pk)
#
#     return render(
#         request,
#         'supervision/detail/detail_detail.html',
#         context={
#             'title': 'Деталь',
#             'detail_detail': detail_detail,
#             'menu': menu
#         },
#     )
#
# # --------- Редактирование, обновление, удаление  формы чертеж
#
# class DetailCreate(CreateView):
#     model = Detail
#     fields = '__all__'
#
# class DetailUpdate(UpdateView):
#     model = Detail
#     fields = '__all__'
#
# class DetailDelete(DeleteView):
#     model = Detail
#     success_url = reverse_lazy('detail_list')


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
    # employee_detail = Profile.objects.get(id=pk)
    # profile_detail = Profile.objects.get(id=pk)
    career_list = Career.objects.filter(profile__user_id=pk).order_by('-start_date')
    # current_position = Profile.objects.filter(position__career__user_id__exact=pk, position__career__end_date__exact=None)
    # current_position = Career.objects.filter(user_id=pk).last()
    employee_business_trips = BusinessTrip.objects.filter(user_id__exact=pk).order_by('-start')


    context = {
        'title': 'Сотрудник',
        'employee_detail': employee_detail,
        'career_list': career_list,
        # 'current_position': current_position,
        'employee_business_trips': employee_business_trips
    }
    # print(current_position.last())
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

# class EmployeeUpdate(UpdateView):
#     model = Profile
#     fields = '__all__'
#     template_name = 'supervision/employee/employeeupdate_form.html'
#     # template_name = 'supervision/employee/profile_form.html'
#     success_url = reverse_lazy('employee_list')


def employee_update(request, pk):
    user = User.objects.get(pk=pk)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('employee_list')

    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile)
    return render(request, 'supervision/employee/employeeupdate_form.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'title': 'Редактирование профиля'})



#--------------- Служебные письма----------------

def letter_list(request):
    letter_list = Letter.objects.all()

    if request.session.get('activ_place'):
        letter_list_place = Letter.objects.filter(mismatch__place_id__exact=request.session['activ_place'])
    else:
        letter_list_place = False


    return render(
        request,
        'supervision/letter/letter_list.html',
        context={
            'title': 'Список Служебных писем',
            'letter_list': letter_list,
            'letter_list_place': letter_list_place,
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
                change_status_mismatch(request)
                return redirect('letter_list')
            except:
                form.add_error(None, "Ошибка добавления Служебного письма")
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        mismatch_id = request.GET['mismatch_id']
        form = CreateLetterForm(initial={'user': request.user, 'mismatch': mismatch_id})

    return render(request, 'supervision/letter/lettercreate_form.html',
                  {'form': form, 'title': 'Служебное письмо в ОШМ'})


class LetterUpdate(UpdateView):
    model = Letter
    fields = ['number', 'date', 'title', 'text', 'user',
                  'to', 'mismatch', 'file', 'image']
    template_name = 'supervision/letter/lettercreate_form.html'
    success_url = reverse_lazy('letter_list')
    complex = {
        'title': 'Служебное письмо в ОШМ'
    }

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
    solution = Solution.objects.get(pk=pk)

    return render(
        request,
        'supervision/solution/solution_detail.html',
        context={
            'title': 'Техническое решение',
            'solution': solution,
        },
    )

# --------- Редактирование, обновление, удаление  формы чертеж

def solution_create(request):
    if request.method == 'POST':
        form = CreateSolutionForm(request.POST, request.FILES)

        if form.is_valid():
            # print(form.cleaned_data)
            try:
                form.save()
                change_status_mismatch(request)
                return redirect('solution_list')
            except:
                form.add_error(None, "Ошибка добавления Технического решения")
        # return HttpResponseRedirect(reverse('mismatch'))
    else:
        mismatch_id = request.GET['mismatch_id']
        form = CreateSolutionForm(initial={'user': request.user, 'mismatch': mismatch_id})

    return render(request, 'supervision/solution/solutioncreate_form.html',
                  {'form': form, 'title': 'Техническое решение'})

class SolutionUpdate(UpdateView):
    model = Solution
    fields = '__all__'
    template_name = 'supervision/solution/solutioncreate_form.html'
    success_url = reverse_lazy('solution_list')
    complex = {
        'title': 'Редактирование технического решения'
    }

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

def type_mismatch_detail(request, pk):
    type_mismatch_detail = PlaceStatus.objects.get(pk=pk)

    return render(
        request,
        'supervision/mismatch/type_mismatch_detail.html',
        context={
            'title': 'Тип несоответствия',
            'type_mismatch_detail': type_mismatch_detail,

        },
    )

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


#--------------- Наименования----------------

def description_list(request):
    description_list = Description.objects.all()

    return render(
        request,
        'supervision/description/description_list.html',
        context={
            'title': 'Список Наименований',
            'description_list': description_list,
        },
    )

def description_detail(request, pk):
    description_detail = Description.objects.get(pk=pk)

    return render(
        request,
        'supervision/description/description_detail.html',
        context={
            'title': 'Наименование',
            'description_detail': description_detail,
        },
    )

# --------- Редактирование, обновление, удаление  формы наименования

class DescriptionCreate(CreateView):
    model = Description
    template_name = 'supervision/description/description_form.html'
    fields = ['description']
    success_url = reverse_lazy('description_list')

class DescriptionUpdate(UpdateView):
    model = Description
    template_name = 'supervision/description/description_form.html'
    fields = ['description']
    success_url = reverse_lazy('description_list')

# class DescriptionDelete(DeleteView):
#     model = Description
#     success_url = reverse_lazy('description_list')


#--------------- Материал----------------

def material_list(request):
    material_list = Material.objects.all()

    return render(
        request,
        'supervision/material/material_list.html',
        context={
            'title': 'Список Материалов',
            'material_list': material_list,
        },
    )

def material_detail(request, pk):
    material_detail = Material.objects.get(pk=pk)

    return render(
        request,
        'supervision/material/material_detail.html',
        context={
            'title': 'Материал',
            'material_detail': material_detail,
        },
    )

# --------- Редактирование, обновление, удаление  формы материала

class MaterialCreate(CreateView):
    model = Material
    template_name = 'supervision/material/material_form.html'
    fields = ['material', 'gost']
    success_url = reverse_lazy('material_list')

class MaterialUpdate(UpdateView):
    model = Material
    template_name = 'supervision/material/material_form.html'
    fields = ['material', 'gost']
    success_url = reverse_lazy('material_list')

# class MaterialDelete(DeleteView):
#     model = Material
#     success_url = reverse_lazy('material_list')