import os

startSearchPath = "."
storePath = "./result.txt"

print "Starting parsing Measure files from path: " + startSearchPath

for root, dirs, files in os.walk(startSearchPath):
    #print files
	for file in files:
		#print file
		if file.endswith("MEAS.txt"):
			print "Found MEAS file: " + file
			#print root
			fileIn = os.path.join(root, file)
			print fileIn
			in_file = open(fileIn,"r")
			#read only the first line
			text = in_file.readline()
			in_file.close()
			print "Value from file: " + text

			out_file = open(storePath,"ab+")
			out_file.write(text)
			out_file.close()
