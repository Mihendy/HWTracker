# Generated by Django 4.2.7 on 2023-12-08 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_task_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name']},
        ),
    ]
