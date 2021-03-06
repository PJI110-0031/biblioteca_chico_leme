# Generated by Django 3.2.8 on 2021-11-03 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20211101_1657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shelf',
            options={'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects'},
        ),
        migrations.AlterField(
            model_name='book',
            name='shelf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='books.shelf', verbose_name='Subject'),
        ),
    ]
