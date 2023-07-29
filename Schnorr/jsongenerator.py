import json

def to_json_string(data):
    return json.dumps(data, indent=4)

if __name__ == "__main__":
    g = int(input("enter a value for g: "))
    k = int(input("enter a value for k: "))
    s = int(input("enter a value for s: "))
    sigma = int(input("enter a value for sigma: "))
    y = int(input("enter a public key: "))
    r = pow(g, k)
    c = (sigma - k) // s
    message = input("enter a message: ")

    data = {
        "group": {
            "generator": {
                "tag": "prime",
                "data": {
                    "value": hex(g)[2:],  # Remove '0x' prefix
                    "prime": hex(r)[2:]  # Remove '0x' prefix
                }
            },
            "p": hex(r)[2:]  # Remove '0x' prefix
        },
        "message": message,
        "publicKey": {
            "tag": "prime",
            "data": {
                "value": hex(y)[2:],  # Remove '0x' prefix
                "prime": hex(r)[2:]  # Remove '0x' prefix
            }
        },
        "signature": {
            "r": {
                "tag": "prime",
                "data": {
                    "value": hex(r)[2:],  # Remove '0x' prefix
                    "prime": hex(r)[2:]  # Remove '0x' prefix
                }
            },
            "sigma": {
                "value": hex(sigma)[2:],  # Remove '0x' prefix
                "prime": hex(s)[2:]  # Remove '0x' prefix
            }
        }
    }

    json_string = to_json_string(data)
    print(json_string)
