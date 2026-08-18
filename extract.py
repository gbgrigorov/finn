import re,json,sys,glob

def load(path):
    h=open(path,encoding='utf-8').read()
    return h.replace('\\"','"').replace('\\u0026','&').replace('\\n','\n')

def objs(u):
    out=[]
    for m in re.finditer(r'\{"availability":', u):
        s=m.start(); d=0; i=s; instr=False; esc=False
        while i < len(u):
            c=u[i]
            if instr:
                if esc: esc=False
                elif c=='\\': esc=True
                elif c=='"': instr=False
            else:
                if c=='"': instr=True
                elif c=='{': d+=1
                elif c=='}':
                    d-=1
                    if d==0:
                        try: out.append(json.loads(u[s:i+1]))
                        except Exception: pass
                        break
            i+=1
    return out

cars={}
for f in sys.argv[1:]:
    for o in objs(load(f)):
        if not isinstance(o,dict): continue
        if 'brand' not in o or 'price' not in o: continue
        cid=o.get('id')
        if not cid or cid in cars: continue
        cars[cid]=o

print('cars:',len(cars))
keys=set()
for c in cars.values(): keys|=set(c.keys())
print(sorted(keys))
json.dump(list(cars.values()), open('cars_raw.json','w'), ensure_ascii=False)
