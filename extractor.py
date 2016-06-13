import argparse
from optparse import OptionParser
#FOR FILE TYPES with file exension for header use magic library
import mimetypes
from mimetypes import MimeTypes
import os
import zipfile
import tarfile
from os import listdir


inputs  = []
outputs = []

def usage():
 global inputs
 global outputs
 parser = argparse.ArgumentParser(prog='Unzipper', description = "Utility to extract all compressed files. ")

 requiredNamed = parser.add_argument_group('required named arguments') 
 requiredNamed.add_argument('-f','--files', required=True, metavar='File', type=str, nargs='+',help='Files to be extracted')
 requiredNamed.add_argument('-o','--outdir', required=True, metavar='File', type=str, nargs='+',help='Files where to be extracted')

 args = parser.parse_args()
 inputs  = args.files
 outputs = args.outdir
 #print(inputs)

 start = len(outputs)
 end   = len(inputs)
 for i in range(start, end):
  outputs.append(getDirFromPath(inputs[i]))
 #print(outputs)


def getDirFromPath(fullpath):
 #print(fullpath)
 wkspFldr = fullpath.split('\\')[0:-1]
 dirPath = '\\'.join(wkspFldr)

 if not dirPath:
  return os.path.dirname(os.path.abspath(__file__))
 return dirPath


def filetype(file):
 name= ''
 mime = MimeTypes()
 mime_type = mime.guess_type(file)
 #print(mime_type)


 if "application/x-zip-compressed" in mime_type:
  name= "zip"
 elif "gzip" in mime_type:
  name= "gzip"
 elif "application/x-tar" in mime_type:  
  name= "tar"
 return name

def unzip(source_filename, dest_dir):
    print("---------------------")
    print("CONTENTS")
    print("---------------------")


    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            print(member.filename)
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)
    print("---------------------")





usage()



for idx,file in enumerate(inputs):
 print("Unzipping %s " %  file)
 print("File Category", filetype(file))
 if filetype(file) == "zip":
  unzip(file, outputs[idx])


 elif filetype(file) == "gzip":
  tar = tarfile.open(file, "r:gz")
  temp = tar.getnames()
  infoFile = "\n".join(temp)


  print("---------------------")
  print("CONTENTS")
  print("---------------------")
  

  for t in temp:
   directory = os.path.isdir(t)
   if directory :
    print("+ "+ t)
    depthOne = os.listdir(t)
    depthOne = '\n  -'.join(depthOne)
    depthOne = '  -' + depthOne
    print(depthOne)    
   else:
    print("- "+ t)
   
   
  print("---------------------")

  for member in tar.getmembers():
   tar.extract(member, path= outputs[idx])



 
