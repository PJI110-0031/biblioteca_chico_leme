# Generated by Django 3.2.8 on 2021-11-01 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20211026_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='subjects',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
