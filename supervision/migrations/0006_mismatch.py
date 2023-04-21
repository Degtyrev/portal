# Generated by Django 4.1.7 on 2023-04-02 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supervision', '0005_element'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mismatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=' Краткое описание', max_length=400)),
                ('text', models.TextField(help_text=' Полное описание')),
                ('type', models.CharField(choices=[('p', 'Конструкторское'), ('m', 'Производстенное')], max_length=2)),
                ('letter', models.CharField(help_text='Номер служебного письма', max_length=150)),
                ('answer', models.CharField(help_text='Ответ служебное письмо', max_length=150)),
                ('solution', models.CharField(help_text='Принятое решени', max_length=150)),
                ('date_finding', models.DateField(help_text='Дата')),
                ('drawing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supervision.drawing')),
                ('object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supervision.objects')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
