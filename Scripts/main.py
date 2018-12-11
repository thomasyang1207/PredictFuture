import parse, math, processData
import statistics as st
import ID3Augmented as ID3

def runModel(data, target):
	processData.processData(data)
	#select attributes...
	if target not in data[0].keys():
		print('Please enter a valid target attribute')
	attributes = [k for k in data[0].keys()]
	
	print('\n\n')
	testAttributes = [['Precipitation', ' Consumption', 'c G Coverage', 'b Proportion of Tech Value', ' research spending per GDP', ' CO Emission', 
	' percentage of manufacturing employment', ' Manufacutring add value', ' Transportation Volume', ' number of ATM', ' not in education or employment', 
	' material footprint', ' Annual growth per employee', ' Annual Growth Rate', 'b Scholars', ' Organized Learning', ' Reading Proficiency', 
	' Malnutritiohn', ' Food insecurities', ' Undernourishment', 'Population', 'Area sq mi', 'Pop Density per sq mi', 
	'Net migration', 'Infant mortality per  births', 'GDP  per capita', 'Literacy ', 
	'Arable ', 'Crops ', 'Other ', 'Climate', 'Birthrate', 'Deathrate', 'Agriculture', 'Industry', 'Service', 'CoastlineLength'],

	['Precipitation','Climate', 'Population', 'Area sq mi', 'Pop Density per sq mi', 'CoastlineLength'],

	['Climate'], ['Area sq mi'], ['Pop Density per sq mi'], ['Industry']
	]

	attributes = testAttributes[1]
	print('Performing experiment for target:', target, ', and attributes: \n', attributes)
	for ex in data:
		keySet = list(ex.keys())
		for k in keySet:
			if k not in attributes and k != target: ex.pop(k)

	print('remaining attributes are: ', data[0].keys())

	#discretize our target, remove unneeded
	targetData = [ex for ex in data if type(ex[target]) != str]
	targetMedian = st.median([val[target] for val in targetData])

	for ex in targetData:
		ex[target] = 'greater' if ex[target] > targetMedian else 'lesser'

	print("median value for target:", target, ': ', targetMedian)

	#set which attribute are continuous, which ones are not... 
	continuous = ['Precipitation','Arable ', 'Crops ', 'Other ', 'Population', 'Area sq mi', 'Pop Density per sq mi','CoastlineLength'] 

	results = []
	for i in range(100):
		model = ID3.ID3Augmented(attributes, target, continuous, targetData)
		results.append(model.runTrial(1))

	print(sum(results) / len(results))










	


if __name__ == '__main__':
	myData = parse.parseAndRemoveComma('..\\Data\\FinalizedDataset.csv')
	runModel(myData, 'Poverty Rate Goal')


