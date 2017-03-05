import os

startSearchPath = "."
storePath = "./mesure.txt"
pattern = "MEAS.txt"
filePrePattern = "PV_TRD_8226_51_"
filePostPattern = "MEAS.txt"

class FileSearch(object):

    def __init__(self, filepath, pattern):
        ''' We have to define some variable for computation '''
        self.startSearchPath = filepath
        self.pattern = pattern
        self.fileList = []

    def getFileList(self):
        '''Get the list of Files that ends with defined pattern'''
        for root, dirs, files in os.walk(self.startSearchPath):
            # for each file found
            for file in files:
                #select file that ends with desired pattern
                if file.endswith(self.pattern):
                    fileIn = os.path.join(root, file)
                    print "Found file: " + fileIn
                    self.fileList.append(fileIn)
        if not self.fileList:
            raise Exception ("List is Empty")
        return self.fileList

    def printList(self):
        ''' print array file'''
        print self.fileList


class storeResult(object):

    def __init__(self, array):
        self.fileList = array
        self.fileAndResult = {}

    def getResult(self):
        for fileIn in self.fileList:
            print fileIn
            try:
                in_file = open(fileIn,"r")
            except:
                raise Exception ("Unable to read file")
            #read only the number of the first line (deleting new line)
            measureResult = in_file.readline().split(" ")#
            print "Measure Result Value from file: %s is %s" % (fileIn , measureResult[1].rstrip())
            in_file.close()
            # Store only the num
            self.fileAndResult[fileIn] = measureResult[1].rstrip()
        return self.fileAndResult

    def calcOutputName(self, prepattern, postpattern):
        ''' Starting from full file name, we have to understant the test case associated to result  '''
        localList = []
        for key in self.fileAndResult.keys():
            print key
            ' get prefix index '
            start =  key.rfind(prepattern)
            start = start + len(prepattern)
            ' get postfix index of '
            end = key.rfind(postpattern)
            fileOutputName =  key[start:end]
            print fileOutputName
            localList.append(fileOutputName)
            localList.append(self.fileAndResult.get(key))
            print localList
            self.fileAndResult[key] = localList
            return self.fileAndResult

    def printResult(self):
        print self.fileAndResult

if __name__ == "__main__":
    print "Starting parsing Measure files from path: \t %s" % startSearchPath
    print "File Search Pattern: \t %s" %  pattern
    files = FileSearch(startSearchPath, pattern)
    v = files.getFileList()
    files.printList()

    r = storeResult(v)
    dic = r.getResult()
    r.printResult()
    dic = r.calcOutputName(filePrePattern, filePostPattern)
    r.printResult()
