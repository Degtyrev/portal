from django.db import models
from django.urls import reverse


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50, help_text="Отчество", null=True, blank=True)
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    position = models.ForeignKey('Career', on_delete=models.SET_NULL, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

# Дата рождения: {{ user.profile.birth_date }}

class Career(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    POSITION = (
        ('3', '3 категория'),
        ('2', '2 категория'),
        ('1', '1 категория'),
        ('ld', 'Ведущий'),
    )
    position = models.CharField(max_length=5, choices=POSITION, default='ld')
    start_date = models.DateField(help_text="Дата приёма")
    end_date = models.DateField(help_text="Дата увольнения", null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.position}'


class Objects(models.Model):
    name = models.CharField(max_length=250, help_text="Название объекта")
    object_model = models.CharField(max_length=250, help_text="Модель оборудования (котла)", null=True, blank=True)
    object_type = models.CharField(max_length=250, help_text="Тип оборудования (котла)", null=True, blank=True)
    contract = models.CharField(max_length=250, help_text="номер договора", null=True, blank=True)
    project_manager = models.CharField(max_length=100, help_text='руководитель проекта', null=True, blank=True)
    chief_engineer = models.CharField(max_length=100, help_text='главный инженер проекта', null=True, blank=True)

    STATUS_OBJ = (
        ('p', 'Перспективный'),
        ('a', 'Действующий'),
        ('c', 'Завершенный'),
        ('d', 'Отмененный'),
    )
    status = models.CharField(max_length=2, choices=STATUS_OBJ, default='a')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('object-detail', args=[str(self.id)])



class BusinessTrip(models.Model):
    object_name = models.ForeignKey('Objects', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start = models.DateField(help_text='Дата начала командировки', null=True, blank=True)
    end = models.DateField(help_text='Дата окончания командировки', null=True, blank=True)
    purpose = models.CharField(max_length=250, help_text='Цель командировки')

    def __str__(self):
        return f'{self.object_name} {self.purpose}'

    def get_absolute_url(self):
        return reverse('business_trip-detail', args=[str(self.id)])


class Unit(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    number = models.CharField(max_length=20, help_text='номер узла/подузла')
    name = models.CharField(max_length=200, help_text='наименование узла/подузла')

    def __str__(self):
        return f'{self.number} {self.name}'

    def get_absolute_url(self):
        return reverse('unit-detail', args=[str(self.id)])

class Element(models.Model):
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=50, help_text='Обозначение детали')
    name = models.CharField(max_length=250, help_text='Наименование детали')
    fac_number = models.IntegerField(help_text='Заводской номер', null=True, blank=True)
    order = models.IntegerField(help_text='Номер Заказа', null=True, blank=True)
    mass = models.DecimalField(help_text='Масса', max_digits=11, decimal_places=3, null=True, blank=True)
    steel = models.CharField(max_length=250, help_text='Марка стали', null=True, blank=True)

    def __str__(self):
        return f'{self.number} {self.name}'

    def get_absolute_url(self):
        return reverse('element-detail', args=[str(self.id)])

    class Meta:
        unique_together = ('number', 'name')

class Mismatch(models.Model):
    object = models.ForeignKey('Objects', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True)
    status = models.ManyToManyField('Status', through='Tracking')
    element = models.ForeignKey('Element', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=400, help_text=' Краткое описание')
    text = models.TextField(help_text=' Полное описание')
    TYPE = (
        ('p', 'Конструкторское'),
        ('m', 'Производстенное'),
    )
    type = models.CharField(max_length=2, choices=TYPE)
    letter = models.CharField(max_length=150, help_text='Номер служебного письма', null=True, blank=True)
    answer = models.CharField(max_length=150, help_text='Ответ служебное письмо', null=True, blank=True)
    solution = models.CharField(max_length=150, help_text='Принятое решени', null=True, blank=True)
    corrected = models.CharField(max_length=150, help_text='Кем устранено', null=True, blank=True)
    date_finding = models.DateField(help_text='Дата', null=True, blank=True)
    factory = models.CharField(max_length=150, help_text='Изготовитель', null=True, blank=True)
    pack = models.CharField(max_length=150, help_text='Грузовое место', null=True, blank=True)
    amount = models.IntegerField(help_text='Количество', null=True, blank=True)
    file = models.FileField(upload_to='media/mismatch/', null=True, blank=True)
    image = models.ImageField(upload_to='media/mismatch/images/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mismatch-detail', args=[str(self.id)])


class Status(models.Model):
    status = models.CharField(max_length=200, help_text='Статус')

    def __str__(self):
        return self.status


class Tracking(models.Model):
    mismatch = models.ForeignKey('Mismatch', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True)
    date_status = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='media/mismatch/status/', null=True, blank=True)

    def __str__(self):
        return f'{self.mismatch} {self.status}'

    # class Meta:
    #     unique_together = ('mismatch', 'status')