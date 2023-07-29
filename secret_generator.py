import json
from fractions import Fraction
from sympy import mod_inverse, Pow

def lagrange_interpolation(points,prime):
	if not points or len(points[0]) != 2:
		raise ValueError("Invalid input. Expected a 2D array with each row containing a point (x, y).")

	M = len(points)
	x_values, y_values = zip(*points)

	def calculate_lagrange_term(i, x):
		term = Fraction(1, 1)
		for j in range(M):
			if i != j:
				term *= (Fraction(x - x_values[j], x_values[i] - x_values[j]))%prime
		return term
	def generate_secret(x):
		secret = Fraction(0, 1)
		for i in range(M):
			secret += (y_values[i] * calculate_lagrange_term(i, x))%prime
		return secret

	return generate_secret

def mod_inverse(a, prime):
    return Pow(a, -1, prime)

print(mod_inverse(0.5,5))
with open('data.json', 'r') as file:
    data = json.load(file)
    k = data["k"]
    n = data["n"]
    shares_list = data["shares"]
    shares = [[share["value"]["value"] for share in shares_list]]
    print(shares)
    prime = int(data["shares"][0]["value"]["prime"],16)
    hex_2d_array = [[share["index"], int(share["value"]["value"],16)] for share in shares_list]
    print(hex_2d_array)
    interpolate = lagrange_interpolation(hex_2d_array,prime)
    print(interpolate(0))
    p = interpolate(0)%prime
    h = hex(int(p))
    print(h)

