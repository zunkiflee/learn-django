'''
import string

allchar = []

for i in range(65,91):
	allchar.append(chr(i))

for i in range(97,123):
	allchar.append(chr(i))

for i in range(10):
	allchar.append(str(i))

print(allchar)
print('------------------')
allchar = list(string.ascii_letters)
allchar.extend([str(i) for i in range(10)])
print(allchar)
'''
import random

def GenerateToken(domain='http://localhost:8000/confirm/'):
	allchar = [ chr(i) for i in range(65,91)]
	allchar.extend([chr(i) for i in range(97,123)])
	allchar.extend([str(i) for i in range(10)])

	emailtoken =''

	for i in range(40):
		emailtoken += random.choice(allchar)

	url = domain + emailtoken
	
	return url


GenerateToken()
print(GenerateToken())