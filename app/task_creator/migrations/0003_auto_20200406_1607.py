# Generated by Django 3.0.2 on 2020-04-06 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_creator', '0002_auto_20200406_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsuite',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='task_creator.ProjectList'),
        ),
    ]
