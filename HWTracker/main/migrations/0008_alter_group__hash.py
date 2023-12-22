# Generated by Django 4.2.8 on 2023-12-22 13:50

from django.db import migrations, models
import main.functions


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_group__hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='_hash',
            field=models.CharField(default=main.functions.get_random_string32, max_length=256),
        ),
    ]
