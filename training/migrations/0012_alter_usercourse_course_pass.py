# Generated by Django 3.2.5 on 2021-08-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0011_auto_20210819_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='course_pass',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
