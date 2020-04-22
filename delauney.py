import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Point:
	def __eq__(self,p):
		return self.x==p.x and self.y==p.y
	def __init__(self,x,y,z,c):
		self.x=x
		self.y=y
		self.z=z
		self.city=c
	def __str__(self):
		return "%s: %d %d"%(self.city,self.x,self.y)	
	def __hash__(self):
		return x*8192+y

def nfake(p):
	return p.city[0:4]!="fake"

def ccw(p1,p2,p3):
	vx1,vy1,vx2,vy2 = p2.x-p1.x,p2.y-p1.y,p3.x-p2.x,p3.y-p2.y
	return vx1*vy2-vy1*vx2

gr={}

class Triangle:
	def __eq__(self,p):
		return self.__hash__()==p.__hash__()
	def __str__(self):
		return "(%d; %d) (%d; %d) (%d; %d)" % (self.pts[0].x,self.pts[0].y,self.pts[1].x,self.pts[1].y,self.pts[2].x,self.pts[2].y)
	def __init__(self,p1,p2,p3):
		self.triangles=[None,None,None]
		self.pts=[p1,p2,p3]	
	def __hash__(self):
		p1,p2,p3=self.pts
		return p1.x+p1.y*(2**12)+p2.x*(2**24)+p2.y*(2**36)+p3.x*(2**48)+p3.y*(2**60)
	def center(self):
		return Point(sum([p.x for p in self.pts])/3.0, sum([p.y for p in self.pts])/3.0, None, None)
	def inside(self,p):#2 inside 1 edge 0 outside
		p1,p2,p3=self.pts
		area=abs(ccw(p1,p2,p3))
		are2=abs(ccw(p1,p,p3))+abs(ccw(p,p2,p3))+abs(ccw(p1,p2,p))
		if area!=are2:
			return 0
		if abs(ccw(p1,p,p3))==0:
			return 1
		if abs(ccw(p,p2,p3))==0:
			return 1
		if abs(ccw(p1,p2,p))==0:
			return 1
		return 2

	def replace(self,a,b):
		for i in range(3):
			if self.triangles[i]==a:
				self.triangles[i]=b

	def split(self,p):
		p1,p2,p3=self.pts
		t1,t2,t3=self.triangles

		T1=Triangle(p,p2,p3)
		T2=Triangle(p,p3,p1)
		T3=Triangle(p,p1,p2)

		def work(p,t,T,T2,T3):
			T.triangles=[t,T2,T3]
			if t is None:
				return
			t.replace(self,T)
		work(p1,t1,T1,T2,T3)
		work(p2,t2,T2,T3,T1)
		work(p3,t3,T3,T1,T2)

		

		return [T1,T2,T3]

	def plot(self):
		P=list(filter(nfake,self.pts))
		if len(P)==0:
			return
		P.append(P[0])
		for i in range(len(P)-1):
			gr.setdefault(P[i],set()).add(P[i+1])
			gr.setdefault(P[i+1],set()).add(P[i])
		
		

	def next_triangle(self,p):
		c=self.center()
		for i in range(3):
			p1=self.pts[i]
			p2=self.pts[(i+1)%3]
			if ccw(p1,p2,c)*ccw(p1,p2,p)<0:
				return self.triangles[(i+2)%3]

pts=[]

f=open('usa.txt','r') #file with points
for line in f:
	s=line.split('!')
	y=int((float(s[2])-25)*60)
	x=int((float(s[3])+123)*60)	
	#y=float(s[2])
	#x=float(s[3])
	z=float(s[4])
	pts.append(Point(x,y,z,s[1]))
f.close() 

fake=[\
	Point(-1500,2000,0,"fake city #1"),\
	Point( 4800,2000,0,"fake city #2"),\
	Point( 1650,-2000,0,"fake city #3"),\
]

def Z(pt):
	x=pt.x
	y=pt.y
	ans=0
	for i in range(0,12):
		if x&(1<<i):
			ans+=1<<(2*i+1)
		if y&(1<<i):
			ans+=1<<(2*i)
	return ans

