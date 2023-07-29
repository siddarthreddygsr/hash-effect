def isPrime(number,itr):  #prime function to check given number prime or not
	if itr == 1:   #base condition
		return True
	if number % itr == 0:  #if given number divided by itr or not
		return False
	if isPrime(number,itr-1) == False:   #Recursive function Call
		return False
	return True

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
	print(group_field)