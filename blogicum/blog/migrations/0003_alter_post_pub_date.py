# Generated by Django 3.2.16 on 2023-09-14 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20230911_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, help_text='Если установить дату и время в будущем — можно делать отложенные публикации.', verbose_name='Дата и время публикации'),
        ),
    ]
