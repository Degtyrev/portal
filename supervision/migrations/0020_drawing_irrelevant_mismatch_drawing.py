# Generated by Django 4.1.7 on 2023-05-29 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0019_rename_user_career_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, verbose_name='Обозначение детали')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование детали')),
                ('mass', models.DecimalField(blank=True, decimal_places=3, max_digits=11, null=True, verbose_name='Масса')),
                ('steel', models.CharField(blank=True, max_length=250, null=True, verbose_name='Марка стали')),
                ('file', models.FileField(blank=True, null=True, upload_to='media/detail/', verbose_name='Файлы')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supervision.group')),
            ],
            options={
                'unique_together': {('number', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Irrelevant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Количество')),
                ('drawing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supervision.drawing')),
                ('mismatch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supervision.mismatch')),
            ],
            options={
                'unique_together': {('mismatch', 'drawing')},
            },
        ),
        migrations.AddField(
            model_name='mismatch',
            name='drawing',
            field=models.ManyToManyField(through='supervision.Irrelevant', to='supervision.drawing', verbose_name='Детали'),
        ),
    ]
