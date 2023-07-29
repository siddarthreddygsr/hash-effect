import json
import hashlib


with open('data.json', 'r') as file:
    json_data = file.read()

data = json.loads(json_data)

g = int(data["group"]["generator"]["data"]["value"])
p = int(data["group"]["generator"]["data"]["prime"],16)
q = int(data["group"]["p"],16)
public_key_y = int(data["publicKey"]["data"]["value"],16)
message = data["message"]
r = int(data["signature"]["r"]["data"]["value"],16)
c = int(data["hash"]["value"],16)
# print(c)
sigma = int(data["signature"]["sigma"]["value"],16)
# print(r)
numerator = pow(g,sigma,p)
denominator = pow(public_key_y,c,p)


print(numerator)
print(denominator)

if numerator == denominator*r%p:
    print("valid")
else:
    print("invalid")
# if new_r == r:
#     print("valid")



