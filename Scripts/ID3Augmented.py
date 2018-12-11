from node import Node
from collections import Counter
from math import log
import random

class ID3Augmented:
	def __init__(self, attributes, target, continuousAttr, examples):
		#intialize variables here
		self.continuousAttr = set(continuousAttr)
		self.attributes = list(attributes)
		self.target = target #assume that the target is a discrete attribute... 
		self.root = None

		self.examples = []
		for ex in examples:
			self.examples.append(dict(ex))

	def runTrial(self,numTrials):
		#split the examples, run "buildModel"
		acc = []
		for i in range(numTrials):
			random.shuffle(self.examples)
			train = self.examples[:3*len(self.examples)//4]
			trainBuild = train[:3*len(train)//4]
			trainValid = train[3*len(train)//4:]
			test = self.examples[3*len(self.examples)//4:]
			self.root = self.buildModel(trainBuild, self.target, trainBuild[0][self.target])
			self.prune(self.root, self.target, trainValid)
			acc.append(self.test(self.root, self.target, test)) 
			#print(self.root)
		print('\n')
		print('Test accuracy = ', str(sum(acc) / len(acc)))
			#print('most determininstic attribute ended up being', self.root.attribute)
		return sum(acc) / len(acc)


	def getSplit(self, examples, target, attr):
		#get the optimal boundary for a 
		entropyFun = lambda ex, tC: sum([tC[key] / len(ex) * log(len(ex) / tC[key], 2) for key in tC.keys()]);
		classification = [ex[target] for ex in examples]
		targetCount = Counter(classification)
		initialEntropy = entropyFun(examples, targetCount)

		if attr not in self.continuousAttr:
			return None

		knownEx = [ex for ex in examples if ex[attr] != '?']
		if len(knownEx) == 0: return None
		unknownEx = [ex for ex in examples if ex[attr] == '?']
		candidateBounds = [ex[attr] for ex in knownEx]

		results = [] #entropy results... 
		for num in candidateBounds:
			#num is our current bound. perform the experiment. 
			valueMaps = {'lesser': [], 'greater': []}
			for ex in knownEx:
				if ex[attr] > num: valueMaps['greater'].append(ex)
				else: valueMaps['lesser'].append(ex)

			valueMaps['?'] = unknownEx
			attributeClassCount = {}
			for val, listOfExamples in valueMaps.items():
				attributeClassCount[val] = Counter([ex[target] for ex in listOfExamples])
			curEntropy = sum([len(valueMaps[val]) / len(knownEx) * (initialEntropy - entropyFun(valueMaps[val], count)) for val,count in attributeClassCount.items()])
			results.append(curEntropy)

		return candidateBounds[results.index(max(results))], max(results)

	def buildModel(self, examples, target, default):
		#runs on the examples; returns a node (to be used by runTrial)
		out = Node()
		out.label = default
		if len(examples) == 0: 
			return out

		classification = [ex[target] for ex in examples]
		targetCount = Counter(classification)
		if len(examples[0]) <= 1:
			out.label = max(classification, key=targetCount.get)
			return out

		if len(targetCount) <= 1:
			out.label = [i for i in targetCount.keys()][0]
			return out

		entropyFun = lambda ex, tC: sum([tC[key] / len(ex) * log(len(ex) / tC[key], 2) for key in tC.keys()]);
		initialEntropy = entropyFun(examples, targetCount)

		# for each (remaining attribute), partition based on the attribute value; 
		attributeMaps = {}
		attributeEntropies = {}
		continuousAttributeBounds = {} #maps continuous attributes to valid boundaries.
		for attr in [i for i in examples[0].keys() if i != target]: 
			if attr in self.continuousAttr:
				attributeMaps[attr] = {}
				splitResult = self.getSplit(examples, target, attr)
				if splitResult != None:
					#print("attribute", attr, 'bound is', splitResult[0])
					#store the result...
					continuousAttributeBounds[attr] = splitResult[0]
					attributeEntropies[attr] = splitResult[1]
					for ex in examples:
						exClass = ex[attr]
						if exClass != '?':
							exClass = 'greater' if ex[attr] > splitResult[0] else 'lesser'
						if exClass in attributeMaps[attr]: attributeMaps[attr][exClass].append(ex)
						else: attributeMaps[attr][exClass] = [ex]
				else:
					for ex in examples:
						exClass = ex[attr]
						if exClass in attributeMaps[attr]: attributeMaps[attr][exClass].append(ex)
						else: attributeMaps[attr][exClass] = [ex]
					attributeEntropies[attr] = 0.0
					continuousAttributeBounds[attr] = 0
			else:
				#not continuous...
				attributeMaps[attr] = {}
				for ex in examples: 
					if ex[attr] in attributeMaps[attr]: attributeMaps[attr][ex[attr]].append(ex)
					else: attributeMaps[attr][ex[attr]] = [ex]

				attributeClassCount = {}
				for val, listOfExamples in attributeMaps[attr].items():
					attributeClassCount[val] = Counter([ex[target] for ex in listOfExamples])
				attributeEntropies[attr] = sum([len(attributeMaps[attr][val]) / len(examples) * (initialEntropy - entropyFun(attributeMaps[attr][val], count)) for val,count in attributeClassCount.items()])

		bestAttr = max(attributeEntropies, key=attributeEntropies.get)

		out.label = None
		out.attribute = bestAttr
		out.continuous = bestAttr in self.continuousAttr
		out.continuousBound = continuousAttributeBounds[bestAttr] if bestAttr in self.continuousAttr else 0
		out.defaultChild = self.buildModel([], target, max(classification, key=targetCount.get))

		for val,listOfExamples in attributeMaps[bestAttr].items():
			for ex in listOfExamples:
				del ex[bestAttr]
			tempCount = Counter([ex[target] for ex in listOfExamples])
			mode = max(tempCount, key=tempCount.get)
			out.children[val] = self.buildModel(listOfExamples, target, mode)

			for ex in listOfExamples:
				ex[bestAttr] = val
		return out



	def evaluate(self, node, example):
		#evaluate the 
		curNode = node;
		while curNode.label == None:
			exampleValue = example.get(curNode.attribute,None)
			if curNode.continuous and exampleValue != '?': 
				exampleValue = 'greater' if exampleValue > curNode.continuousBound else 'lesser'
			curNode = curNode.children.get(exampleValue, curNode.defaultChild)
		return curNode.label

	def prune(self, node, target, examples):
		#prune
		if node.attribute != None and len(examples) != 0:
			for val, child in node.children.items():
				childExamples = [ex for ex in examples if ex[node.attribute] == val]
				self.prune(child, target, childExamples)
			labelCount = Counter([ex[target] for ex in examples])
			mostCommonLabel = max(labelCount, key=labelCount.get)
			if self.test(node, target, examples) < (labelCount[mostCommonLabel] / len(examples)):
				node.attribute = None
				node.label = mostCommonLabel
				node.children.clear()
				node.defaultChild = None

	def test(self, node, target, examples):
		#perform testing. 
		return len([ex for ex in examples if ex[target] == self.evaluate(node, ex)]) / len(examples)
