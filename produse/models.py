from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime

def normalize_string(raw_string):
    return raw_string.replace('ă','a').replace('â','a').replace('ş','s').replace('ș','s').replace('ţ','t').replace('ț','t').replace('î','i').replace('ç','c')

def nice_url(value):
    return normalize_string(value.lower().replace(' ','-').replace(',',''))

class Categorii(models.Model):
    nume = models.CharField(max_length = 80)
    poza = models.ImageField(upload_to='pictures/',
                             default='pictures/none.png', null=True, blank=True)

    def __str__(self):
        return self.nume

    def _get_nice_url(self):
        return nice_url(self.nume)

    url_norm = property(_get_nice_url)

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categorii'
    
class Produse(models.Model):
    nume = models.CharField(max_length = 80)
    nume_latin = models.CharField(max_length = 80, blank=True)
    poza = models.ImageField(upload_to='pictures/',
                             default='pictures/none.png', null=True, blank=True)
    categorie = models.ForeignKey(Categorii, on_delete=models.SET_NULL,
                                  null=True, blank=True)
    specie = models.CharField(max_length = 80, blank=True)
    familie = models.CharField(max_length = 80, blank=True)
    descriere = models.TextField(blank=True)
    pret = models.DecimalField(max_digits=10, decimal_places=2,
                                           default=0)
    stoc = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nume

    def _get_nice_url(self):
        return nice_url(self.nume)

    url_norm = property(_get_nice_url)

    class Meta:
        verbose_name = 'Produs'
        verbose_name_plural = 'Produse'

class Promotii(models.Model):
    pret_redus = models.DecimalField(max_digits=10, decimal_places=2,
                                           default=0)
    procent = models.BooleanField(default=False)
    data_inceput = models.DateField(default=datetime.date.today)
    data_sfarsit = models.DateField(default=datetime.date.today)
    produse_id = models.ManyToManyField(Produse, blank=True)
    
    def __str__(self):
        shown_string = ''
        if self.procent == True:
            shown_string += str(self.pret_redus) + '%'
        else:
            shown_string += str(self.pret_redus) + ' lei'
        shown_string += ' - Debut : ' + str(self.data_inceput)
        shown_string += ' - Sfârșit : ' + str(self.data_sfarsit)
        return shown_string

    def clean(self):
        if self.data_sfarsit < self.data_inceput:
            raise ValidationError('Data de sfârșit nu poate fi mai mică decât data de început.')

    class Meta:
        verbose_name = 'Promoţie'
        verbose_name_plural = 'Promoţii'
    
class Poze(models.Model):
    poza = models.ImageField(upload_to='pictures/',
                             default='pictures/none.png', null=True, blank=True)
    produse_id = models.ForeignKey(Produse, on_delete=models.SET_NULL,
                                  null=True, blank=True)

    def __str__(self):
        return self.nume

    class Meta:
        verbose_name = 'Poza'
        verbose_name_plural = 'Poze'

class Useri(models.Model):
    ADRESARE_CHOICES = [
        ('DL', 'Domnul'),
        ('DNA', 'Doamna'),
        ('DRA', 'Domnisoara')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    adresare = models.CharField(max_length=3, choices=ADRESARE_CHOICES)
    prenume = models.CharField(max_length = 80)
    nume = models.CharField(max_length = 80)
    strada = models.CharField(max_length = 160)
    nr_strada = models.CharField(max_length = 10, blank=True)
    det_adresa = models.CharField(max_length = 200, blank=True)
    judet = models.CharField(max_length = 40)
    localitate = models.CharField(max_length = 40)
    cod_postal = models.CharField(max_length = 10)

    def __str__(self):
        return self.prenume + ' ' + self.nume

    class Meta:
        verbose_name = 'Utilizator'
        verbose_name_plural = 'Utilizatori'

class ItemComanda(models.Model):
    produs_id = models.ForeignKey(Produse, null=True, on_delete=models.SET_NULL)
    cantitate = models.PositiveIntegerField(default=1)
    pret_unitar = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0)

    def __str__(self):
        return 'Produs nr ' + str(self.produs_id) + ' - Cantitate : ' + str(self.cantitate)

    def pret_total(self):
        return '{:.2f}'.format(self.cantitate * float(self.pret_unitar))
        
    class Meta:
        verbose_name = 'Item comanda'
        verbose_name_plural = 'Itemi comanda'

class Comenzi(models.Model):
    PLATA_CHOICES = [
        ('NUM', 'Numerar, la livrare'),
        ('CRD', 'Cu cardul'),
        ('TRB', 'Transfer bancar')
    ]
    referinta = models.CharField(max_length = 80)
    user = models.ForeignKey(Useri, on_delete = models.CASCADE)
    tip_plata = models.CharField(max_length = 3, choices = PLATA_CHOICES)
    platita = models.BooleanField(default = False)
    data_plata = models.DateField(blank = True, null=True)
    livrata = models.BooleanField(default = False)
    data_livrare = models.DateField(blank = True, null=True)
    itemi = models.ManyToManyField(ItemComanda, blank=True)
    data_creare = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Comandă ref. ' + self.referinta

    def pret_total(self):
        pret = 0
        for item in self.itemi.all():
            pret += float(item.pret_unitar) * item.cantitate

        return '{:.2f}'.format(pret)

    def lista_itemi(self):
        return self.itemi.all()

    class Meta:
        verbose_name = 'Comandă'
        verbose_name_plural = 'Comenzi'
