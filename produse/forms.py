from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from produse.models import Useri

OBIECT_ALEGERE =[
    ('cont', 'Contul meu'),
    ('date', 'Datele mele personale'),
    ('produs', 'Informații despre un produs'),
    ('alt', 'Alt subiect')
]

ADRESARE_CHOICES = [
    ('DL', 'Domnul'),
    ('DNA', 'Doamna'),
    ('DRA', 'Domnișoara')
]

PLATA_CHOICES = [
    ('NUM', 'Numerar, la livrare'),
    ('CRD', 'Cu cardul'),
    ('TRB', 'Transfer bancar')
]

class ContactForm(forms.Form):
    subiect = forms.ChoiceField(choices = OBIECT_ALEGERE, required = True,
                                label = 'Alegeți subiectul* ')
    nume = forms.CharField(label = 'Introduceți numele dvs.* ', required = True,
                           max_length = 100)
    email = forms.EmailField(required = True,
                             label = 'Intoduceți email-ul dvs.* ')
    telefon = forms.CharField(max_length = 50,
                              label = 'Completați numărul dvs de telefon ')
    mesaj = forms.CharField(required = True, widget = forms.Textarea,
                            label = 'Mesajul dvs.* ')
    
class LoginForm(forms.Form):
    username = forms.CharField(label = 'Identifiant * (adresa dvs de email) ',
                               required = True)
    password = forms.CharField(widget=forms.PasswordInput,
                               label = 'Parola * ')

class SubsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required = True,
                               min_length = 8, max_length = 40, label='Parolă * ')
    password_conf = forms.CharField(widget=forms.PasswordInput(),
                                    required = True, min_length = 8,
                                    max_length = 40, label='Confirmaţi parolă * ')
    adresare = forms.ChoiceField(choices=ADRESARE_CHOICES,
                                 widget=forms.RadioSelect(), required = True,
                                 label='Adresare * ')

    def save(self):
        cd = self.cleaned_data
        username = cd.get('email')
        email = cd.get('email')
        password = cd.get('password')
        prenume = cd.get('prenume')
        nume = cd.get('nume')
        adresare = cd.get('adresare')
        strada = cd.get('strada')
        nr_strada = cd.get('nr_strada')
        det_adresa = cd.get('det_adresa')
        judet = cd.get('judet')
        localitate = cd.get('localitate')
        cod_postal = cd.get('cod_postal')
        user = User.objects.create_user(username, password=password,
                                        email=email, first_name=prenume,
                                        last_name=nume)
        utilizator = Useri.objects.create(user_id=user.id, email=email,
                                          adresare=adresare, prenume=prenume,
                                          nume=nume, strada=strada,
                                          nr_strada=nr_strada,
                                          det_adresa=det_adresa, judet=judet,
                                          localitate=localitate,
                                          cod_postal=cod_postal)
        return utilizator

    def clean(self):
        super(SubsForm, self).clean()
        cd = self.cleaned_data
        password = cd.get('password')
        password_conf = cd.get('password_conf')
        if not password == password_conf:
            raise forms.ValidationError('Parolele introduse nu sunt identice')
        return cd
        
    class Meta:
        model = Useri
        fields = ['adresare', 'prenume', 'nume', 'strada', 'nr_strada',
                  'det_adresa', 'judet', 'localitate', 'cod_postal', 'email']
        widgets = {'email':forms.EmailInput(attrs={'autocomplete' : 'off'}),
                   'password':forms.PasswordInput(attrs={'autocomplete' : 'off'})}
        labels = {'prenume':'Prenume * ', 'nume':'Nume * ',
                  'email':'Adresă de e-mail * (va fi folosită ca identifiant) ',
                  'det_adresa':'Detalii adresa: bloc, sc., et., ap. (opţional) ',
                  'judet':'Județ * ', 'localitate':'Localitate * ',
                  'strada':'Strada * ', 'nr_strada':'Nr Strada ',
                  'cod_postal':'Cod poștal * '}

class UserForm(forms.ModelForm):
    class Meta:
        model = Useri
        fields = ['email', 'adresare', 'prenume', 'nume', 'strada', 'nr_strada',
                  'det_adresa', 'judet', 'localitate', 'cod_postal']
        labels = {'adresare':'Adresare * ', 'prenume':'Prenume * ', 'nume':'Nume * ',
                  'email':'Adresă de e-mail * ',
                  'det_adresa':'Detalii adresa: bloc, sc., et., ap. (opţional) ',
                  'judet':'Județ * ', 'localitate':'Localitate * ',
                  'strada':'Strada * ', 'nr_strada':'Nr Strada ',
                  'cod_postal':'Cod poștal * '}

class PlataForm(forms.Form):
    tip_plata = forms.ChoiceField(choices=PLATA_CHOICES,
                                 widget=forms.RadioSelect(), label='')
