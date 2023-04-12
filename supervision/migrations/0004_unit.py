# Generated by Django 4.1.7 on 2023-04-02 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0003_businesstrip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(help_text='номер узла/подузла', max_length=20)),
                ('name', models.CharField(help_text='наименование узла/подузла', max_length=20)),
                ('parent', models.ForeignKey(default='0', null=True, on_delete=django.db.models.deletion.CASCADE, to='supervision.unit')),
            ],
        ),
    ]