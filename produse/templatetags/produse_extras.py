from django import template
from datetime import date

register = template.Library()

@register.filter
def calc_procent(value, arg):
    procent = int(round((float(arg) - float(value))/float(value) * 100,0))
    return str(procent) + '%'

@register.filter
def timp_restant(data_sfarsit):
    azi = date.today()
    diferenta = data_sfarsit - azi
    sir_formatat = ''
    if diferenta.total_seconds() > 0:
        zile = diferenta.days + 1
        sir_formatat += str(zile) + ' zile rămase'
    elif diferenta.total_seconds() == 0:
        sir_formatat = 'Ultima zi de promoție !'
    return sir_formatat

@register.filter
def initiale(user):
    sir = ''
    try:
        sir += user.first_name[0].upper()
        sir += user.last_name[0].upper()
    except:
        sir = ''
    return sir
            
        
        
    
