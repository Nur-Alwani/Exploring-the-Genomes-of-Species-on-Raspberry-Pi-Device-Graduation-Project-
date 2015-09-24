#!/usr/bin/python
import sys

# Give the filename, a map of the chromosomes, and the instruction
# Generate a jagged matrix of (difference between location, symbol) tuples
# where each row of the matrix is a chromosome
def getPos(filename, chromeMap, instr):
  # Open the file
  inFile = open(filename, 'r')
  
  myInstr = [[] for i in range(len(chromeMap))]
  
  # Go through the file to count the number of substitutions
  while 1:
    line = inFile.readline()
    if not line:
      break
  
    # Get rid of new line at the end
    line = line[:-1]
  
    # Break apart string by comma
    vals = line.split(',')
  
    # Put each field in a different variable
    type  = int(vals[0])
    chrom = vals[1]
    pos   = int(vals[2])
    old   = vals[3].split('/')[0] # Get old sequence
    new   = vals[3].split('/')[1] # Get new sequence
  
    # Look for particular instruction
    if (type == instr):
      # Chrome gives us the index for the first dimention
      chromInd = chromeMap[chrom]

      # Do things slightly differently for sub, ins, del
      if instr == 0:
        # Sub stores (position, new symbol)
        myInstr[chromInd].append((pos, new))

      elif instr == 1:
        # Del stores (position, length of deleted seq)
        myInstr[chromInd].append((pos, len(old)))

      elif instr == 2:
        # Ins stores (position, inserted seq)
        myInstr[chromInd].append((pos, new))
  inFile.close()
  
  # Convert locations to differences
  for i in xrange(len(chromeMap)):
    # Sort the sublist by location
    myInstr[i].sort()
    
    prevTemp = 0
    currTemp = 0

    # Go through the list, take differences
    for j in xrange(len(myInstr[i])):
      currTemp   = myInstr[i][j][0]
      myInstr[i][j] = (myInstr[i][j][0]-prevTemp, myInstr[i][j][1])
      prevTemp   = currTemp

  return(myInstr)

# Give the filename, a map of the chromosomes, and the 4 instruction matrices
# Each matrix is jagged, consisting of (difference between location, symbol)
# tuples where each row of the matrix is a chromosome
# The 4 instructions are insertions, deletions, substitutions, and special
# substitutions, where special substitutions are one where the substitutions
# are not from {A,C,G,T}
def getPosAll(filename, chromeMap):
  # Open the file
  inFile = open(filename, 'r')
  
  # Insertions, deletions, substitutions, and special substitutions
  myIns = [[] for i in range(len(chromeMap))]
  myDel = [[] for i in range(len(chromeMap))]
  mySub = [[] for i in range(len(chromeMap))]
  mySpecSub = [[] for i in range(len(chromeMap))]

  # Normal substitutions consist only of A, C, G, and T
  normalSubs = ['A', 'C', 'G', 'T']
  
  # Go through the file to count the number of substitutions
  while 1:
    line = inFile.readline()
    if not line:
      break
  
    # Get rid of new line at the end
    line = line[:-1]
  
    # Break apart string by comma
    vals = line.split(',')
  
    # Put each field in a different variable
    type  = int(vals[0])
    chrom = vals[1]
    pos   = int(vals[2])
    old   = vals[3].split('/')[0] # Get old sequence
    new   = vals[3].split('/')[1] # Get new sequence
  
    # Substitution
    if (type == 0):
      # Chrome gives us the index for the first dimention
      chromInd = chromeMap[chrom]

      # Determine whether it's a special substitution
      if (old in normalSubs) and (new in normalSubs):
        # Sub stores (position, old + new symbol)
        mySub[chromInd].append((pos, old+new))
      else:
        # Special sub stores (position, new symbol)
        mySpecSub[chromInd].append((pos, new))

    # Deletion
    elif (type == 1):
      # Chrome gives us the index for the first dimention
      chromInd = chromeMap[chrom]

      # Del stores (position, length of deleted seq)
      myDel[chromInd].append((pos, len(old)))

    # Insertion
    elif (type == 2):
      # Chrome gives us the index for the first dimention
      chromInd = chromeMap[chrom]

      # Ins stores (position, inserted seq)
      myIns[chromInd].append((pos, new))

    # Unrecognized instruction
    else:
      print >> sys.stderr, "Unrecgnized instruction!"

  inFile.close()
  
  # Convert locations to differences
  for i in xrange(len(chromeMap)):
    # Sort the sublist by location
    mySub[i].sort()
    mySpecSub[i].sort()
    myDel[i].sort()
    myIns[i].sort()
    
    # Go through the list, take differences: Do this for each of the
    # instructions
    prevTemp = 0
    currTemp = 0
    for j in xrange(len(mySub[i])):
      currTemp   = mySub[i][j][0]
      mySub[i][j] = (mySub[i][j][0]-prevTemp, mySub[i][j][1])
      prevTemp   = currTemp

    prevTemp = 0
    currTemp = 0
    for j in xrange(len(mySpecSub[i])):
      currTemp   = mySpecSub[i][j][0]
      mySpecSub[i][j] = (mySpecSub[i][j][0]-prevTemp, mySpecSub[i][j][1])
      prevTemp   = currTemp

    prevTemp = 0
    currTemp = 0
    for j in xrange(len(myDel[i])):
      currTemp   = myDel[i][j][0]
      myDel[i][j] = (myDel[i][j][0]-prevTemp, myDel[i][j][1])
      prevTemp   = currTemp

    prevTemp = 0
    currTemp = 0
    for j in xrange(len(myIns[i])):
      currTemp   = myIns[i][j][0]
      myIns[i][j] = (myIns[i][j][0]-prevTemp, myIns[i][j][1])
      prevTemp   = currTemp

  return(mySub, mySpecSub, myDel, myIns)
