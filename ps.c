#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#define K 5
int n,m,*cl,*occ,*occs,*nt,*tl,*wh,*un,nu,*a;double pb[64];
unsigned long long s;static inline unsigned long long r(){s^=s<<13;s^=s>>7;s^=s<<17;return s;}
int main(int c,char**v){FILE*f=fopen(v[1],"r");char b[256];fgets(b,256,f);sscanf(b,"p cnf %d %d",&n,&m);
cl=malloc(sizeof(int)*m*K);for(int i=0;i<m*K;i+=K){for(int j=0;j<K;j++)fscanf(f,"%d",&cl[i+j]);int z;fscanf(f,"%d",&z);}
s=atoll(v[3])*2654435761ULL+1;double cb=atof(v[4]);int T=atoi(v[5]);
a=malloc(sizeof(int)*(n+1));FILE*g=fopen(v[2],"r");for(int i=1;i<=n;i++){int ch=fgetc(g);a[i]=(ch=='1');}
int noise=atoi(v[6]); // percent random flips of init
for(int i=1;i<=n;i++) if((int)(r()%100)<noise)a[i]^=1;
int L=2*(n+1);int*cnt=calloc(L,sizeof(int));for(int i=0;i<m*K;i++){int l=cl[i];cnt[l>0?2*l:-2*l+1]++;}
occs=malloc(sizeof(int)*(L+1));occs[0]=0;for(int i=0;i<L;i++)occs[i+1]=occs[i]+cnt[i];occ=malloc(sizeof(int)*m*K);int*fill=calloc(L,sizeof(int));
for(int i=0;i<m*K;i++){int l=cl[i];int x=l>0?2*l:-2*l+1;occ[occs[x]+fill[x]++]=i/K;}
for(int i=0;i<64;i++)pb[i]=pow(1+i,-cb);
nt=calloc(m,sizeof(int));tl=calloc(m,sizeof(int));wh=malloc(sizeof(int)*m);un=malloc(sizeof(int)*m);nu=0;
#define TRUE(l) (a[abs(l)]==((l)>0))
for(int i=0;i<m;i++){for(int j=0;j<K;j++){int l=cl[i*K+j];if(TRUE(l)){nt[i]++;tl[i]^=abs(l);}}if(!nt[i]){wh[i]=nu;un[nu++]=i;}}
int best=nu;time_t t0=time(0);long fl=0;
while(nu){ if((fl&0xfffff)==0){ if(time(0)-t0>T)break;}
 int ci=un[r()%nu];double sum=0,pr[K];int vs[K];
 for(int j=0;j<K;j++){int x=abs(cl[ci*K+j]);vs[j]=x;int lt=a[x]?2*x:2*x+1;int br=0;for(int o=occs[lt];o<occs[lt+1];o++)if(nt[occ[o]]==1)br++;pr[j]=pb[br<63?br:63];sum+=pr[j];}
 double rr=(r()%1000000)/1e6*sum;int j=0;for(;j<K-1;j++){rr-=pr[j];if(rr<=0)break;}
 int x=vs[j];int ot=a[x]?2*x:2*x+1,nl=a[x]?2*x+1:2*x;a[x]^=1;fl++;
 for(int o=occs[ot];o<occs[ot+1];o++){int q=occ[o];nt[q]--;tl[q]^=x;if(!nt[q]){wh[q]=nu;un[nu++]=q;}}
 for(int o=occs[nl];o<occs[nl+1];o++){int q=occ[o];if(!nt[q]){int w=wh[q];un[w]=un[--nu];wh[un[w]]=w;}nt[q]++;tl[q]^=x;}
 if(nu<best){best=nu;}
}
fprintf(stderr,"best %d flips %ld\n",best,fl);
if(!nu){for(int i=1;i<=n;i++)putchar(a[i]?'1':'0');putchar('\n');return 0;}return 1;}
