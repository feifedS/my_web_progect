# Generated by Django 4.1.5 on 2023-02-23 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Customer'), (2, 'Master')], default=1),
        ),
    ]
