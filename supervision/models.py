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
    name = models.CharField(max_length=250, verbose_name='Должность')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position_detail', args=[str(self.id)])


class Place(models.Model):
    name = models.CharField(max_length=250, help_text="Название объекта", verbose_name='Название объекта')
    equipment = models.CharField(max_length=250, help_text="Модель оборудования (котла)", null=True, blank=True, verbose_name='Модель оборудования (котла)')
    equipment_type = models.CharField(max_length=250, help_text="Тип оборудования (котла)", null=True, blank=True, verbose_name='Тип оборудования (котла)')
    contract = models.CharField(max_length=250, help_text="номер договора", null=True, blank=True, verbose_name='номер договора')
    project_manager = models.CharField(max_length=100, help_text='руководитель проекта', null=True, blank=True, verbose_name='руководитель проекта')
    chief_engineer = models.CharField(max_length=100, help_text='главный инженер проекта', null=True, blank=True, verbose_name='главный инженер проекта')
    order = models.IntegerField(help_text='Номер Заказа', null=True, blank=True, verbose_name='Номер Заказа')
    # STATUS_OBJ = (
    #     ('Перспективный', 'Перспективный'),
    #     ('Действующий', 'Действующий'),
    #     ('Завершенный', 'Завершенный'),
    #     ('Отмененный', 'Отмененный'),
    # )
    status = models.ForeignKey('PlaceStatus', on_delete=models.SET_NULL,  null=True, blank=True, verbose_name='Статус')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('place_detail', args=[int(self.id)])

class PlaceStatus(models.Model):
    name = models.CharField(max_length=250, verbose_name='статус объекта')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('status_place', kwargs={'status_id': self.id})


class BusinessTrip(models.Model):
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, verbose_name='Оъект')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='сотрудник')
    start = models.DateField(help_text='Дата начала командировки', null=True, blank=True, verbose_name='дата начала')
    end = models.DateField(help_text='Дата окончания командировки', null=True, blank=True, verbose_name='дата окончания')
    purpose = models.CharField(max_length=250, help_text='Цель командировки', verbose_name='Цель')
    activ = models.BooleanField(help_text='Действующая', default=False, verbose_name='статус')

    def __str__(self):
        return f'{self.place} {self.purpose}'

    def get_absolute_url(self):
        return reverse('business_trip_detail', args=[int(self.id)])

    class Meta:
        permissions =(('can_extension', 'Может продливать командировку'),)


class Group(models.Model):
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, verbose_name='Оъект')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    number = models.PositiveIntegerField(help_text='номер узла без родителя')
    suffix = models.CharField(max_length=10, help_text='суфикс номера', null=True, blank=True)
    name = models.CharField(max_length=200, help_text='наименование узла/подузла')


    def check_parent(self):
        if not self.parent:
            return ""


    def __str__(self):
        return f'{self.parent} -> {self.number} {self.name}'

    def get_absolute_url(self):
        return reverse('group_detail', args=[str(self.id)])


class Drawing(models.Model):
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=50, help_text='Обозначение детали')
    name = models.CharField(max_length=250, help_text='Наименование детали')
    mass = models.DecimalField(help_text='Масса', max_digits=11, decimal_places=3, null=True, blank=True)
    steel = models.CharField(max_length=250, help_text='Марка стали', null=True, blank=True)
    file = models.FileField(upload_to='media/detail/', null=True, blank=True)

    def __str__(self):
        return f'{self.number} {self.name}'

    def get_absolute_url(self):
        return reverse('drawing_detail', args=[str(self.id)])

    class Meta:
        unique_together = ('number', 'name')


class Detail(models.Model):
    drawing = models.ForeignKey('Drawing', on_delete=models.SET_NULL, null=True, blank=True)
    mfnumber = models.IntegerField(help_text='Заводской номер', null=True, blank=True)
    quantity = models.IntegerField(help_text='Количество', null=True, blank=True)
    factory = models.CharField(max_length=150, help_text='Изготовитель', null=True, blank=True)

    def __str__(self):
        return f'{self.drawing.number} {self.drawing.name}'

    def get_absolute_url(self):
        return reverse('detail_detail', args=[str(self.id)])


class Mismatch(models.Model):
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=400, help_text=' Краткое описание')
    text = models.TextField(help_text=' Полное описание')
    TYPE = [
        ('p', 'Конструкторское'),
        ('m', 'Производстенное'),
    ]
    type = models.CharField(max_length=2, choices=TYPE, help_text='Тип несоответствия')
    file = models.FileField(upload_to='media/mismatch/', null=True, blank=True)
    image = models.ImageField(upload_to='media/mismatch/images/', null=True, blank=True)
    details = models.ManyToManyField('Detail', through='Irrelevant')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mismatch_detail', args=[str(self.id)])


class Irrelevant(models.Model):
    mismatch = models.ForeignKey('Mismatch', on_delete=models.CASCADE)
    detail = models.ForeignKey('Detail', on_delete=models.CASCADE)
    quantity = models.IntegerField(help_text='Количество', null=True, blank=True)

    class Meta:
        unique_together = ('mismatch', 'detail')


class Letter(models.Model):
    number = models.PositiveIntegerField(unique=True)
    date = models.DateField(default=date.today)
    title = models.CharField(max_length=250)
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    to = models.CharField(max_length=350, null=True, blank=True)
    mismatch = models.ForeignKey('Mismatch', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='media/mismatch/letter/', null=True, blank=True)
    image = models.ImageField(upload_to='media/mismatch/letter/images/', null=True, blank=True)

    def __str__(self):
        return f'{self.number} {self.title}'

    def get_absolute_url(self):
        return reverse('letter_detail', args=[str(self.id)])

class Solution(models.Model):
    number = models.PositiveIntegerField(unique=True)
    date = models.DateField(default=date.today)
    title = models.CharField(max_length=250)
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    to = models.CharField(max_length=350, null=True, blank=True)
    mismatch = models.ForeignKey('Mismatch', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='media/mismatch/solution/', null=True, blank=True)

    def __str__(self):
        return f'{self.number} {self.title}'

    def get_absolute_url(self):
        return reverse('solution_detail', args=[str(self.id)])


class Status(models.Model):
    name = models.CharField(max_length=200, help_text='Статус')

    def __str__(self):
        return self.name


class Tracking(models.Model):
    mismatch = models.ForeignKey('Mismatch', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True)
    date_status = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.mismatch.title} {self.status.name}'

    # class Meta:
    #     unique_together = ('mismatch', 'status')