# Generated by Django 4.1.7 on 2023-05-26 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0018_alter_mismatch_file_alter_mismatch_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='career',
            old_name='user',
            new_name='profile',
        ),
        migrations.AlterUniqueTogether(
            name='career',
            unique_together={('profile', 'position')},
        ),
    ]
