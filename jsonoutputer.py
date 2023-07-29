import numpy as np
import random
from fractions import Fraction
import json
from sympy import mod_inverse, Pow

def isPrime(number, itr):  
    if itr == 1:
        return True
    if number % itr == 0:
        return False
    if isPrime(number, itr - 1) == False:
        return False
    return True

def convert_to_hex(arr):
    hex_array = []
    for row in arr:
        # hex_row = [hex(element) for element in row]
        hex_row = [hex(element)[2:] for element in row] 
        hex_array.append(hex_row)
    return hex_array

def primeField(p):
    return list(range(p))

def groupField(p, g):
    group_field = []
    group_field.append((g ** 0) % p)
    i = 1
    while (g ** i) % p != group_field[0]:
        group_field.append((g ** i) % p)
        i += 1
    return group_field

def create_polynomial(coefficients):
    polynomial = np.poly1d(coefficients)
    return polynomial

def create_shares(f, no_of_shares):
    shares = []
    x = list(range(1,no_of_shares+1))
    for i in x:
        share_i = []
        share_i.append(i)
        share_i.append(f(i))
        shares.append(share_i)
    return shares

def check_share(shares):
    x = []
    y = []
    for i in shares:
        x.append(i[0])
        y.append(i[1])
    print(x, y)

def mod_add(a, b, prime):
    return (a + b) % prime

def mod_sub(a, b, prime):
    return (a - b) % prime

def mod_mul(a, b, prime):
    return (a * b) % prime

def mod_inverse(a, p):
    # Calculate the modular inverse of 'a' modulo 'p' using Extended Euclidean Algorithm
    for b in range(1, p):
        if (a * b) % p == 1:
            return (b*1)%p
    raise ValueError("Inverse does not exist.")

def mod_div(a, b, prime):
    inverse_b = mod_inverse(b, prime)
    return mod_mul(a, inverse_b, prime)

def lagrange_interpolation(points,prime):
    if not points or len(points[0]) != 2:
        raise ValueError("Invalid input. Expected a 2D array with each row containing a point (x, y).")

    M = len(points)
    x_values, y_values = zip(*points)

    def calculate_lagrange_term(i, x):
        term = Fraction(1, 1)
        for j in range(M):
            if i != j:
                term = mod_mul(term,mod_div(x - x_values[j], x_values[i] - x_values[j],prime),prime)
                # term *= Fraction(x - x_values[j], x_values[i] - x_values[j])
        return term

    def generate_secret(x):
        secret = Fraction(0, 1)
        for i in range(M):
            secret = mod_add(secret,mod_mul(y_values[i], calculate_lagrange_term(i, x),prime),prime)
            # secret += y_values[i] * calculate_lagrange_term(i, x)
        return secret

    return generate_secret

if __name__ == "__main__":
    a = 1/3
    print(mod_inverse(-3,5))
    print(-3%5)
    print(mod_inverse(3,11))
    g = 3
    print(mod_inverse(81,11))
    p = int(input("Enter the value of p: "))
    if not isPrime(p, p - 1):
        print("p is supposed to be a prime number")
        exit
    else:
        prime_field = primeField(p)
        print("Prime field: ", prime_field)
        g = int(input("Enter a value for g: "))
        group_field = groupField(p, g)
        x = int(input("enter value: "))
        print((g ** x) % p)

    print(group_field)
    n = len(group_field)
    s = int(input("enter a value for s: "))
    k = int(input("Enter a value for threshold: "))
    if s >= p:
        exit
    if k < 2:
        exit
    coefficients = [s]
    for i in range(k - 1):
        coefficients.insert(0, random.randint(1000, 10000))
    print(coefficients)
    f = create_polynomial(coefficients)
    no_of_shares = int(input("enter the number of shares u want to create: "))
    while no_of_shares < k:
        print(" number of shares should be greater than ", k)
        print("Try again!!")
        no_of_shares = int(input("enter the number of shares u want to create: "))
    shares = create_shares(f, no_of_shares)
    print(shares)
    print(convert_to_hex(shares))

    interpolate = lagrange_interpolation(shares,p)
    secret = interpolate(0)
    hex_secret = hex(int(secret))
    print("Secret:", secret)
    print("Hex Secret:", hex_secret)

    # Output the result as JSON
    output_data = {
        "secret": int(hex_secret,16),
        "shares": [
            {
                "index": share[0],
                "value": {
                    "value": hex(int(share[1]))[2:],
                    "prime": hex(p)[2:]
                }
            }
            for share in shares
        ]
    }

    with open("output.json", "w") as json_file:
        json.dump(output_data, json_file, indent=4)

