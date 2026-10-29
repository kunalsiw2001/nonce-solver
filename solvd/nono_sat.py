import json,time,sys
from pysat.solvers import Solver
from pysat.card import CardEnc,EncType
def runs(l):
    o=[];c=0
    for x in l:
        if x=='1':c+=1
        elif c:o.append(c);c=0
    if c:o.append(c)
    return o
def solve_board(b,name='cadical195'):
    H,W=b['height'],b['width']; top=[0]
    def nv(): top[0]+=1; return top[0]
    X=[[nv() for c in range(W)] for r in range(H)]
    cls=[]
    def line(clue,cells):
        n=len(cells)
        if not clue:
            for v in cells: cls.append([-v]); return
        k=len(clue); S=[]
        minpre=[sum(clue[:j])+j for j in range(k)]
        suf=[sum(clue[j:])+(k-j-1) for j in range(k)]
        for j,L in enumerate(clue):
            lo=minpre[j]; hi=n-suf[j]
            S.append({p:nv() for p in range(lo,hi+1)})
        for j in range(k):
            vs=list(S[j].values()); cls.append(vs)
            e=CardEnc.atmost(vs,bound=1,top_id=top[0],encoding=EncType.seqcounter); top[0]=max(top[0],e.nv); cls.extend(e.clauses)
        for j in range(k-1):
            L=clue[j]
            for p,v in S[j].items():
                cls.append([-v]+[w for q,w in S[j+1].items() if q>=p+L+1])
        cover=[[] for _ in range(n)]
        for j,L in enumerate(clue):
            for p,v in S[j].items():
                for x in range(p,p+L): cover[x].append(v); cls.append([-v,cells[x]])
        for x in range(n): cls.append([-cells[x]]+cover[x])
    for r in range(H): line(b['rows'][r],X[r])
    for c in range(W): line(b['cols'][c],[X[r][c] for r in range(H)])
    with Solver(name=name,bootstrap_with=cls) as s:
        assert s.solve(); m=set(l for l in s.get_model() if l>0)
    g=["".join('1' if X[r][c] in m else '0' for c in range(W)) for r in range(H)]
    assert all(runs(g[r])==list(b['rows'][r]) for r in range(H)) and all(runs("".join(g[r][c] for r in range(H)))==list(b['cols'][c]) for c in range(W))
    return g
if __name__=="__main__":
    ch=json.load(open(sys.argv[1] if len(sys.argv)>1 else "challenge.json")); out=[]
    for b in ch["boards"]:
        t=time.time(); out.append(solve_board(b)); print("ok",round(time.time()-t,2),flush=True)
    body={"challengeId":ch["challengeId"],"encoding":"bin","boards":out}
    s=json.dumps(body,separators=(",",":")); open("answer.json","w").write(s); print("bytes",len(s),"left",ch["expiresAt"]-time.time())
