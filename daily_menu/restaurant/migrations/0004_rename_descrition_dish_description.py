# Generated by Django 4.2 on 2024-08-10 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_dailymenu_name_alter_dish_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='descrition',
            new_name='description',
        ),
    ]
