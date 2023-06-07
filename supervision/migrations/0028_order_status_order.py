# Generated by Django 4.1.7 on 2023-06-07 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supervision', '0027_remove_order_status_place_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supervision.placestatus', verbose_name='Статус Заказа'),
        ),
    ]