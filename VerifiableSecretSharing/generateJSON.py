import numpy as np
import random

def create_polynomial(coefficients):
	# Create the polynomial using numpy.poly1d
	polynomial = np.poly1d(coefficients)
	return polynomial

def isPrime(number,itr):  #prime function to check given number prime or not
	if itr == 1:   #base condition
		return True
	if number % itr == 0:  #if given number divided by itr or not
		return False
	if isPrime(number,itr-1) == False:   #Recursive function Call
		return False
	return True

if __name__ == "__main__":
    g = int(input("enter a value for g : "))
    degree = int(input("enter the degree of the polynomial : "))
    x = int(input("enter a value for x : "))
    p = 4
    while not isPrime(p,p-1):
        p = int(input("enter a prime value for p: "))

    q = 2*p + 1
    coeff = []
    for i in range(degree):
        coeff.append(random.randint(1,20))
    polynomial = create_polynomial(coeff)
    y = int(polynomial(x))
    print(y)
    print(polynomial)
    commitments = []
    for i in coeff:
         temp = pow(g,i)
         commitments.append(temp)
    rhs = g**y
    print(g)
    print(y)
    print("rhs")
    print(rhs)

