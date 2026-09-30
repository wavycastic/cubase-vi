import re, struct, sys, time
sys.path.insert(0, 'tools')
from cubelib.pe import PE
t0=time.time()
pe = PE(r'E:\Steinberg\Cubase 15\Cubase15.exe')
print('parse', round(time.time()-t0,2), 's')
for s in pe.sections:
    print(f'{s.name:9} vaddr=0x{s.vaddr:08X} vsize=0x{s.vsize:08X} rsize=0x{s.raw_size:08X}')
fns = pe.functions()
print('funcs', len(fns), round(time.time()-t0,2))
starts = {b for b,e in fns}
target = pe.imagebase + 0x1E9B6F0
t1=time.time()
sec = [s for s in pe.sections if s.name=='.text'][0]
buf = pe.bin.data[sec.raw_ptr:sec.raw_ptr+sec.raw_size]
print('text bytes', len(buf))
hits=[]
n=0
for m in re.finditer(rb'[\xe8\xe9](.{4})', buf, re.S):
    p = sec.vaddr + m.start()
    rel = int.from_bytes(m.group(1),'little',signed=True)
    t = pe.imagebase + p + 5 + rel
    n+=1
    if t == target:
        hits.append(pe.imagebase+p)
print('matches',n,'hits',hits, 'scan', round(time.time()-t1,2),'s')