pts.sort(key=lambda pt:Z(pt))

t=Triangle(fake[0],fake[1],fake[2])

s=set([t])

def check(t1,t2):
	for i in range(3):
		for j in range(3):
			if t1.pts[i]==t2.pts[j]:
				if t1.pts[(i+1)%3]==t2.pts[(j+2)%3]:
					x1,y1=t1.pts[i].x,t1.pts[i].y
					x3,y3=t1.pts[(i+1)%3].x,t1.pts[(i+1)%3].y
					
					x0,y0=t1.pts[(i+2)%3].x,t1.pts[(i+2)%3].y
					x2,y2=t2.pts[(j+1)%3].x,t2.pts[(j+1)%3].y
			
					sa=(x0-x1)*(x0-x3)+(y0-y1)*(y0-y3)
					sb=(x2-x1)*(x2-x3)+(y2-y1)*(y2-y3)				

					if sa<0 and sb<0:
						return False
					if sa>=0 and sb>=0:
						return True
	
					sc=abs((x0-x1)*(y0-y3)-(x0-x3)*(y0-y1))
					sd=abs((x2-x1)*(y2-y3)-(x2-x3)*(y2-y1))

					return sc*sb+sa*sd>=0	
from random import choice
			
def work(t1,t2):
	if t1 is None:
		return t2
	if t2 is None:
		return t1
	if not t1 in s:
		if t2 in s:
			return t2
		return None
	if not t2 in s:
		if t1 in s:
			return t1
		return None
	#print(t1)
	#print(t2)
	if not check(t1,t2):
		s.remove(t1)
		s.remove(t2)
		for i in range(3):
			for j in range(3):
				if t1.pts[i]==t2.pts[j]:
					if t1.pts[(i+1)%3]==t2.pts[(j+2)%3]:

						p1 = t1.pts[(i+2)%3]
						p2 = t2.pts[(j+1)%3]

						T1 = t1.triangles[i]
						T2 = t1.triangles[(i+1)%3]
						T3 = t2.triangles[(j+2)%3]
						T4 = t2.triangles[j]

						s1 = Triangle(p1,t1.pts[i],p2)
						s2 = Triangle(p2,t1.pts[(i+1)%3],p1)
	
						s1.triangles = [T3,s2,T2]
						s2.triangles = [T1,s1,T4]

						if T1 is not None:
							T1.replace(t1,s2)
						if T2 is not None:
							T2.replace(t1,s1)
						if T3 is not None:
							T3.replace(t2,s1)
						if T4 is not None:
							T4.replace(t2,s2)

						s.add(s1)
						s.add(s2)
					
						x1 = work(s1,T2)
						x2 = work(s1,T3)
						x3 = work(s2,T4)
						x4 = work(s2,T1)

						x=[x1,x2,x3,x4]
						for y in x:
							if y in s:
								return y
	else:
		return t1		
		
		
	#print("=======")
	#t1.plot()
	#t2.plot()
	#plt.show()
	

for p in pts:
	while t.inside(p)==0:
		t=t.next_triangle(p)
	if t.inside(p)==1:
		print(str(p))
		raise "lol rofl lmao"
	s.remove(t)
	new_triangles = t.split(p)
	for n in new_triangles:
		s.add(n)
	for n in new_triangles:
		t=work(n,n.triangles[0])
	
	

import matplotlib.pyplot as plt
for t in s:
	for p in t.pts:
		t.plot()


P=[]
clr={}
def dfs(p):
	clr[p] = True
	P.append(p)
	for v in gr[p]:
		if clr.get(v) is None:
			dfs(v)
			P.append(p)
		else:
			P.append(v)
			P.append(p)

dfs(pts[0])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('Longtitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation')
ax.plot([p.x/60-123 for p in P], [p.y/60+25 for p in P], [p.z for p in P], 'r-',markersize=2)

plt.show()
