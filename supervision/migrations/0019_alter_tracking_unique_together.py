# Generated by Django 4.1.7 on 2023-04-07 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0018_alter_tracking_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tracking',
            unique_together=set(),
        ),
    ]