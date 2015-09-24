#!/usr/bin/python
import heapq
import bits
import sys
import math

############################################################################################################################

# This function takes in a list of types of the form (frequency, symbol) and
# generates a huffman table in the form of a dictionary
def makeHuffTable(symbolTupleList):
  # General approach:
  # First make a tree, then traverse the tree to build our dictionary

  # Make the tree:
  # Copy over the list first
  trees = list(symbolTupleList)

  # Turn list into heap
  heapq.heapify(trees)

  # Keep going until we're left with just a root
  while len(trees) > 1:
    # Get the two smallest frequencies
    childR, childL = heapq.heappop(trees), heapq.heappop(trees)

    # Parent consists of the combined frequency and left and right child
    parent = (childL[0] + childR[0], childL, childR)

    # Put the parent back onto the tree
    heapq.heappush(trees, parent)

  # Convert the tree into a table
  huffTable = {}
  treeToTable(trees[0], huffTable)

  # Give back the table
  return huffTable

############################################################################################################################

# Convert a huffman tree into a huffman codebook
def treeToTable(huffTree, huffTable, prefix = ''):
  # We've hit a leaf
  if len(huffTree) == 2:
    # Add an entry to the huffman table
    huffTable[huffTree[1]] = prefix
  else:
    # Call treeToTable on the two children
    treeToTable(huffTree[1], huffTable, prefix+'0')
    treeToTable(huffTree[2], huffTable, prefix+'1')

############################################################################################################################

# Convert a list of values into a tuple of (frequency, value)
def listToSymbolTupleList(myList):
  symbolTupleList = {}
  for i in xrange(len(myList)):
    currSymbol = str(myList[i])
    if not currSymbol in symbolTupleList:
      symbolTupleList[currSymbol] = 1
    else:
      symbolTupleList[currSymbol] += 1
  return [(val,key) for (key,val) in symbolTupleList.iteritems()]

############################################################################################################################

# Write Huffman table in bit format
# First 32 bits tells us how many entries there are in the Huffman table
# Then print out the codeword/key pairs
# 32 bits fixed to tell us the key associated with the codeword
# 8 bits fixed to tell us the length of the codeword
# variable bits to tell us codeword
def writeHuffTable(huffTable, f):

  # Get the number of entries in the Huffman table
  numEntries = len(huffTable.keys())
  numEntriesOut = bin(numEntries)[2:]
  if len(numEntriesOut) > 32:
    print >> sys.stderr, "Number of entries is too long!"
  else:
    numEntriesOut = '0'*(32-len(numEntriesOut))+numEntriesOut

  remainder = 0
  numLeft   = 0
  (remainder, numLeft) = bits.stringToBitsOut(numEntriesOut, f, remainder, numLeft)
  
  # Loop through the keys
  for myKey in huffTable.keys():
    # Turn into binary representation the key, the codeword, and the length of the codeword
    keyOut     = bin(int(myKey))[2:]
    myCodeword = huffTable[myKey]
    myCodeLen  = bin(len(huffTable[myKey]))[2:]
    #print myKey 
    #sys.stdout.flush()
    # 32 bits is not enough for the key, so there is an error
    if len(keyOut) > 32:
      print >> sys.stderr, "Key is too long!"
      continue
    else:
      keyOut = '0'*(32-len(keyOut))+keyOut

    # 8 bits is not enough for the length of the codeword, so there is an error
    if len(myCodeLen) > 8:
      print >> sys.stderr, "Codeword length is too long!"
      continue
    else:
      myCodeLen = '0'*(8-len(myCodeLen))+myCodeLen

    # Write out the key
    (remainder, numLeft) = bits.stringToBitsOut(keyOut, f, remainder, numLeft)
    # Write out the length of the codeword
    (remainder, numLeft) = bits.stringToBitsOut(myCodeLen, f, remainder, numLeft)
    # Write out the codeword
    (remainder, numLeft) = bits.stringToBitsOut(myCodeword, f, remainder, numLeft)
  bits.flushBitsOutput(f, remainder, numLeft)

############################################################################################################################

