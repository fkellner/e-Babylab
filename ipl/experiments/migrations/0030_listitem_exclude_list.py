# Generated by Django 2.0.8 on 2018-09-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0029_auto_20180916_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='exclude_list',
            field=models.BooleanField(default=False, help_text='Exclude list during experiment'),
        ),
    ]