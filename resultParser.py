import os
import zipfile


startSearchPath = "."
storePath = "./mesure.txt"
pattern = "MEAS.txt"
filepattern = "html"
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

class DirSearch(object):

    def __init__(self, dirpath, filextension):
        ''' We have to define some variable for computation '''
        self.startSearchPath = dirpath
        self.pattern = filextension
        self.DirList = []

    def getDirList(self):
        '''Get the list of Files that ends with defined pattern'''
        for root, dirs, files in os.walk(self.startSearchPath):
            # for each dir found
            for currentFile in files:
                #select dir that start with desired pattern
                if currentFile.endswith(self.pattern):
                    fullPath = os.path.realpath(root)
                    print "Found Path {0} " . format(os.path.realpath(root))
                    self.DirList.append(fullPath)
                    #shutil.make_archive("aa", 'zip', os.path.realpath(root))

        if not self.DirList:
            raise Exception ("List is Empty")
        return self.DirList


    def printList(self):
        ''' print array file'''
        print self.DirList


def zip(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    # Retrieve the paths of the folder contents.
    zip_file = zipfile.ZipFile(os.path.join(output_path,"log.zip"), 'w', zipfile.ZIP_DEFLATED)
    for root, folders, files in os.walk(folder_path):
        # Include all subfolders, including empty ones.
        for folder_name in folders:
            absolute_path = os.path.join(root, folder_name)
            relative_path = absolute_path.replace(folder_path + '\\','')
            print "Adding '%s' to archive." % absolute_path
            zip_file.write(absolute_path)
        for file_name in files:
            if not file_name.endswith(".zip"):
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(folder_path + '\\','')
                print "Adding '%s' to archive." % absolute_path
                zip_file.write(absolute_path)
                os.remove(absolute_path)
        print "'%s' created successfully." % absolute_path


    zip_file.close()


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
        for key in self.fileAndResult.keys():
            localList = []
            ' get prefix index '
            start =  key.rfind(prepattern)
            start = start + len(prepattern)
            ' get postfix index of '
            end = key.rfind(postpattern)
            ' compute Test name '
            fileOutputName =  key[start:end]
            ' new value list will have the name and the result'
            localList.append(fileOutputName)
            localList.append(self.fileAndResult.get(key))

            self.fileAndResult[key] = localList

        return self.fileAndResult

    def printResult(self):
        print self.fileAndResult

if __name__ == "1__main__":
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

if __name__ == "__main__":

    ds = DirSearch(startSearchPath, filepattern)
    listDir = ds.getDirList()

    for buildir in listDir:
        print("Zip Dir {0}") . format(buildir)
        zip(buildir,buildir)
