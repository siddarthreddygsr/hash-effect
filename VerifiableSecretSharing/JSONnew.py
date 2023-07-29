import numpy as np
import random
import json

def create_polynomial(coefficients):
    # Create the polynomial using numpy.poly1d
    polynomial = np.poly1d(coefficients)
    return polynomial

def isPrime(number, itr):
    # prime function to check given number prime or not
    if itr == 1:  # base condition
        return True
    if number % itr == 0:  # if given number divided by itr or not
        return False
    if isPrime(number, itr-1) == False:  # Recursive function Call
        return False
    return True

if __name__ == "__main__":
    g = int(input("enter a value for g : "))
    degree = int(input("enter the degree of the polynomial : "))
    x = int(input("enter a value for x : "))
    p = 4
    while not isPrime(p, p-1):
        p = int(input("enter a prime value for p: "))

    q = 2 * p + 1
    coeff = []
    for i in range(degree):
        coeff.append(random.randint(1, 20))
    polynomial = create_polynomial(coeff)
    y = int(polynomial(x))

    commitments = [pow(g, i, q) for i in coeff]
    rhs = pow(g, y, q)

    # Create the JSON data
    json_data = {
        "share": {
            "index": x,
            "value": {
                "value": hex(y)[2:],  # Convert y to hexadecimal without '0x' prefix
                "prime": hex(p)[2:]   # Convert p to hexadecimal without '0x' prefix
            }
        },
        "commitments": [
            {
                "tag": "prime",
                "data": {
                    "value": hex(commitment)[2:],  # Convert commitment to hexadecimal without '0x' prefix
                    "prime": hex(q)[2:]             # Convert q to hexadecimal without '0x' prefix
                }
            }
            for commitment in commitments
        ],
        "group": {
            "generator": {
                "tag": "prime",
                "data": {
                    "value": hex(g)[2:],  # Convert g to hexadecimal without '0x' prefix
                    "prime": hex(q)[2:]   # Convert q to hexadecimal without '0x' prefix
                }
            },
            "p": hex(p)[2:]             # Convert p to hexadecimal without '0x' prefix
        }
    }

    # Convert the JSON data to a JSON-formatted string
    json_string = json.dumps(json_data, indent=4)
    with open('output.json', 'w') as file:
        file.write(json_string)

    # Print the JSON-formatted string
    print(json_string)
