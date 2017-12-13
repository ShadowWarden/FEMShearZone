# User inputs a list of nodes 
# Triples of nodes giving each element and Young's mod (E) and poissan's ration (nu)
# specify boundary nodes and Q on them.
# drop rows corresponding to boundary displacements
# shift with (-) sign, columns corresponding to boundary displacements to RS
# solve for remaining qs
# Find e
# Find sigma
from pylab import *

def rtriag(i1,i2,i3):
  # draws a red triangle connecting nodes i1,i2 and i3
  plot([x[i1]+qq[2*i1],x[i2]+qq[2*i2]],[y[i1]+qq[2*i1+1],y[i2]+qq[2*i2+1]],'r')
  plot([x[i2]+qq[2*i2],x[i3]+qq[2*i3]],[y[i2]+qq[2*i2+1],y[i3]+qq[2*i3+1]],'r')
  plot([x[i3]+qq[2*i3],x[i1]+qq[2*i1]],[y[i3]+qq[2*i3+1],y[i1]+qq[2*i1+1]],'r')
def otriag(i1,i2,i3):
  # draws a red triangle connecting nodes i1,i2 and i3
  plot([x[i1],x[i2]],[y[i1],y[i2]],'g')
  plot([x[i2],x[i3]],[y[i2],y[i3]],'g')
  plot([x[i3],x[i1]],[y[i3],y[i1]],'g')

def det(e):
	x13=x[e[0]]-x[e[2]]
	x23=x[e[1]]-x[e[2]]
	y13=y[e[0]]-y[e[2]]
	y23=y[e[1]]-y[e[2]]	
	return ((x13)*(y23)-(x23)*(y13))

def B(e):
	x13=x[e[0]]-x[e[2]]
	x12=x[e[0]]-x[e[1]]	
	x23=x[e[1]]-x[e[2]]
	y13=y[e[0]]-y[e[2]]
	y12=y[e[0]]-y[e[1]]	
	y23=y[e[1]]-y[e[2]]	
	b=array([[y23,0,-y13,0,y12,0],[0,-x23,0,x13,0,-x12],[-x23,y23,x13,-y13,-x12,y12]])/det(e)	
	return b

def D(e):
	E=e[3]
	nu=e[4]	
	return (E/(1-nu-2*nu*nu)*array([[1-nu,nu,0],[nu,1-nu,0],[0,0,0.5*(1-2*nu)]]))

def Q(e):	
	return array([qq[2*e[0]],qq[2*e[0]+1],qq[2*e[1]],qq[2*e[1]+1],qq[2*e[2]],qq[2*e[2]+1]])


def K(e):
	return 0.5*det(e)*dot(dot(B(e).T,D(e)),B(e))

x=loadtxt("case6.x")
y=loadtxt("case6.y")
elem=loadtxt("output.txt")
# boundary q data: node-id q_x q_y
qb=loadtxt("case6.qb")
N=len(elem)
n=len(x)
e=zeros((N,3))
sigma=zeros((N,3))

# print x
# print y
# print elem
print qb
# junk=input()
# print det(elem[1])
# print B(elem[0])
# print B(elem[1])
# print D(elem[0])
# print Q(elem[0])
# for i in range(6):
#   print "%2d: " % i,
#   for j in range(6):
#     print "%5.2f " % (K(elem[0])[i][j]),
#   print ";"
# for i in range(6):
#   print "%2d: " % i,
#   for j in range(6):
#     print "%5.2f " % (K(elem[1])[i][j]),
#   print ";"
# for i in range(6):
#   print "%2d: " % i,
#   for j in range(6):
#     print "%5.2f " % (K(elem[2])[i][j]),
#   print ";"
# for i in range(6):
#   print "%2d: " % i,
#   for j in range(6):
#     print "%5.2f " % (K(elem[3])[i][j]),
#   print ";"

k=zeros((2*n,2*n))
for i in range(len(elem)):
	n1=2*elem[i,0]
	n2=2*elem[i,1]
	n3=2*elem[i,2]
	ii=array([n1,n1+1,n2,n2+1,n3,n3+1],dtype=integer)
	k[meshgrid(ii,ii)]+=K(elem[i])

	print "Iteration no. %d" % (i)
# find rows corresponding to boundary nodes
m=2*len(qb[:,0])
nb=zeros(m,dtype="int")
nb[:]=r_[2*qb[:,0],2*qb[:,0]+1]
ii=argsort(nb)
nb=nb[ii]
qs=(qb[:,1:].T).flatten()[ii]
print nb
print qs
ni=zeros(2*n-m,dtype="int")
j=0
for i in range(2*n):
  if i==nb[j]:
    j+=1
  else:
    ni[i-j]=i
print ni

krest=k[ni,:]

kk=krest[:,ni]
rs=-krest[:,nb]
rest=dot(rs,qb[:,1:].flatten())

print rest

qi=dot(inv(kk),rest)


qq=zeros((2*n,1))
qq[nb,0]=qs
qq[ni,0]=qi
print qq

# print jj
# krest=k[meshgrid(jj,jj)]
# print krest

# f=F[jj]
# q=dot(inv(krest),f)
# qq=zeros(2*n)
# qq[jj]=q
# print qq
# print q

for i in range(len(elem)):
	e[i,:]=dot(B(elem[i]),Q(elem[i])).T
	sigma[i,:]=dot(D(elem[i]),e[i,:]).T
	
print e
print sigma	

sig=zeros((len(elem),2))

sig[:,0]=(sigma[:,0]+sigma[:,1])/2.0-sqrt(4*sigma[:,2]*sigma[:,2]+(sigma[:,0]-sigma[:,1])*(sigma[:,0]-sigma[:,1]))/2.0
sig[:,1]=arctan(sigma[:,2]/(sig[:,0]-sigma[:,1]))

print sig
# get the centroids of the elements for the quiver plot
n=zeros((N,3),dtype="int")
n[:,:]=elem[:,0:3]
n0=n[:,0];n1=n[:,1];n2=n[:,2]
xx=(x[n0]+qq[2*n0].T+x[n1]+qq[2*n1].T+x[n2]+qq[2*n2].T)/3.0
yy=(y[n0]+qq[2*n0+1].T+y[n1]+qq[2*n1+1].T+y[n2]+qq[2*n2+1].T)/3.0

# plot(x,y,'g--')
figure(1)
for i in range(N):
  otriag(n0[i],n1[i],n2[i])
  # rtriag(n0[i],n1[i],n2[i])
ylim([-0.2,0.2])
xlabel(r"$x\rightarrow$")
ylabel(r"$y\rightarrow$")
# title(r"Undistorted mesh");

figure(2)

X,Y=meshgrid(xx,yy)
quiver(xx,yy,sigma[:,2],-sigma[:,2],scale=60)

quiver(xx,yy,sig[:,0]*cos(sig[:,1]),-sig[:,0]*sin(sig[:,1]),scale=60)

for i in range(N):
  # otriag(n0[i],n1[i],n2[i])
  rtriag(n0[i],n1[i],n2[i])

ylim([-0.2,0.2])
xlabel(r"$x\rightarrow$")
ylabel(r"$y\rightarrow$")
# title(r"Plot of Principal stress in the distorted mesh");
show()
