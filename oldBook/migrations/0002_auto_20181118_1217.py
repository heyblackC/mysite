# Generated by Django 2.1.1 on 2018-11-18 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oldBook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, verbose_name='其他描述'),
        ),
    ]
