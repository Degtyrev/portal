from django.db import models
from django.urls import reverse
import datetime
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50, help_text="Отчество", null=True, blank=True)
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    death_date = models.DateField(verbose_name='Дата смерти', null=True, blank=True)
    position = models.ManyToManyField('Position', through='Career')
    is_liner = models.BooleanField(default=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('employee_detail', args=[str(self.user.id)])

# Дата рождения: {{ user.profile.birth_date }}

class Career(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True,)
    start_date = models.DateField(help_text="Дата приёма")
    end_date = models.DateField(help_text="Дата увольнения", null=True, blank=True)

    def __str__(self):
        return f'{self.user.user.first_name} {self.user.user.last_name} {self.position}'
    class Meta:
        unique_together = ('user', 'position')


class Position(models.Model):
    name = models.CharField(max_length=250, verbose_name='Должность', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position_detail', args=[str(self.id)])


class Place(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название объекта')
    equipment = models.CharField(max_length=250, null=True, blank=True, verbose_name='Модель оборудования (котла)')
    equipment_type = models.CharField(max_length=250, null=True, blank=True, verbose_name='Тип оборудования (котла)')
    contract = models.CharField(max_length=250, null=True, blank=True, verbose_name='номер договора')
    project_manager = models.CharField(max_length=100, null=True, blank=True, verbose_name='руководитель проекта')
    chief_engineer = models.CharField(max_length=100, null=True, blank=True, verbose_name='главный инженер проекта')
    order = models.IntegerField(null=True, blank=True, verbose_name='Номер Заказа', unique=True)
    status = models.ForeignKey('PlaceStatus', on_delete=models.SET_NULL,  null=True, blank=True, verbose_name='Статус объекта')

    def __str__(self):
        return f'{self.name} з/з({self.order})'

    def get_absolute_url(self):
        return reverse('place_detail', args=[int(self.id)])

class PlaceStatus(models.Model):
    name = models.CharField(max_length=250, verbose_name='статус объекта', null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('place_status_detail', args=[int(self.pk)])


class BusinessTrip(models.Model):
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, verbose_name='Оъект')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Cотрудник')
    start = models.DateField(null=True, blank=True, verbose_name='дата начала')
    end = models.DateField(null=True, blank=True, verbose_name='дата окончания')
    purpose = models.CharField(max_length=250, verbose_name='Цель командировки')
    status = models.ForeignKey('ConditionTrip', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='статус')

    def __str__(self):
        return f'{self.place} {self.purpose}'

    def get_absolute_url(self):
        return reverse('business_trip_detail', args=[int(self.id)])

    class Meta:
        permissions =(('can_extension', 'Может продливать командировку'),)

class ConditionTrip(models.Model):
    name = models.CharField(max_length=50, verbose_name='Состояние командировки', null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('condition_trip_detail', args=[int(self.pk)])



class Group(models.Model):
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, verbose_name='Оъект')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родительская Группа')
    number = models.PositiveIntegerField(verbose_name='номер Группы, без номера родителя')
    suffix = models.CharField(max_length=10, verbose_name='суфикс Группы', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='наименование Группы')


    def __str__(self):
        return  f'{self.number}. {self.name}'
        # return f'{self.parent} -> {self.number} {self.name}'

    def get_absolute_url(self):
        return reverse('group_detail', args=[str(self.id)])


class Drawing(models.Model):
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=50, verbose_name='Обозначение детали')
    name = models.CharField(max_length=250, verbose_name='Наименование детали')
    mass = models.DecimalField(verbose_name='Масса', max_digits=11, decimal_places=3, null=True, blank=True)
    steel = models.CharField(max_length=250, verbose_name='Марка стали', null=True, blank=True)
    file = models.FileField(upload_to='media/detail/', null=True, blank=True, verbose_name='Файлы')

    def __str__(self):
        return f'{self.number} {self.name}'

    def get_absolute_url(self):
        return reverse('drawing_detail', args=[str(self.id)])

    class Meta:
        unique_together = ('number', 'name')


# class Detail(models.Model):
#     drawing = models.ForeignKey('Drawing', on_delete=models.SET_NULL, null=True, blank=True)
#     mfnumber = models.IntegerField(verbose_name='Заводской номер', null=True, blank=True)
#     quantity = models.IntegerField(verbose_name='Количество', null=True, blank=True)
#     factory = models.CharField(max_length=150, verbose_name='Изготовитель', null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.drawing.number} {self.drawing.name}'
#
#     def get_absolute_url(self):
#         return reverse('detail_detail', args=[str(self.id)])


class Mismatch(models.Model):
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=400, verbose_name=' Краткое описание')
    text = models.TextField(verbose_name=' Полное описание')
    correct = models.TextField(verbose_name='Предложения по устранению', null=True, blank=True)
    type = models.ForeignKey('TypeMismatch', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='media/mismatch/', null=True, blank=True, verbose_name='Файлы')
    image = models.ImageField(upload_to='media/mismatch/images/', null=True, blank=True, verbose_name='Фото')
    details = models.ManyToManyField('Drawing', through='Irrelevant')
    status = models.ManyToManyField('Status', through='Tracking')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mismatch_detail', args=[int(self.pk)])

class Status(models.Model):
    name = models.CharField(max_length=200, verbose_name='Статус', unique=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('solution_detail', args=[str(self.id)])

class Tracking(models.Model):
    mismatch = models.ForeignKey('Mismatch', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True)
    date_status = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.mismatch.title} {self.status.name}'

    # class Meta:
    #     unique_together = ('mismatch', 'status')


class TypeMismatch(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип несоответствия', null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return receiver('type_mismatch', args=[int(self.pk)])

class Irrelevant(models.Model):
    mismatch = models.ForeignKey('Mismatch', on_delete=models.CASCADE, null=True, blank=True)
    detail = models.ForeignKey('Drawing', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Количество', null=True, blank=True)

    class Meta:
        unique_together = ('mismatch', 'detail')


class Letter(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name='Номер письма')
    date = models.DateField(default=date.today, verbose_name='Дата')
    title = models.CharField(max_length=250, verbose_name='Тема')
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='От кого')
    to = models.CharField(max_length=350, null=True, blank=True, verbose_name='Кому')
    mismatch = models.ForeignKey('Mismatch', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Несоответствие')
    file = models.FileField(upload_to='media/mismatch/letter/', null=True, blank=True, verbose_name='Файлы')
    image = models.ImageField(upload_to='media/mismatch/letter/images/', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return f'{self.number} {self.title}'

    def get_absolute_url(self):
        return reverse('letter_detail', args=[str(self.id)])

class Solution(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name='Номер Тех.решения')
    date = models.DateField(default=date.today, verbose_name='Дата')
    title = models.CharField(max_length=250, verbose_name='Тема')
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='От кого')
    to = models.CharField(max_length=350, null=True, blank=True, verbose_name='Кому')
    mismatch = models.ForeignKey('Mismatch', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Несоответствие')
    file = models.FileField(upload_to='media/mismatch/solution/', null=True, blank=True, verbose_name='Файлы')

    def __str__(self):
        return f'{self.number} {self.title}'

    def get_absolute_url(self):
        return reverse('solution_detail', args=[str(self.id)])


