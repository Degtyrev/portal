# Generated by Django 4.1.7 on 2023-05-22 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0015_alter_mismatch_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='supervision/media/users/photo', verbose_name='Фото'),
        ),
    ]