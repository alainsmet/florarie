from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from produse.models import Produse, Categorii, Promotii, Poze, Useri, Comenzi, ItemComanda
from produse.forms import ContactForm, LoginForm, SubsForm, UserForm, PlataForm
import datetime
import random
import sys

def calcul_promo(produs, promotie):
    if promotie.procent == True:
        produs.pret_redus = round(produs.pret * promotie.pret_redus / 100,2)
    else:
        if promotie.pret_redus < produs.pret:
            produs.pret_redus = promotie.pret_redus

def index(request):
    promotii = Promotii.objects.filter(data_sfarsit__gte=datetime.date.today(),
                                       data_inceput__lte=datetime.date.today())
    produse_promotii = []
    produse_rand = []
    for promotie in promotii:
        produse = promotie.produse_id.all()
        for produs in produse:
            calcul_promo(produs, promotie)
            produse_promotii.append(produs)
    
    produse_rand = list(Produse.objects.filter(stoc__gt=0))
    produse_rand = random.sample(produse_rand, 6)
    for produs in produse_rand:
        for produs_promo in produse_promotii:
            if produs.id == produs_promo.id:
                produs.pret_redus = produs_promo.pret_redus
                break
    return render(request,'index.html',{'produse_promotii':produse_promotii,
                                        'produse':produse_rand,
                                        'user':request.user,
                                        'num_art': num_art(request)})

def plante_lista(request):
    categorii = Categorii.objects.all()
    produse = Produse.objects.all()
    promotii = Promotii.objects.filter(data_sfarsit__gte=datetime.date.today(),
                                       data_inceput__lte=datetime.date.today())
    produse_promotii = []
    for promotie in promotii:
        produse_promo = promotie.produse_id.all()
        for produs_promo in produse_promo:
            for produs in produse:
                if produs.id == produs_promo.id:
                    calcul_promo(produs, promotie)
                    produse_promotii.append(produs)
                    break
    return render(request,'plante.html',{'categorii':categorii,
                                         'produse':produse,
                                         'produse_promotii':produse_promotii,
                                         'user':request.user,
                                         'num_art': num_art(request)})

def detaliu_planta(request, produs_nume, produs_id):
    try:
        produs_nume = produs_nume.replace('-',' ')
        produs = Produse.objects.get(id=produs_id)
        promotii = Promotii.objects.filter(data_sfarsit__gte=datetime.date.today(),
                                       data_inceput__lte=datetime.date.today())
        promotie_actuala = None
        for promotie in promotii:
            produse_promo = promotie.produse_id.all()
            for produs_promo in produse_promo:
                if produs.id == produs_promo.id:
                    calcul_promo(produs, promotie)
                    promotie_actuala = promotie
                    break
    except:
        raise Http404("Produsul nu mai există în momentul de faţă spre vanzare.")
    else:
        return render(request,'detaliu_planta.html',{'produs':produs,
                                                     'promotie':promotie_actuala,
                                                     'user':request.user,
                                                     'num_art': num_art(request)})

def categorie(request, categorie_nume, cat_id):
    try:
        categorie_nume = categorie_nume.replace('-',' ')
        categorie = Categorii.objects.get(id=cat_id)
        produse = Produse.objects.filter(categorie=cat_id)
        promotii = Promotii.objects.filter(data_sfarsit__gte=datetime.date.today(),
                                       data_inceput__lte=datetime.date.today())
        for promotie in promotii:
            produse_promo = promotie.produse_id.all()
            for produs_promo in produse_promo:
                for produs in produse:
                    if produs.id == produs_promo.id:
                        calcul_promo(produs, promotie)
                        break
    except:
        raise Http404("Categoria nu există.")
    else:
        return render(request,'categorie.html',{'categorie':categorie,
                                                'produse':produse,
                                                'user':request.user,
                                                'num_art': num_art(request)})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Nu trimite niciun email, dar codul poate fi implementat aici
            # daca este absolut necesar :)
            return render(request, 'contact_trimis.html', {'user':request.user,
                                                           'num_art': num_art(request)})
    else:
        return render(request, 'contact.html', {'form': ContactForm,
                                                'user':request.user,
                                                'num_art': num_art(request)})

