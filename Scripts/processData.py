import math

def alphabetizeAttributeString(data):
	for i in range(len(data)):
		newDict = {}
		for k,v in data[i].items():
			newDict[''.join([c for c in k if c.isalpha() or c == ' '])] = v;
		data[i] = newDict

def convertToNumber(data):
	for ex in data:
		for key in ex.keys():
			try:
				ex[key] = float(ex[key])
			except ValueError:
				ex[key] = ex[key]

def decapitalize(data):
	for ex in data:
		for key in ex.keys():
			if ex[key].isalpha(): ex[key] = ex[key].lower()

def processData(data):
	alphabetizeAttributeString(data)
	#decapitalize names
	decapitalize(data)
	#convert numeric attributes to numbers.
	convertToNumber(data)


	