# Read Huffman table in bit format
# First 32 bits tells us how many entries there are in the Huffman table
# 32 bits fixed to tell us the key associated with the codeword
# 8 bits fixed to tell us the length of the codeword
# variable bits to tell us codeword
def readHuffTable(f):
  huffTable = {}

  buffer = ''
  bufferSize = 0

  # Get the number of codewords
  (numCodewords, buffer, bufferSize) = bits.getVarBits(f, 32, buffer, bufferSize)
  numCodewords = int(numCodewords, 2)

  # Keep reading codewords
  while numCodewords > 0:
    # Get the key
    (key, buffer, bufferSize) = bits.getVarBits(f, 32, buffer, bufferSize)
    key= int(key, 2)

    # Get the codeword length
    (codewordLen, buffer, bufferSize) = bits.getVarBits(f, 8, buffer, bufferSize)
    codewordLen = int(codewordLen, 2)

    (codeword, buffer, bufferSize) = bits.getVarBits(f, codewordLen, buffer, bufferSize)

    huffTable[codeword] = key

    numCodewords -= 1

  return huffTable

############################################################################################################################
############################################################################################################################


################################################################################
# Golomb coded Huffman Table
# Our keys are integers ranging from 0 to [large number].  The lower numbers
# are densely populated, meaning we have all the integers from 0 to 100 (for
# example).  We try to save the amount of storage required to specify the keys,
# so for the sparely populated integers, we take the deltas between successive
# keys and perform Golomb encoding on those deltas.  For the densely populated
# part, we don't specify the key at all; the encoder just assumes the keys are
# one up counted.  In order to do this, we must first specify the number of
# consecutive integers that we have.

# The format of this codebook is as follows:
# 32 bits to specify number of entries in the Huffman table        (tableSize)
# 32 bits to specify first nonconsecutive integer                  (denseSize)
# 32 bits used to specify the parameter M for our Golomb Code      (Msize)
# Variable bits used to specify the key (This is our Golomb code)
# 5 bits used to specify the length of each codeword               (lenSize)
# Variable bits to specify the codeword
tableSize = 32
denseSize = 32
MSize     = 32
countSize = 32
lenSize   = 5
def writeGolombCodedHuffTable(huffTable, f):
  # Get the number of entries in the Huffman table
  numEntries = len(huffTable.keys())

  # Write out the number of entries in the Huffman table
  numEntriesOut = bin(numEntries)[2:]
  if len(numEntriesOut) > tableSize:
    print >> sys.stderr, "Number of entries is too long!"
  else:
    numEntriesOut = '0'*(tableSize-len(numEntriesOut))+numEntriesOut
  remainder = 0
  numLeft   = 0
  (remainder, numLeft) = bits.stringToBitsOut(numEntriesOut, f, remainder, numLeft)

  # Now we need to get a sorted list of the key and item pairs
  sortedKeyValueList = [(int(key),val) for (key,val) in huffTable.iteritems()]
  sortedKeyValueList.sort()

  # Find where our first nonconsecutive number occurs
  sparseStart = 0
  count = 0
  ind   = 0
  ok    = 0 
  while (ok == 0):
    ind = count
    while (sortedKeyValueList[ind-count][0] == ind):
      ok = 1
      ind = ind + 1
    sparseStart = ind-count
    count = count + 1
  count = count - 1

  # Write out the start of the sparse integers
  sparseStartOut = bin(sparseStart)[2:]
  if len(sparseStartOut) > denseSize:
    print >> sys.stderr, "Start of sparse integers too large!"
  else:
    sparseStartOut = '0'*(denseSize-len(sparseStartOut))+sparseStartOut
  (remainder, numLeft) = bits.stringToBitsOut(sparseStartOut, f, remainder, numLeft)

  # Calculate the deltas for the keys in the sparse region
  sparseDeltas = [sortedKeyValueList[i][0]-sortedKeyValueList[i-1][0]-1 for i in xrange(sparseStart,numEntries)]

  # Calculate M parameter in Golomb coding for the deltas
  M = sum(sparseDeltas)/len(sparseDeltas)

  # Write out count
  countOut = bin(count)[2:]
  if len(countOut) > countSize:
    print >> sys.stderr, "count value too large!"
  else:
    countOut = '0'*(countSize-len(countOut))+countOut
  (remainder, numLeft) = bits.stringToBitsOut(countOut, f, remainder, numLeft)

  # Write out M
  MOut = bin(M)[2:]
  if len(MOut) > MSize:
    print >> sys.stderr, "M value too large!"
  else:
    MOut = '0'*(MSize-len(MOut))+MOut
  (remainder, numLeft) = bits.stringToBitsOut(MOut, f, remainder, numLeft)

  # M also tells us the length (in bits) of our remainder part
  MLen = int(math.ceil(math.log(M,2)))

  # Loop through the sorted key/value list
  for ind in xrange(numEntries):
    # Write out the key if we're in the sparse region
    if (ind >= sparseStart):
      # Calculate the quotient and remainder of sparseDeltas divided by M
      quo  = int(sparseDeltas[ind-sparseStart]/M)
      rem = sparseDeltas[ind-sparseStart]%M

      # Get the two parts of the Golomb key
      unaryPart = '1'*quo + '0'
      huffPart  = bin(rem)[2:]
      huffPart  = '0'*(MLen-len(huffPart))+huffPart

      # Golomb code the key
      keyOut = unaryPart + huffPart

      # Write out the key
      (remainder, numLeft) = bits.stringToBitsOut(keyOut, f, remainder, numLeft)

    # Get the codeword
    codeword = sortedKeyValueList[ind][1]

    # Get the length of the codeword in binary
    codeLen  = bin(len(codeword))[2:]

    # Check the size of the codeword length
    if len(codeLen) > lenSize:
      print >> sys.stderr, "Codeword length is too long!"
      continue
    else:
      codeLen = '0'*(lenSize-len(codeLen))+codeLen

    # Write out the length of the codeword
    (remainder, numLeft) = bits.stringToBitsOut(codeLen, f, remainder, numLeft)

    # Write out the codeword
    (remainder, numLeft) = bits.stringToBitsOut(codeword, f, remainder, numLeft)

  bits.flushBitsOutput(f, remainder, numLeft)

