# Generated by Django 3.2.5 on 2021-09-24 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produse', '0009_rename_comanda_comenzi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comenzi',
            name='data_livrare',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comenzi',
            name='data_plata',
            field=models.DateField(blank=True, null=True),
        ),
    ]
