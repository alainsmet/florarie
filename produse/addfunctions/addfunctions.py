def normalize_string(raw_string):
    return raw_string.replace('ă','a').replace('â','a').replace('ş','s').replace('ţ','t').replace('î','i').replace('ç','c')

def nice_url(value):
    return normalize_string(value.lower().replace(' ','-'))
