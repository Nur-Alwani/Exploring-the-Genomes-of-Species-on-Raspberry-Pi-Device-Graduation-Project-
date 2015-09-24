#!/usr/bin/python
import struct
import sys

############################################################################################################################

def intToFixedBits(int, fixedBits):
  bits = bin(int)[2:]
  while len(bits) < fixedBits:
    bits = '0' + bits
  return "".join(bits)    
############################################################################################################################

# Given a string of 1's and O's, such as '0010101010', write
# out the bits 8 at a time, and put the remaining bits in
# remainder.  numLeft tells us the number of bits we put into
# remainder.
# inString is of type String, f is the filehandler, remainder is of type int,
# and numLeft is of type int
def stringToBitsOut(inString, f, remainder, numLeft):
  numToDo     = len(inString)
  numToGet    = 8-numLeft
  currPointer = 0

  # Make sure we have enough to at least fill up remainder
  if (numToDo >= numToGet):
    # Interpret string as base two
    remainder |= int(inString[currPointer:currPointer+numToGet],2)

    # Write out the byte
    bin_data = struct.pack('>B',remainder)
    f.write(bin_data)

    # Update how many we need to do, our current pounter, number of bits to
    # get, etc.
    numToDo     -= numToGet
    currPointer += numToGet
    numToGet     = 8
    remainder    = 0

    # Keep writing out 8 bits at a time
    while numToDo >= 8:
      # Interpret string as base two
      remainder = int(inString[currPointer:currPointer+numToGet],2)
  
      # Write out the byte
      bin_data = struct.pack('>B',remainder)
      f.write(bin_data)

      # Update how many we need to do, our current pounter, etc
      numToDo -= numToGet
      currPointer += numToGet

    # Fill out the rest
    numLeft = numToDo

    # Put the rest of the string into remainder, making sure to shift the bits
    # appropriately
    if numLeft > 0:
      remainder = (int(inString[currPointer:],2) << (8-numLeft))
    else:
      remainder = 0

  # We don't even have enough to write something out once
  elif (numToDo > 0):
    numToShift = 8 - numToDo - numLeft
    remainder |= (int(inString,2) << (numToShift))
    numLeft   += numToDo

  return(remainder, numLeft)

############################################################################################################################

# Write out the last byte
def flushBitsOutput(f, remainder, numLeft):
  # Write out the byte
  bin_data = struct.pack('>B',remainder)
  f.write(bin_data)

  return(0,0)

############################################################################################################################

# Read in a byte and return it as a string
def bitsToStringIn(f):
  myString = f.read(1)
  if myString != '':
    # Get the bit string
    myString = bin(struct.unpack('>B',myString)[0])[2:]

    # Pad with zeros in front to make sure it's 8 bits long
    myString = '0'*(8-len(myString)) + myString
  return myString

############################################################################################################################

# Read in a variable number of bits.  We need a buffer to keep
# track of leftover bits since we have to read in a byte at a time
def getVarBits(f, numToGet, buffer, bufferSize):
  bitsOut = ''

  # Keep reading bits until we get the amount we want
  while (numToGet > 0):
    # If the buffer's empty, read in another byte
    if bufferSize == 0:
      buffer = bitsToStringIn(f)
      bufferSize = 8

    # Take a bit from the buffer and put it in the output
    bitsOut = bitsOut + buffer[8-bufferSize]
    bufferSize -= 1

    numToGet -= 1

  return (bitsOut, buffer, bufferSize)

############################################################################################################################

# Different version of getVarBits.  I think this one is better because we don't
# have to carry around bufferSize.
def getBits(f, numToGet, leftOver):
  currWord = ''

  for ind in xrange(numToGet):
    # If leftOver is empty, get another 8 bits
    if len(leftOver) == 0:
      leftOver = bitsToStringIn(f)
  
    # Keep pushing on another bit
    currWord = currWord + leftOver[0]
    leftOver = leftOver[1:]

  return (currWord, leftOver)

############################################################################################################################

