# Generated by Django 4.0.5 on 2022-07-07 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MouleOne', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
