# Generated by Django 3.0.2 on 2020-04-06 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task_creator', '0003_auto_20200406_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsuite',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]