def login(request):
    utilizator_valid = True
    try:
        utilizator_gasit = User.objects.get(username=request.user.username)
        utilizator = Useri.objects.get(user=utilizator_gasit.id)
    except:
        utilizator_valid = False
        
    if utilizator_valid:
        return redirect('cont')
    
    if request.method == 'POST':
        if 'login' in request.POST:
            form_log = LoginForm(request.POST)
            form_sub = SubsForm()
            if form_log.is_valid():
                cos_complet = _extragere_cos(request)
                dj_logout(request)
                request.session['cos'] = cos_complet
                request.session.modified = True
                cd = form_log.cleaned_data
                username = cd.get('username')
                password = cd.get('password')
                user = authenticate(request, username=username,
                                    password=password)
                if user is not None:
                    if user.is_active:
                        cos_complet = _extragere_cos(request)
                        dj_login(request, user)
                        request.session['cos'] = cos_complet
                        request.session.modified = True
                        return redirect('cont')
                    
        elif 'creare-cont' in request.POST:
            form_log = LoginForm()
            form_sub = SubsForm(request.POST)
            if form_sub.is_valid():
                form_sub.save()
                cd = form_sub.cleaned_data
                username = cd.get('email')
                password = cd.get('password')
                user = authenticate(request, username=username,
                                    password=password)
                if user is not None:
                    cos_complet = _extragere_cos(request)
                    dj_login(request, user)
                    request.session['cos'] = cos_complet
                    request.session.modified = True
                return redirect('cont')
    else:
        form_log = LoginForm()
        form_sub = SubsForm()
    return render(request, 'login.html', {'formLogin': form_log,
                                          'formSubs': form_sub,
                                          'user': request.user,
                                          'num_art': num_art(request)})

def cont(request):
    utilizator_valid = True
    try:
        utilizator_gasit = User.objects.get(username=request.user.username)
        utilizator = Useri.objects.get(user=utilizator_gasit.id)
    except:
        utilizator_valid = False
        
    if request.method == 'POST':
        form = UserForm(request.POST, instance=utilizator)
        if not utilizator_valid :
            return redirect('autentificare')
        elif form.is_valid():
            form.save()
            mesaj = 'Datele dvs au fost actualizate'
            comenzi = Comenzi.objects.filter(user_id=utilizator.id)
            return render(request, 'cont.html', {'user': request.user,
                                                 'formUser': form,
                                                 'num_art': num_art(request),
                                                 'mesaj': mesaj,
                                                 'comenzi': comenzi})
    else:
        if not utilizator_valid:
            return redirect('autentificare')
        form = UserForm(instance=utilizator)
        comenzi = Comenzi.objects.filter(user_id=utilizator.id)
    return render(request, 'cont.html', {'user': request.user,
                                         'formUser': form,
                                         'num_art': num_art(request),
                                         'comenzi': comenzi})

def logout(request):
    cos_complet = _extragere_cos(request)
    dj_logout(request)
    request.session['cos'] = cos_complet
    request.session.modified = True
    return redirect('index')

def _extragere_cos(request):
  if not request.session.has_key('cos'):
    return {}
  else:
    return request.session['cos']

def golire_cos(request):
    if request.session.has_key('cos'):
        request.session['cos'] = {}

def num_art(request):
    cos_complet = _extragere_cos(request)
    cantitate_totala = 0
    for produs, cantitate in cos_complet.items():
        cantitate_totala += cantitate
    return cantitate_totala

def cos(request):
    cos_complet = _extragere_cos(request)
    promotii = Promotii.objects.filter(data_sfarsit__gte=datetime.date.today(),
                                       data_inceput__lte=datetime.date.today())
    produse = []
    pret_total = 0
    for produs, cantitate in cos_complet.items():
        produs_data = Produse.objects.get(id=produs)
        produs_data.cantitate = cantitate
        produs_data.pret_total = '{:.2f}'.format(int(produs_data.cantitate) * float(produs_data.pret))
        for promotie in promotii:
            produse_promo = promotie.produse_id.all()
            for produs_promo in produse_promo:
                if produs_data.id == produs_promo.id:
                    calcul_promo(produs_data, promotie)
                    produs_data.pret_total = '{:.2f}'.format(int(produs_data.cantitate) * float(produs_data.pret_redus))
                    break
        pret_total += float(produs_data.pret_total)
        produse.append(produs_data)
    pret_total = '{:.2f}'.format(pret_total)
    return render(request, 'cos.html', {'user': request.user,
                                        'produse': produse,
                                        'pret_total': pret_total,
                                        'num_art': num_art(request)})

