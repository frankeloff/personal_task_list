# Generated by Django 4.1.5 on 2023-03-01 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='task',
            name='date_of_completion',
            field=models.DateTimeField(verbose_name='Дата выполнения'),
        ),
    ]
