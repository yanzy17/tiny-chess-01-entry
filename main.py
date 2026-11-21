import json,os,urllib.request as U
E=os.environ["MAKEFUN_ENV_URL"]
V=[0,100,320,330,500,900,3000]
D={}
for i,h in enumerate("PNBRQK"):D[h]=i+1;D[h.lower()]=-i-1
C=[6-max(abs(i%8*2-7),abs(i//16*2-7)) for i in range(128)]
A={2:(14,18,31,33,-14,-18,-31,-33),3:(15,-15,17,-17),4:(1,-1,16,-16),5:(1,-1,16,-16,15,-15,17,-17),6:(1,-1,16,-16,15,-15,17,-17)}
W="abcdefgh";N=[0];B=30000;K={1:0,-1:0}
def P(p,b):
 r=U.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with U.urlopen(r) as x:return json.load(x)
def LD(f):
 b=[0]*128;r=7;c=0
 for h in f.split()[0]:
  if h=="/":r-=1;c=0
  elif h.isdigit():c+=int(h)
  else:b[r*16+c]=D[h];c+=1
 return b
def M(b,c):
 L=[]
 for s in range(128):
  p=b[s]
  if not p or p*c<0:continue
  t=abs(p)
  if t==1:
   d=16*c;j=s+d
   if not j&0x88 and not b[j]:
    if j>>4 in(0,7):L+=[s|j<<7|q<<14 for q in(2,3,4,5)]
    else:
     L.append(s|j<<7);k=j+d
     if s>>4==(1 if c>0 else 6) and not k&0x88 and not b[k]:L.append(s|k<<7)
   for o in(d-1,d+1):
    j=s+o
    if not j&0x88 and b[j]*c<0:
     if j>>4 in(0,7):L+=[s|j<<7|q<<14 for q in(2,3,4,5)]
     else:L.append(s|j<<7)
  else:
   for o in A[t]:
    j=s+o
    while not j&0x88:
     v=b[j]
     if not v or v*c<0:L.append(s|j<<7)
     if v or t==2 or t==6:break
     j+=o
 return L
def AT(b,s,c):
 for o in(15,17):
  j=s-o*c
  if not j&0x88 and b[j]==c:return 1
 for o in(14,18,31,33,-14,-18,-31,-33):
  j=s+o
  if not j&0x88 and b[j]==2*c:return 1
 for o in(1,-1,15,-15,16,-16,17,-17):
  j=s+o
  if not j&0x88 and b[j]==6*c:return 1
 for o in(1,-1,16,-16):
  j=s+o
  while not j&0x88:
   p=b[j]
   if p:
    if p==4*c or p==5*c:return 1
    break
   j+=o
 for o in(15,-15,17,-17):
  j=s+o
  while not j&0x88:
   p=b[j]
   if p:
    if p==3*c or p==5*c:return 1
    break
   j+=o
 return 0
def MV(b,m):
 f=m&127;t=m>>7&127;p=b[f];cap=b[t];pr=m>>14;c=1 if p>0 else -1;u=(f,t,cap,pr)
 b[f]=0;b[t]=pr*c if pr else p
 if abs(p)==1:
  if f&7!=t&7 and not cap:b[t-16*c]=0
 elif abs(p)==6:
  K[c]=t
  if abs((f&7)-(t&7))==2:
   r=t&~7|(7 if t>f else 0);g=t&~7|(5 if t>f else 3)
   b[g]=b[r];b[r]=0
 return u
def UN(b,m,u):
 f,t,cap,pr=u;p=b[t];c=1 if p>0 else -1
 b[t]=cap;b[f]=c if pr else p
 if abs(p)==1:
  if f&7!=t&7 and not cap:b[t-16*c]=-c
 elif abs(p)==6:
  K[c]=f
  if abs((f&7)-(t&7))==2:
   r=t&~7|(7 if t>f else 0);g=t&~7|(5 if t>f else 3)
   b[r]=b[g];b[g]=0
def O(b,m):
 return 9*abs(b[m>>7&127])-abs(b[m&127])+(m>>14)*90
def EV(b):
 s=0
 for i in range(128):
  p=b[i]
  if p:
   t=abs(p);q=i if p>0 else i^0x70
   v=V[t]+((6-t)*C[q] if t<6 else -2*C[q])
   if t==1:v+=6*(q>>4)
   s+=v if p>0 else -v
 return s
def S(b,c,d,a,be):
 N[0]+=1
 if N[0]>B:raise Exception
 L=M(b,c)
 if d<1:
  s=EV(b)*c
  if s>=be:return s
  if s>a:a=s
  L=[m for m in L if b[m>>7&127] or m>>14]
  L.sort(key=lambda m:O(b,m),reverse=True)
  for m in L:
   u=MV(b,m)
   if AT(b,K[c],-c):UN(b,m,u);continue
   r=-S(b,-c,0,-be,-a);UN(b,m,u)
   if r>=be:return r
   if r>a:a=r
  return a
 L.sort(key=lambda m:O(b,m),reverse=True)
 k=0
 for m in L:
  u=MV(b,m)
  if AT(b,K[c],-c):UN(b,m,u);continue
  k=1
  r=-S(b,-c,d-1,-be,-a);UN(b,m,u)
  if r>=be:return r
  if r>a:a=r
 return a if k else -99999
def PM(m):
 return (int(m[1])-1)*16+W.index(m[0])|((int(m[3])-1)*16+W.index(m[2]))<<7|({"q":5,"r":4,"b":3,"n":2}.get(m[4:],0)<<14)
def UC(m):
 return W[m&7]+str((m>>4&7)+1)+W[m>>7&7]+str((m>>11&7)+1)+("nbrq"[(m>>14)-2] if m>>14 else "")
while 1:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  f=g["fen"];b=LD(f);c=1 if f.split()[1]=="w" else -1
  K[1]=b.index(6);K[-1]=b.index(-6)
  L=[PM(m) for m in g["legal_moves"]];best=L[0];N[0]=0
  for d in range(1,10):
   a=-99999;bm=0
   if best in L:L.remove(best);L.insert(0,best)
   try:
    for m in L:
     u=MV(b,m);r=-S(b,-c,d-1,-99999,-a);UN(b,m,u)
     if r>a:a=r;bm=m
   except:break
   if bm:best=bm
   if a>29000:break
  g=P("/move",{"game":g["game"],"move":UC(best)})
