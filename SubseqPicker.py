#!/usr/bin/python
import sys
#from mimify import File
#from time import time
import re
#from twisted.python.util import println
#import math
#import cStringIO

bufferSize = 10000
############################################################################################################################

# Check to see if a string is a header
def isHeader(strg, search=re.compile(r'[^ACGTURYKMSWBDHVNXacgturykmswbdhvnx]').search):
  return bool(search(strg))

############################################################################################################################

############################### AS A FUNCTION ###############################################
def openAndPrepare(filename):
  #t0 = time()
  # open file
  try:
    inFile = open(filename)
  except IOError:
    print >> sys.stderr, "Input file " + filename + " not found!"
    sys.exit()

  headerSize = 0

  # start reading file line by line
  linelen = 0
  line = inFile.readline()
  if isHeader(line):
    header = line
    if header[-1] == '\n':
        header = header[:-1]  
    headerSize = len(line)
    line = inFile.readline()
  linelen = len(line)
  if line[-1] == "\n":
    linelen = linelen - 1
  inFile.seek(0)
  #t1 = time()
  #print t1-t0
  return (inFile, headerSize, linelen, header)  
    
############################### AS A FUNCTION ###############################################
def PickSubseq(inFile, position, length, headerSize, linelen):  
  ## consider adding the header size (position correction) as if we need to read from the current location of the non-lined file
  if position == -1:
      position = inFile.tell()
      if position == 0:
        position += headerSize
        inFile.seek(position)
      #pos
  else:
  ## add the number of \n chars will be met (need to be skipped) to reach to the exact actual position
  ## also add the header size in order to skip it to reach to the actual absolute position
    position = position + (position / linelen) + headerSize
    #inFile.seek(0)
    inFile.seek(position)
  
  substr = inFile.read(length)
  if substr == '':
    return ''

  needed = substr.count('\n')
  #needed = 0
  #(output, needed) = processSequence(substr, output)

  if needed > 0:
    #output = cStringIO.StringIO()
    #substr = substr.strip()
    #trans=''.join('' if chr(c) == '\n' else chr(c) for c in range(256))
    #substr = substr.translate(None, '\n')
    substr = substr.replace('\n','')
    #temp2 = ''
    temp = ''
    while needed > 0:
      temp2 = inFile.read(needed)
      if not temp2:
        break
      temp2 = temp2.replace('\n','')
      needed -= len(temp2)
      temp = '%s%s' %(temp, temp2)
    substr = substr + temp
    #temp = ''
    #output.close()
#  if length <= 4:
#    print '.', '\t'
#  if len(substr) <> length:
#    print len(substr), '  ', length, '       ', oldneeded, ' ', len(temp)
    
  return substr.upper()  
############################### AS A FUNCTION ###############################################
#def processSequence(substr, output):
#  needed = 0
#  for i in xrange(len(substr)):
#    if substr[i] == '\n':
#      #substr[i] = ''
#      needed += 1
#    elif substr[i].islower():
#      output.write(substr[i].upper())
#    else:
#      output.write(substr[i])
#  return (output, needed)
############################### AS A FUNCTION ###############################################
#def PickSubseqWithBuffering(inFile, position, length, headerSize, linelen, buffer):
#  ## if reading from the last location, check whether the required seq. is hold by the buffer    
#  if position == -1 and len(buffer) >= length:
#    substr = buffer[:length]
#    buffer = buffer[length:]   
#    return substr.upper()
#
#  ## consider adding the header size (position correction) as if we need to read from the current location of the non-lined file
#  if position == -1:
#      position = inFile.tell()
#      if position == 0:
#        position += headerSize
#        inFile.seek(position)
#  else:
#  ## add the number of \n chars will be met (need to be skipped) to reach to the exact actual position
#  ## also add the header size in order to skip it to reach to the actual absolute position
#    position = position + (position / linelen) + headerSize
#    inFile.seek(0)
#    inFile.seek(position)
#  
#  substr = inFile.read(length)
#  count = 0
#  while substr.find('\n') <> -1:
#    count = substr.count('\n')
#    substr = substr.replace('\n','')
#    temp = inFile.read(count)
#    if not temp:
#      break
#    substr = substr + temp
#   
#  return substr.upper()  
############################### AS A FUNCTION ###############################################
def finalizeAndClose(afile):
  afile.close()
############################### AS A FUNCTION ###############################################
# get the whole length/size of a file without header or '\n's or EOF
def getActualFileSize(filename):
  (afile, headerSize, linelen, header) = openAndPrepare(filename)
  afile.seek(0,2)               ## seeking to the end of the file
  length = afile.tell()         ## getting the current location
  length -= headerSize          ## subtrating header
  breaks = length/(linelen+1)   ## counting '\n'
  length -= breaks+1            ## subtracting '\n's and EOF too 
  finalizeAndClose(afile)
  return length
############################### AS A FUNCTION ###############################################
