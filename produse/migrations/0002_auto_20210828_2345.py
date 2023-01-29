# Generated by Django 3.2.5 on 2021-08-28 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorii',
            options={'verbose_name': 'Categorie', 'verbose_name_plural': 'Categorii'},
        ),
        migrations.AlterModelOptions(
            name='poze',
            options={'verbose_name': 'Poza', 'verbose_name_plural': 'Poze'},
        ),
        migrations.AlterModelOptions(
            name='produse',
            options={'verbose_name': 'Produs', 'verbose_name_plural': 'Produse'},
        ),
        migrations.AlterModelOptions(
            name='promotii',
            options={'verbose_name': 'Promoţie', 'verbose_name_plural': 'Promoţii'},
        ),
        migrations.RemoveField(
            model_name='promotii',
            name='produse_id',
        ),
        migrations.AddField(
            model_name='produse',
            name='promotie_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='produse.promotii'),
        ),
        migrations.AlterField(
            model_name='produse',
            name='descriere',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='produse',
            name='familie',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='produse',
            name='nume_latin',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='produse',
            name='pret',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produse',
            name='specie',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='promotii',
            name='data_inceput',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='promotii',
            name='pret_redus',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]