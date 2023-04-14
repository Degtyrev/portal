# Generated by Django 4.1.7 on 2023-04-12 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0021_rename_status_businesstrip_activ'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plaсe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название объекта', max_length=250)),
                ('equipment', models.CharField(blank=True, help_text='Модель оборудования (котла)', max_length=250, null=True)),
                ('equipment_type', models.CharField(blank=True, help_text='Тип оборудования (котла)', max_length=250, null=True)),
                ('contract', models.CharField(blank=True, help_text='номер договора', max_length=250, null=True)),
                ('project_manager', models.CharField(blank=True, help_text='руководитель проекта', max_length=100, null=True)),
                ('chief_engineer', models.CharField(blank=True, help_text='главный инженер проекта', max_length=100, null=True)),
                ('status', models.CharField(choices=[('p', 'Перспективный'), ('a', 'Действующий'), ('c', 'Завершенный'), ('d', 'Отмененный')], default='a', max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='businesstrip',
            name='object_name',
        ),
        migrations.RemoveField(
            model_name='mismatch',
            name='object',
        ),
        migrations.DeleteModel(
            name='Objects',
        ),
        migrations.AddField(
            model_name='businesstrip',
            name='plaсe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supervision.plaсe'),
        ),
        migrations.AddField(
            model_name='mismatch',
            name='plaсe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supervision.plaсe'),
        ),
    ]
