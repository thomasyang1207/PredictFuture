class Node:
	def __str__(self):
		myString = ""
		
		if self.label != None:
			myString += "Leaf Node. \n"
			myString += "Label: "
			myString += str(self.label)
			myString += "\n"

		if self.attribute != None:
			myString += "Branch Node. \n"
			myString += "Attribute: "
			myString += str(self.attribute)
			myString += "\n"
			if self.continuous:
				myString += 'Attribute is continuous; boundary is: '
				myString += str(self.continuousBound)
			myString += "\n"

		myString += "\n\n"

		for key, val in self.children.items():
			myString += "Child with value: " + str(key) + "\n"
			myString += val.__str__()

		return myString


	def __init__(self):
		self.label = None #None for non-leaf branches; otherwise, label with the actual label
		self.children = {} #values here will be either "lesser" or "greater"
		self.defaultChild = None
		self.attribute = None #None for leaf; attribute for actual; Attribute is a string; attribute tells us what we are testing for.

		self.continuous = False
		self.continuousBound = 0
