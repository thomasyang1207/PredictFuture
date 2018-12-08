import csv

def parse(filename):
	'''
	takes a filename and returns attribute information and all the data in array of dictionaries
	'''
	# initialize variables

	out = []	
	csvfile = open(filename,'r', newline='')
	fileToRead = csv.reader(csvfile)

	headers = next(fileToRead)
	for i in range(0, len(headers)):
		if 'name' in headers[i]:
			headers[i] = 'name'
		elif 'Country' in headers[i]:
			headers[i] = 'Country'
	for row in fileToRead:
		for i in range(0, len(row)):
			row[i] = ''.join([a for a in row[i] if a != '\t'])
		if row[0] != '':
			out.append(dict(zip(headers, row)))

	csvfile.close()

	return out

def parseAndRemoveComma(filename):
	out = []	
	csvfile = open(filename,'r', newline='')
	fileToRead = csv.reader(csvfile)

	headers = next(fileToRead)
	for i in range(0, len(headers)):
		if 'name' in headers[i]:
			headers[i] = 'name'
		elif 'Country' in headers[i]:
			headers[i] = 'Country'
	for row in fileToRead:
		for i in range(0, len(row)):
			row[i] = ''.join([a for a in row[i] if a != '\t'])
			row[i] = row[i].replace(',', '.')
			row[i] = row[i].replace('"', '')
			row[i] = row[i].replace(' km', '')
		if row[0] != '':
			out.append(dict(zip(headers, row)))

	csvfile.close()

	return out

def getCountryCodes(filename):
	myData = parse(filename)
	return dict(zip([dat['name'] for dat in myData], [dat['alpha-3'] for dat in myData]))


if __name__ == '__main__':
	myData = parse('..\\Data\\country_codes.csv')
	print([val for key,val in dict(zip([dat['name'] for dat in myData], [dat['alpha-3'] for dat in myData])).items()])