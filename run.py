import sys,subprocess,os,time,threading
cnf,mid,tag=sys.argv[1],int(sys.argv[2]),sys.argv[3]
C=[list(map(int,l.split()[:-1])) for l in open(cnf) if l and l[0] not in 'pc']
opts=[['--sat'],['--sat','--walkinitially=true'],[],['--sat','--target=2'],['--sat','--phase=false'],['--sat','--stable=2']]
import collections
cnt=collections.Counter()
for c in C:
  for l in c: cnt[abs(l)]+=1 if l>0 else -1
open('maj.txt','w').write(''.join('1' if cnt[v]>0 else '0' for v in range(1,1537)))
subprocess.run(['gcc','-O3','-march=native','-o','ps','ps.c','-lm'])
procs=[]
cbs=[3.0,3.4,3.7,4.0,4.4,2.6,5.0,3.2,3.9,4.2]
for j in range(2):
  procs.append(subprocess.Popen(['./ps',cnf,'maj.txt',str(mid*7+j+1),str(cbs[(mid*2+j)%len(cbs)]),'880',str([0,0,5,10][j+ (mid%2)*2])],stdout=subprocess.PIPE,text=True))
for j in range(2):
  o=opts[(mid*4+j)%len(opts)]
  procs.append(subprocess.Popen(['k/build/kissat','-q','-n','--seed=%d'%(mid*4+j+7)]+o+[cnf],stdout=subprocess.PIPE,text=True))
done=threading.Event(); res={}
def watch(p):
  out=p.stdout.read()
  if done.is_set(): return
  if 's SATISFIABLE' in out:
    res['m']=[int(x) for l in out.splitlines() if l.startswith('v') for x in l.split()[1:]]; done.set()
  elif len(out.strip())==1536 and set(out.strip())<=set('01'):
    res['m']=[(i+1) if ch=='1' else -(i+1) for i,ch in enumerate(out.strip())]; done.set()
for p in procs: threading.Thread(target=watch,args=(p,),daemon=True).start()
done.wait(900)
for p in procs: p.kill()
if 'm' in res:
  A=['0']*1536
  for l in res['m']:
    if 0<abs(l)<=1536: A[abs(l)-1]='1' if l>0 else '0'
  A=''.join(A); assert all(any((A[abs(l)-1]=='1')==(l>0) for l in c) for c in C)
  os.makedirs('sol',exist_ok=True); open('sol/%s.txt'%tag,'w').write(A)
  for i in range(10):
    r=subprocess.run('git config user.email a@b.c; git config user.name bot; git add sol; git commit -qm sol; git pull -q --rebase; git push -q',shell=True)
    if r.returncode==0: break
    time.sleep(2)
