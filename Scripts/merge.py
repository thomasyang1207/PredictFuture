import csv
from parse import parse, getCountryCodes, parseAndRemoveComma

def applyCountryCodes(dataset, countrycodes):
	couldNotMatch = []
	for dat in dataset:
		countryName = ''.join([c for c in dat['Country'] if c.isalpha() or c == '-' or c == ' '])
		substitution = countrycodes.get(countryName, dat['Country'])
		if countryName not in countrycodes: couldNotMatch.append(countryName)
		dat['Country'] = substitution

def mergeDataset(datasets, countrycodes=None):
	#assume that the keys are countries. datasets are the datasets to be merged. countrycodes are the countries. 

	datasetByCountry = {}
	allAttributes = []

	for dataset in datasets:
		for key,val in dataset[0].items():
			if key not in allAttributes: allAttributes.append(key)

	defaultDictionary = {}
	for attribute in allAttributes:
		defaultDictionary[attribute] = '?'

	for dataset in datasets:
		for countryDict in dataset:
			if countryDict['Country'] in datasetByCountry:
				datasetByCountry[countryDict['Country']].update(countryDict)
			else:
				datasetByCountry[countryDict['Country']] = dict(defaultDictionary)
				datasetByCountry[countryDict['Country']].update(countryDict)


	return [val for key,val in datasetByCountry.items() if len(key) <= 4]

def applyCountryCodesPermanently(countrycodes, filename):
	dataset = parse(filename)
	applyCountryCodes(dataset, countrycodes)
	with open(filename, 'w', newline='') as csvfile:
		fieldnames = [k for k in dataset[0].keys()]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for ex in dataset:
			writer.writerow(ex)

def writeCountryCodes(countrycodes, filename):
	with open(filename, 'w', newline='') as csvfile:
		fieldnames = [k for k in countrycodes.keys()]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerow(countrycodes)

if __name__ == '__main__':
	countrycodes = getCountryCodes('..\\Data\\country_codes.csv')
	data1 = parse('..\\Data\\Precipitation.csv')
	data2 = parse('..\\Data\\GlobalDataEdited.csv')
	data3 = parseAndRemoveComma('..\\Data\\Geography.csv')
	data4 = parseAndRemoveComma('..\\Data\\Coastline.csv')
	#writeCountryCodes(countrycodes, '..\\Data\\processed_country_codes.csv')
	#applyCountryCodesPermanently(countrycodes, '..\\Data\\Precipitation.csv')
	mergedDataset = mergeDataset([data1,data2,data3,data4], countrycodes)
	#print([dat['Country'] for dat in mergedDataset])
	for key,val in mergedDataset[1].items():
		print(key, " : ", val)
	print("Number of attributes: ", len(mergedDataset[1]))

	with open('..\\Data\\FinalizedDataset.csv', 'w', newline='') as csvfile:
		fieldnames = [k for k in mergedDataset[0].keys()]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for ex in mergedDataset:
			writer.writerow(ex)

	