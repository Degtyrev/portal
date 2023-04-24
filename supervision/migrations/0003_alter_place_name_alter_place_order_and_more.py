# Generated by Django 4.1.7 on 2023-04-23 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0002_rename_unit_drawing_group_remove_drawing_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(help_text='Название объекта', max_length=250, verbose_name='Название объекта'),
        ),
        migrations.AlterField(
            model_name='place',
            name='order',
            field=models.IntegerField(blank=True, help_text='Номер Заказа', null=True, verbose_name='Номер Заказа'),
        ),
        migrations.AlterField(
            model_name='place',
            name='status',
            field=models.CharField(choices=[('Перспективный', 'Перспективный'), ('Действующий', 'Действующий'), ('Завершенный', 'Завершенный'), ('Отмененный', 'Отмененный')], default='Перспективный', max_length=20, verbose_name='Статус'),
        ),
    ]
