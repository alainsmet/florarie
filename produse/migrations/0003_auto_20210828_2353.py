# Generated by Django 3.2.5 on 2021-08-28 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produse', '0002_auto_20210828_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produse',
            name='promotie_id',
        ),
        migrations.AddField(
            model_name='promotii',
            name='produse_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='produse.produse'),
        ),
    ]
