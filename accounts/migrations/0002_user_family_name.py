# Generated by Django 3.2.5 on 2021-08-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='family_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
