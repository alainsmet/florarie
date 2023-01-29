# Generated by Django 3.2.5 on 2021-09-20 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produse', '0005_auto_20210904_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Useri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('adresare', models.CharField(choices=[('DL', 'Domnul'), ('DNA', 'Doamna'), ('DRA', 'Domnisoara')], max_length=3)),
                ('prenume', models.CharField(max_length=80)),
                ('nume', models.CharField(max_length=80)),
                ('strada', models.CharField(max_length=160)),
                ('nr_strada', models.CharField(max_length=10)),
                ('det_adresa', models.CharField(max_length=200)),
                ('judet', models.CharField(max_length=40)),
                ('localitate', models.CharField(max_length=40)),
                ('cod_postal', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Utilizator',
                'verbose_name_plural': 'Utilizatori',
            },
        ),
    ]