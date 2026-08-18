import json,re,os,unicodedata

cs=json.load(open('cars_raw.json'))

PREMIUM={'BMW','Audi','Mercedes-Benz','Tesla','Polestar','Lexus','Cupra','Alfa Romeo','Volvo'}

def price(c):
    pl=c['price'].get('available_price_list') or {}
    cand=[(int(k.split('_')[1]),v) for k,v in pl.items() if k.startswith('b2c_') and not k.endswith('_old') and isinstance(v,(int,float))]
    if not cand: return None,None
    cand.sort()
    # longest term = cheapest monthly (finn shows lowest)
    best=min(cand,key=lambda t:t[1])
    return round(best[1]),best[0]

def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def eq(c,k):
    v=(c.get('equipment') or {}).get(k) or ''
    parts=[p.strip() for p in re.split(r'[,٫]',v) if p.strip()]
    return parts

out=[]
for c in cs:
    p,term=price(c)
    if not p: continue
    brand=c['brand']['id'] if isinstance(c['brand'],dict) else c['brand']
    model=c['model']
    ct=c['cartype']
    img=(c.get('picture') or {}).get('url','')
    img=img.replace('width=1280','width=900')
    cid=c['id']
    seats=int(c.get('seats') or 5)
    size=c.get('vehicle_size') or {}
    out.append(dict(
        id=cid,
        brand=brand, model=model, trim=c.get('trim_name') or '',
        type=ct, seats=seats, doors=int(c.get('doors') or 5),
        fuel=c.get('fuel') or '', gear=c.get('gearshift') or '',
        power_kw=c.get('power') or 0, ps=round((c.get('power') or 0)*1.36),
        price=p, term=term, msrp=c['price'].get('msrp') or 0,
        drive=c.get('config_drive') or '', color=((c.get('color') or {}).get('specific') or (c.get('color') or {}).get('id') or '') if isinstance(c.get('color'),dict) else (c.get('color') or ''),
        ev_range=int(float(c['ev_range'])) if c.get('ev_range') else None, consumption=c.get('consumption'),
        efficiency=c.get('efficiency_class') or '',
        length=size.get('length_mm'),
        available=c.get('available_from') or '',
        img_url=img, img='assets/cars/%s.webp'%cid,
        safety=eq(c,'safety')[:6], comfort=eq(c,'comfort')[:6],
        premium=brand in PREMIUM,
        engine=c.get('engine') or '', hitch=(str(c.get('has_hitch')).lower()=='true'),
        terms={int(k.split('_')[1]):round(v) for k,v in (c['price'].get('available_price_list') or {}).items() if k.startswith('b2c_') and not k.endswith('_old') and isinstance(v,(int,float))},
        km={int(k.split('_')[1]):round(v) for k,v in c['price'].items() if k.startswith('extra_') and k.split('_')[1].isdigit() and not k.endswith('_old') and isinstance(v,(int,float))},
        km_extra=c['price'].get('extra_km_price'),
    ))

# dedupe by brand+model+drivetrain — a Corolla Benzin and a Corolla Hybrid are
# two different offers, and collapsing them hides the whole drivetrain segment
best={}
for o in out:
    k=(o['brand'],o['model'],o['fuel'])
    if k not in best or o['price']<best[k]['price']: best[k]=o
out=list(best.values())

# FINN's `fuel` field calls plenty of hybrids "Benzin" — only the engine string
# gives it away. A drivetrain-first homepage lives or dies on this being right.
def drivetrain(o):
    f = o['fuel']
    if f == 'Elektro': return 'elektro'
    if f == 'Plug-In-Hybrid' or 'hybrid' in o['engine'].lower(): return 'hybrid'
    return 'verbrenner'

def seg(o):
    s=[]
    if o['type'] in ('Klein- und Kompaktwagen','Hatchback') or o['price']<=350: s.append('small')
    if o['type'] in ('SUV','Kombi','Van','Limousine') and o['seats']>=5: s.append('family')
    score=o['msrp']/1000 + o['ps']/5 + (25 if o['premium'] else 0) + (20 if o['type'] in ('Coupé','Cabriolet') else 0)
    o['sport_score']=round(score)
    if score>=95: s.append('sport')
    if not s: s.append('family')
    return s
for o in out:
    o['drive_type']=drivetrain(o)
    o['seg']=seg(o)

out.sort(key=lambda o:o['price'])
json.dump(out,open('cars.json','w'),ensure_ascii=False,indent=1)
print('total',len(out))
from collections import Counter
print(Counter(x for o in out for x in o['seg']))
print('price range', out[0]['price'], out[-1]['price'])
