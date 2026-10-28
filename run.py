import sys,subprocess,os,time,threading
cnf,mid,tag=sys.argv[1],int(sys.argv[2]),sys.argv[3]
C=[list(map(int,l.split()[:-1])) for l in open(cnf) if l and l[0] not in 'pc']
opts=[['--sat'],['--sat','--walkinitially=true'],[],['--sat','--target=2'],['--sat','--phase=false'],['--sat','--stable=2']]
procs=[]
for j in range(4):
  o=opts[(mid*4+j)%len(opts)]
  procs.append(subprocess.Popen(['k/build/kissat','-q','-n','--seed=%d'%(mid*4+j+7)]+o+[cnf],stdout=subprocess.PIPE,text=True))
done=threading.Event(); res={}
def watch(p):
  out=p.stdout.read()
  if 's SATISFIABLE' in out and not done.is_set():
    res['m']=[int(x) for l in out.splitlines() if l.startswith('v') for x in l.split()[1:]]; done.set()
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
