import csv

def parse(filename):
  '''
  takes a filename and returns attribute information and all the data in array of dictionaries
  '''
  # initialize variables

  out = []  
  csvfile = open(filename,'r')
  fileToRead = csv.reader(csvfile)

  headers = next(fileToRead)

  # iterate through rows of actual data
  for row in fileToRead:
    out.append(dict(zip(headers, row)))

  return out

if __name__ == '__main__':
  myData = parse('Final_Outcome_Updated.csv')
  for ex in myData:
    for key,val in ex.items():
      ex[key] = ''.join([i for i in val if i != '\''])
      if val == "#N/A" or val == "null":
        ex[key] = '?'

  with open('GlobalDataEdited.csv', 'w', newline='') as csvfile:
    fieldnames = [k for k in myData[0].keys()]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for ex in myData:
      writer.writerow(ex)

