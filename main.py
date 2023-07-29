import numpy as np
import random
from fractions import Fraction

def isPrime(number,itr):  #prime function to check given number prime or not
	if itr == 1:   #base condition
		return True
	if number % itr == 0:  #if given number divided by itr or not
		return False
	if isPrime(number,itr-1) == False:   #Recursive function Call
		return False
	return True

def convert_to_hex(arr):
    hex_array = []
    for row in arr:
        hex_row = [hex(element) for element in row]
        hex_array.append(hex_row)
    return hex_array

def primeField(p):
  return list(range(p))

def groupField(p,g):
	group_field = []
	group_field.append((g**0)%p)
	i = 1
	while((g**i)%p != group_field[0]):
		group_field.append((g**i)%p)
		i += 1
	return group_field

def create_polynomial(coefficients):
	# Create the polynomial using numpy.poly1d
	polynomial = np.poly1d(coefficients)
	return polynomial

def create_shares(f,no_of_shares):
	shares = []
	for i in range(no_of_shares):
		share_i = []
		x = random.randint(1,100)
		share_i.append(x)
		share_i.append(f(x))
		shares.append(share_i)
	return shares

def check_share(shares):
	x = []
	y = []
	for i in shares:
		x.append(i[0])
		y.append(i[1])
	print(x,y)

def lagrange_interpolation(points):
	if not points or len(points[0]) != 2:
		raise ValueError("Invalid input. Expected a 2D array with each row containing a point (x, y).")

	M = len(points)
	x_values, y_values = zip(*points)

	def calculate_lagrange_term(i, x):
		term = Fraction(1, 1)
		for j in range(M):
			if i != j:
				term *= Fraction(x - x_values[j], x_values[i] - x_values[j])
		return term
	def generate_secret(x):
		secret = Fraction(0, 1)
		for i in range(M):
			secret += y_values[i] * calculate_lagrange_term(i, x)
		return secret

	return generate_secret

if __name__ == "__main__":
	p = int(input("Enter the value of p: "))
	if not isPrime(p,p-1):
		print("p is supposed to be a prime number")
		exit
	else:
		prime_field = primeField(p)
		print("Prime field: ",prime_field)
		g = int(input("Enter a value for g: "))
		group_field = groupField(p,g)
		x = int(input("enter value: "))
		print((g**x)%p)

	print(group_field)
	n = len(group_field)
	s = int(input("enter a value for s: "))
	k = int(input("Enter a value for threshold: "))
	if s >= p:
		exit
	if k < 2:
		exit
	coefficients = [s]
	for i in range(k-1):
		coefficients.insert(0,random.randint(1,10))
	print(coefficients)
	f = create_polynomial(coefficients)
	no_of_shares = int(input("enter the number of shares u want to create: "))
	while ( no_of_shares < k):
		print(" number of shares should be greater than ", k)
		print("Try again!!")
		no_of_shares = int(input("enter the number of shares u want to create: "))
	shares = create_shares(f,no_of_shares)
	print(shares)
	print(convert_to_hex(shares))
	interpolate = lagrange_interpolation(shares[:k])
	print(interpolate(0))
