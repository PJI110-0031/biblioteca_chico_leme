# Generated by Django 3.2.8 on 2021-10-22 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20211021_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='page_count',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Page count'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='books.publisher', verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='book',
            name='shelf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='books.shelf', verbose_name='Shelf'),
        ),
        migrations.AlterField(
            model_name='book',
            name='volume',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Volume'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='ddc',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='DDC'),
        ),
    ]
