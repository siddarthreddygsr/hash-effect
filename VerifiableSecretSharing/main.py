import json

with open('valid-data.json', 'r') as file:
    json_data = file.read()

data = json.loads(json_data)

data_values = []

share_value = []
p = int(data["share"]["value"]["prime"],16)
q = int(data["commitments"][0]["data"]["prime"],16)
g = int(data["group"]["generator"]["data"]["value"])
x = data["share"]["index"]
y = int(data["share"]["value"]["value"],16)
# data_values.append(share_value)
# data_values.append(share_prime)
commitment_values = []

for commitment in data["commitments"]:
    commitment_value = int(commitment["data"]["value"],16)
    commitment_values.append(commitment_value)


# print(commitment_values)
l = len(commitment_values) - 1
# print(l)

master = 1
# for i in commitment_values:
#     slave = x**l
#     master *= (i**slave)%q
#     l = l-1
l = 0
for i in commitment_values:
    gx = i%q
    # for j in range(x**l):
        # master *= gx
        # master = master %q
    master *= pow(i,x**l,q)
    l = l+1
    master = master%q

master = master%q
print(p,q)
print("LHS = ",master)

new_g= g%q
new_master = pow(new_g, y, q)
new_master %= q
print("RHS = ",new_master)
# new_master = 1
# for i in range(y):
#     new_master *= new_g
#     new_master = new_master %q
# new_master = new_master %q
if master == new_master:
    print("valid")
else:
    print("invalid")