############################################################################################################################

# Read Golomb Coded Huffman table in bit format
# See the comments above writeGolombCodedHuffTable for more about the format of
# the table
def readGolombCodedHuffTable(f):
  huffTable = {}

  buffer = ''
  bufferSize = 0

  # Get the number of codewords
  (numCodewords, buffer, bufferSize) = bits.getVarBits(f, tableSize, buffer, bufferSize)
  numCodewords = int(numCodewords, 2)

  # Get the number of consecutive keys
  (sparseStart, buffer, bufferSize) = bits.getVarBits(f, denseSize, buffer, bufferSize)
  sparseStart = int(sparseStart, 2)

  # Get count for the Golomb code (count is the first number in the dense region: usually 0)
  (count, buffer, bufferSize) = bits.getVarBits(f, countSize, buffer, bufferSize)
  count = int(count, 2)

  # Get M for the Golomb code
  (M, buffer, bufferSize) = bits.getVarBits(f, MSize, buffer, bufferSize)
  M = int(M, 2)

  # Calculate the length of the remainder part
  MLen = int(math.ceil(math.log(M,2)))

  ind = 0
  currKey = 0
  prevKey = 0

  # Keep reading codewords
  for ind in xrange(numCodewords):
    # The key's not specified if we're in the dense region
    if ind < sparseStart:
      currKey = count + ind
    else:
      # Decode by Golomb
      # Get the quotient
      quotient = 0
      (currBit, buffer, bufferSize) = bits.getVarBits(f, 1, buffer, bufferSize)
      while (currBit == '1'):
        (currBit, buffer, bufferSize) = bits.getVarBits(f, 1, buffer, bufferSize)
        quotient = quotient + 1
      # Get the remainder
      (remainder, buffer, bufferSize) = bits.getVarBits(f, MLen, buffer, bufferSize)
      remainder = int(remainder, 2)

      # Get the delta between the previous key and the current key
      delta = quotient*M + remainder + 1
 
      # Now get the actual key
      currKey = prevKey + delta

    # Update previous key (needed when we're in the sparse region)
    prevKey = currKey

    # Get the codeword length
    (codewordLen, buffer, bufferSize) = bits.getVarBits(f, lenSize, buffer, bufferSize)
    codewordLen = int(codewordLen, 2)

    # Get the codeword
    (codeword, buffer, bufferSize) = bits.getVarBits(f, codewordLen, buffer, bufferSize)

    huffTable[codeword] = currKey

  return huffTable


################################################################################
# Insertion version of writing the huffman table