def adauga_in_cos(request, produs_id, cantitate):
    produs_valid = True
    try:
        produs = Produse.objects.get(id=produs_id)
    except:
        produs_valid = False
    if produs_valid:
        if produs.stoc > 0:
            try:
                cantitate = int(cantitate)
            except:
                cantitate = 1
            if cantitate > produs.stoc:
                cantitate = produs.stoc
            produs_id = str(produs_id)
            if not request.session.has_key('cos'):
                request.session['cos'] = {produs_id: cantitate}
            else:
                cos_complet = request.session['cos']
                if cos_complet.get(produs_id):
                    cos_complet[produs_id] += cantitate
                    if cos_complet[produs_id] > produs.stoc:
                        cos_complet[produs_id] = produs.stoc
                else:
                    cos_complet[produs_id] = cantitate
                request.session['cos'] = cos_complet
            request.session.modified = True
            return redirect('cos')
    return redirect('index')

def stergere_produs_cos(request, produs_id):
    cos_complet = _extragere_cos(request)
    produs_id = str(produs_id)
    if produs_id in cos_complet:
        cos_complet.pop(produs_id)
        request.session['cos'] = cos_complet
        request.session.modified = True
    return redirect('cos')

def verif_login(request):
    utilizator_valid = True
    try:
        utilizator_gasit = User.objects.get(username=request.user.username)
        utilizator = Useri.objects.get(user=utilizator_gasit.id)
    except:
        utilizator_valid = False
    if not utilizator_valid:
        return redirect('autentificare')

def nr_comanda():
    while True:
        numar = 'MJ' + str(random.randrange(1,1000000000)).rjust(9,'0')
        try:
            comanda = Comenzi.objects.get(referinta=numar)
        except:
            break
        
    return numar
    

def plata(request):
    verif_login(request)
    if request.method == 'POST':
        form = PlataForm(request.POST)
        if form.is_valid():
            return redirect('comanda')
    return render(request, 'plata.html', {'user': request.user,
                                          'num_art': num_art(request),
                                          'form': PlataForm})

def comanda(request):
    verif_login(request)
    cos_complet = _extragere_cos(request)
    if len(cos_complet) > 0:
        try:
            user = Useri.objects.get(user=User.objects.get(id=request.user.id))
        except:
            return redirect('index')
        
        comanda_temp = Comenzi.objects.create(referinta=nr_comanda(),
                                              user=user,
                                              tip_plata='NUM')
        promotii = Promotii.objects.filter(data_sfarsit__gte=datetime.date.today(),
                                       data_inceput__lte=datetime.date.today())
        
        for produs, cant in cos_complet.items():
            try:
                produs_q = Produse.objects.get(id=produs)
            except:
                return redirect('index')
            
            produs_q.stoc = max(produs_q.stoc - cant, 0)
            
            promo = False
            for promotie in promotii:
                produse_promo = promotie.produse_id.all()
                for produs_promo in produse_promo:
                    if produs_q.id == produs_promo.id:
                        calcul_promo(produs_q, promotie)
                        promo = True
                        break
            
            if promo == True:
                pret=produs_q.pret_redus
            else:
                pret=produs_q.pret
            
            item = ItemComanda.objects.create(produs_id=produs_q,
                                              cantitate=cant,
                                              pret_unitar=pret)
            item.save()
            produs_q.save()
            comanda_temp.itemi.add(item)
        comanda_temp.save()
        golire_cos(request)
        return render(request, 'comanda.html', {'user': request.user,
                                          'num_art': num_art(request),
                                          'comanda': comanda_temp})
    else:
        return redirect('index')
    
def detaliu_comanda(request, referinta):
    try:
        comanda = Comenzi.objects.get(referinta=referinta)
        itemi_comanda = comanda.itemi.all()
    except:
        raise Http404("Comanda " + str(referinta) + " nu există.")
    return render(request, 'detaliu_comanda.html', {'user': request.user,
                                                    'num_art': num_art(request),
                                                    'comanda': comanda,
                                                    'produse': itemi_comanda})
