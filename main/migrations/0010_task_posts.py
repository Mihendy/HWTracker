# Generated by Django 4.2.8 on 2024-06-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_slug_alter_post_title'),
        ('main', '0009_alter_task_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='posts.post'),
        ),
    ]
