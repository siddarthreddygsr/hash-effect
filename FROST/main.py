from functools import reduce
import numpy as np
import random
import sys
import hashlib
import operator
from fractions import Fraction
sys.set_int_max_str_digits(10000000)


def hash(a,b,p):
	combined_string = str(a) + str(b)
	combined_bytes = combined_string.encode('utf-8')
	sha256_hash = hashlib.sha256(combined_bytes).hexdigest()
	return int(sha256_hash,16)%p

def create_polynomial(degree):
	coefficients = []
	for i in range(degree+1):
		coefficients.append(random.randint(1,10))
	polynomial = np.poly1d(coefficients)
	return polynomial

no_of_nodes = int(input("enter no of nodes : "))
threshold = int(input("enter a value for theshold : "))
g = int(input("enter a value for g : "))
degree = threshold - 1
p = 11
q = 23

polynomial_list = []
commit_list = []

for i in range(no_of_nodes):
	polynomial_list.append(create_polynomial(degree))

print(polynomial_list)

for i in polynomial_list:
	commit_i = []
	for j in i:
		commit_i.append(pow(g,j))
	commit_list.append(commit_i)

k = random.randint(1,10)
r = g**k
secrets = []
y = []
u = []
c = []

for i in range(no_of_nodes):
	secret = int(polynomial_list[i][0])
	secrets.append(secret)
	y.append(int(pow(g,secret)))

signatures = []
for i in range(no_of_nodes):
	# c.append(hash(r,y[i],p))
	c.append(hash(r,pow(g,sum(secrets)),p))
	u_i = k + hash(r,y[i],p)*secrets[i]
	u.append(u_i)
	signatures.append([u_i,r])


print("y = ",y)
print("secrets = ",secrets)
print("u = ", u)
print("signatures = ",signatures)
print("c = ",c)

# print(g,u[0],k)
# print(y[0],c[0])
# lhs = pow(g,u[0])
# rhs = pow(y[0],c[0])*r
# print(lhs,rhs)

for i in range(no_of_nodes):
	lhs = pow(g,u[i])%p
	rhs = pow(y[i],c[i])*r%p
	print(lhs,rhs)
	if lhs == rhs:
		print(f"signature {i} is valid")

slave_shares = []
total_share = []
for i in range(no_of_nodes):
	slave_share = []
	s = 0
	for j in range(no_of_nodes):
		share = []
		share.append(i+1)
		share.append(polynomial_list[j](i+1)%p)
		s += polynomial_list[j](i+1)%p
		slave_share.append(share)
	slave_shares.append(slave_share)
	total_share.append(s%p)
print(slave_shares)
print(total_share)

global_secret = 1
for i in secrets:
	global_secret *= g**i
print(global_secret)

pi = int(input("enter a value for pi : "))

d_e = []
d_e_cap = []
for i in range(no_of_nodes):
	d_e_i = []
	d_e_cap_i = []
	for i in range(pi):
		d_e_i_pi = []
		d_e_cap_i_pi = []
		d = random.randint(1,25)
		e = random.randint(1,25)
		d_cap = pow(g,d)
		e_cap = pow(g,e)
		d_e_cap_i_pi.append(d_cap)
		d_e_cap_i_pi.append(e_cap)
		d_e_i_pi.append(d)
		d_e_i_pi.append(e)
		d_e_cap_i.append(d_e_cap_i_pi)
		d_e_i.append(d_e_i_pi)
	d_e_cap.append(d_e_cap_i)
	d_e.append(d_e_i)


print(d_e)
print(d_e_cap)

b = []
for i in range(threshold):
	temp = [i+1] + d_e_cap[i][0]
	b.append(temp)
print("b: ",b)
message = input("enter a message : ")
verifier = [message,b]
print("verifier : ", verifier)

p_hash = []
combined_string = message + str(verifier)
for i in range(no_of_nodes-1):
	stringtohash = str(i) + combined_string
	stringtohash = stringtohash.encode('utf-8')
	sha256_hash = hashlib.sha256(stringtohash).hexdigest()
	hashed = int(sha256_hash,16)%p
	p_hash.append(hashed)
print(p_hash)

c_hash = []

for i in range(threshold):
	combined_string = str(r) + str(y[i]) + message
	stringtohash = str(i) + combined_string
	stringtohash = stringtohash.encode('utf-8')
	sha256_hash = hashlib.sha256(stringtohash).hexdigest()
	hashed = int(sha256_hash,16)%p
	c_hash.append(hashed)

print("c hash : " ,c_hash)

z = []
lamdas = []
for i in range(threshold):
	lamda = Fraction(1, 1)
	for j in range(1,i+1):
		if i != j:
				lamda *= Fraction(j, j - i)
	lamdas.append(lamda)
	z_i = d_e[i][0][0] + d_e[i][0][1]*p_hash[i] + c_hash[i]*secrets[i]*lamda
	z.append(z_i)
z_cap = sum(z)

print("lamdas : ", lamdas)

new_r = 1
for i in range(threshold):
	d = d_e_cap[i][0][0]
	e = d_e_cap[i][0][1]
	r_i = d*pow(e,p_hash[i])
	new_r *= r_i
	lhs = pow(int(g),int(z[i]),int(p))
	rhs = pow(y[i],int(lamdas[i]*c_hash[i]),p)*r_i%p
	print(lhs,rhs)

lhs = pow(g,int(z_cap),p)
comity = pow(g,sum(y),p)
new_c = reduce(operator.mul, c_hash)
# new_c = sum(c_hash)
rhs = pow(comity,new_c,p)*new_r%p

print(c_hash)
# lhs = pow(g, int(z_cap), p)
# comity = pow(g, sum(secrets), p)
# new_c = reduce(operator.mul, c_hash)
# rhs = pow(comity, new_c, p) * new_r % p
print(lhs,rhs)
# print(comity)