# Write Huffman table in bit format
# First 32 bits tells us how many entries there are in the Huffman table
# Then print out the codeword/key pairs
# Key is variable number of bits,
#  00 -> A
#  01 -> C
#  100 -> G
#  101 -> T
#  110 -> N
#  111 -> X (stop of base pair string)
# 8 bits fixed to tell us the length of the codeword
# variable bits fixed to tell us codeword
def writeHuffTable2(huffTable, f):
  # Get the number of entries in the Huffman table
  numEntries = len(huffTable.keys())
  numEntriesOut = bin(numEntries)[2:]
  if len(numEntriesOut) > 32:
    print >> sys.stderr, "Number of entries is too long!"
  else:
    numEntriesOut = '0'*(32-len(numEntriesOut))+numEntriesOut

  remainder = 0
  numLeft   = 0
  (remainder, numLeft) = bits.stringToBitsOut(numEntriesOut, f, remainder, numLeft)
  
  # Loop through the keys
  for myKey in huffTable.keys():
    # Turn into binary representation the key, the codeword, and the length of the codeword
    keyOut = ''
    for i in xrange(len(myKey)):
      if myKey[i] == 'A':
        keyOut += '00'
      elif myKey[i] == 'C':
        keyOut += '01'
      elif myKey[i] == 'G':
        keyOut += '100'
      elif myKey[i] == 'T':
        keyOut += '101'
      elif myKey[i] == 'N':
        keyOut += '110'
    keyOut += '111'
    myCodeword = huffTable[myKey]
    myCodeLen  = bin(len(huffTable[myKey]))[2:]

    # 8 bits is not enough for the length of the codeword, so there is an error
    if len(myCodeLen) > 8:
      print >> sys.stderr, "Codeword length is too long!"
      continue
    else:
      myCodeLen = '0'*(8-len(myCodeLen))+myCodeLen

    # Write out the key
    (remainder, numLeft) = bits.stringToBitsOut(keyOut, f, remainder, numLeft)
    # Write out the length of the codeword
    (remainder, numLeft) = bits.stringToBitsOut(myCodeLen, f, remainder, numLeft)
    # Write out the codeword
    (remainder, numLeft) = bits.stringToBitsOut(myCodeword, f, remainder, numLeft)
  bits.flushBitsOutput(f, remainder, numLeft)

############################################################################################################################

# Read Huffman table in bit format
# First 32 bits tells us how many entries there are in the Huffman table
# Variable bits tell us the key associated with the codeword
#  00 -> A
#  01 -> C
#  100 -> G
#  101 -> T
#  110 -> N
#  111 -> X (stop of base pair string)
# 8 bits fixed to tell us the length of the codeword
# variable bits fixed to tell us codeword
def readHuffTable2(f):
  huffTable = {}

  buffer = ''
  bufferSize = 0

  # Get the number of codewords
  (numCodewords, buffer, bufferSize) = bits.getVarBits(f, 32, buffer, bufferSize)
  numCodewords = int(numCodewords, 2)

  # Keep reading codewords
  while numCodewords > 0:
    # Get the key
    stop = 0
    key = ''
    while stop == 0:
      # First get 1 bit
      (temp, buffer, bufferSize) = bits.getVarBits(f, 1, buffer, bufferSize)

      # If first bit is a 0, then get one more bit
      if (temp == '0'):
        currbp = '0'
        (temp, buffer, bufferSize) = bits.getVarBits(f, 1, buffer, bufferSize)
        currbp += temp
        
        if currbp == '00':
          key += 'A'
        else:
          key += 'C'

      # Otherwise, get two bits
      else:
        currbp = '1'
        (temp, buffer, bufferSize) = bits.getVarBits(f, 2, buffer, bufferSize)
        currbp += temp
        if (currbp == '100'):
          key += 'G'
        elif (currbp == '101'):
          key += 'T'
        elif (currbp == '110'):
          key += 'N'
        else:
          stop = 1

    # Get the codeword length
    (codewordLen, buffer, bufferSize) = bits.getVarBits(f, 8, buffer, bufferSize)
    codewordLen = int(codewordLen, 2)

    (codeword, buffer, bufferSize) = bits.getVarBits(f, codewordLen, buffer, bufferSize)

    huffTable[codeword] = key

    numCodewords -= 1

  return huffTable

############################################################################################################################


# Get a codeword
def getCodeword(f, myHuffTree, leftOver):
  match = 0
  currWord = ''

  while (match == 0):

    # Keep pushing on another bit
    while (len(leftOver) > 0):
      currWord = currWord + leftOver[0]
      leftOver = leftOver[1:]

      if myHuffTree.get(currWord) != None:
        match = 1
        break

    # Get another 8 bits
    if len(leftOver) == 0:
      leftOver = bits.bitsToStringIn(f)

    if leftOver == '':
      return ('', leftOver)

  return (currWord, leftOver)

############################################################################################################################

# Get a key
def getKey(f, myHuffTree, leftOver):
  match = 0
  currWord = ''

  while (match == 0):

    # Keep pushing on another bit
    while (len(leftOver) > 0):
      currWord = currWord + leftOver[0]
      leftOver = leftOver[1:]

      if myHuffTree.get(currWord) != None:
        match = 1
        break

    # Get another 8 bits
    if len(leftOver) == 0:
      leftOver = bits.bitsToStringIn(f)

    if leftOver == '':
      return ('', leftOver)

  return (myHuffTree[currWord], leftOver)

############################################################################################################################

