#!/usr/bin/python
import sys
import os
import huff
import bits
import chromeMap
import re
from time import time
import SubseqPicker
from twisted.python.util import println

timing = 1
debug = 0

############################################################################################################################
### why instru.s have to hold the next ref./target different chars??
# because the chars at these locations are different, they had no chance to be included by the match/instru. itself
# so, their chance is to be both included inside a substtu./ins./del. if this instru. will be merged by the next instru.
# however, if this chance is not applicable, these chars will be an overhead which may result into new instru. with length 1.
                    #############
### during decompression, have to apply del.s, ins.s, substtu.s
# because while deducing ins.s during compression, they are generated according to positions were not affected by del.s yet
# so, we have to revert del.s back, to get seq.s back as it was before del.s, and get correct ins.s locations/positions                 
# also
# because while deducing substtu.s during compression, they are generated according to positions were not affected by ins.s yet
# so, we have to revert ins.s back, to get seq.s back as it was before ins.s, and get correct substtu.s locations/positions  
############################################################################################################################

# Check to see if a string is a header
def isHeader(strg, search=re.compile(r'[^ACGTURYKMSWBDHVNXacgturykmswbdhvnx]').search):
  return bool(search(strg))

############################################################################################################################

# This function takes as input a reference file and target file, and returns a
# list of tuples containing (position, location, length), which describes how
# to create the target given the reference
def getMatches(refFile, targetFile, memFlag, tempRefFile, tempTargetFile, tempInstructionFile):
  # Constants that we can tweak
  # How far left to look 
  ## (i.e. how much bases to insert into the ref. because its left (previous) bases are matching the current target bases
  ## search ref. for matches on its left side of the current ref./target position
  insSize = 5000
  
  # How far right to look 
  ##(i.e. how much to delete from the ref. bases because its right (next) bases are matching the current target bases
  ## search ref. for matches on its right side of the current ref./target position  
  delSize = 100000
  
  # Length of the window to search over
  winLen = insSize + delSize + 1 
  
  # Length of running average
  chk_size = 100
  
  # Length of match to be considered a valid match
  goodThresh = 30

  # The return variable
  myInstructions = []
  numInstructions = 0
  if memFlag == 0:
    instructionTemp = open(tempInstructionFile, 'w')

  #header = ""
  
                                ##################### Reading Reference & Target Genomes each to one long string/file ########################
  #ts = time()
  #if(timing == 1):
  #  t0 = time()

#***
#  # Open the reference file
#  try:
#    inFile = open(refFile)
#  except IOError:
#    print >> sys.stderr, "Reference file " + refFile + " not found!"
#    sys.exit()
#  # Open the reference for writing
#  if memFlag == 0:
#    refTemp = open(tempRefFile, "w")
#
#  # Length of reference
#  refLength = 0
#
#  # Skip the header if it exists
#  refString = ''
#  firstLine = inFile.readline()
#  firstLine = firstLine[:-1]        ## skipping the '\n'
#
#
#  if not isHeader(firstLine):
#    refLength = refLength + len(firstLine)
#    if memFlag == 1:
#      refString = firstLine
#    else:
#      refTemp.write(firstLine)
#
#  # Get the entire reference sequence
#  while 1:
#    line = inFile.readline()
#    if not line:
#      break
#
#    # Append the new line to the string
#    if line[-1] == "\n":
#      refLength = refLength + len(line) - 1
#      # If memFlag = 1, store in refString.  Otherwise, write to disk
#      if memFlag == 1:
#        refString = refString + line[:-1].upper()
#      else:
#        refTemp.write(line[:-1].upper())
#    else:
#      refLength = refLength + len(line)
#      if memFlag == 1:
#        refString = refString + line.upper()
#      else:
#        refTemp.write(line.upper())
#  inFile.close()
#  if memFlag == 0:
#    refTemp.close()
####

#***
#  # Open the target file
#  try:
#    inFile = open(targetFile)
#  except IOError:
#    print >> sys.stderr, "Target file " + targetFile + " not found!"
#    sys.exit()
#  if memFlag == 0:
#    targetTemp = open(tempTargetFile,"w")
#
#  # Get the header if it exists
#  targetString = ''
#  firstLine = inFile.readline()
#  firstLine = firstLine[:-1]
#
#  if isHeader(firstLine):
#    header = firstLine
#  else:
#    if memFlag == 1:
#      targetString = firstLine
#    else:
#      targetTemp.write(firstLine)
#
#  # Get the entire target sequence
#  while 1:
#    line = inFile.readline()
#    if not line:
#      break
#
#    # Append the new line to the string
#    if line[-1] == "\n":
#      # If memFlag = 1, store in targetString.  Otherwise, write to disk
#      if memFlag == 1:
#        targetString = targetString + line[:-1].upper()
#      else:
#        targetTemp.write(line[:-1].upper())
#    else:
#      if memFlag == 1:
#        targetString = targetString + line.upper()
#      else:
#        targetTemp.write(line.upper())
#  inFile.close()
#  if memFlag == 0:
#    targetTemp.close()
#
#  if memFlag == 0:
#    refTemp = open(tempRefFile, "r")
#    targetTemp = open(tempTargetFile, "r")
######

  refLength = SubseqPicker.getActualFileSize(refFile)

  #if(timing == 1):
  #  t1 = time()

  #if(timing == 1):
  #  print 'temping time taken = %f' %(t1-t0)

  #$$
  (Rfile, RheaderSize, Rlinelen, Rheader) = SubseqPicker.openAndPrepare(refFile)
  #$$
  (Tfile, TheaderSize, Tlinelen, Theader) = SubseqPicker.openAndPrepare(targetFile)

#  (Rfile2, RheaderSize, Rlinelen, Rheader) = SubseqPicker.openAndPrepare(refFile)
  #$$
#  (Tfile2, TheaderSize, Tlinelen, Theader) = SubseqPicker.openAndPrepare(targetFile)
  
                                ##################### End Reading Reference & Target Genomes each into one long string ########################

                                ##################### Traversing Reference & Target strings to find matches(instru.s) ########################
  #ts0 = time()

  #### Try finding the maximum target seq. that matches with the given subref. at the given window 
  
  # Array containing the last couple of chk's
  chk_array = []
  
  # Where in the reference to look
  refStart = 0
  actualStart = 0
  refStop = winLen

  # Where in the target to look
  targetStop = 0
            #************* Get Subref. *************#
  # Load the base pairs ## (limited to the determined window length) ## into the reference
  ## initially this subref. will be considered to find a matching with the target seq.
#***
#  if memFlag == 1:
#    myRef = refString[refStart:refStop]
#  else:
#    refTemp.seek(refStart)
#    myRef = refTemp.read(refStop-refStart)
####
  # $$  
  #t0 = time()
  myRef = SubseqPicker.PickSubseq(Rfile, refStart,refStop-refStart, RheaderSize, Rlinelen)
  #t1 = time()
  #print (t1-t0)
#  myRef2 = SubseqPicker.PickSubseq(Rfile2, refStart,refStop-refStart, RheaderSize, Rlinelen)
#  if myRef <> myRef2:
#      print refStop-refStart
  #print myRef2
  
            ############## End Get Subref. ##########

  # Initial target is empty
  ## Why?? empty --> to start getting the maximum match inside the given window of the subref.
  ## So, during the next loop iterations, the target subseq. will be appended with next target bases as
  ## long as the whole sub-target till now is matching the subref. 
  target = ''           ## the initial subtarget.
  targetBuffer = ''     ## buffer to get susequent target chars from - will be used to get chars to be appended to current subtarget
  
  # Cumulative length to keep track of where we are in the file
  cumulative_len = 0
  
  count = 1     ## Why?? 1
  done  = 0

            #************* starting loop of finding subsequent matches -- INSTRUCTIONS *************#

  # Keep going until we run out of the target
  #### parallel: dispatch different ref./target substrs to different cores, then reduce (collect) the length of the biggest matching 
  #### from the cores, then get this biggest match and start normally encoding it as usual.
  while(1):
    # Search for target in the file
    chk = myRef.find(target)
    # Not sure if this really is bad or not
    #if chk == -1:
    #  print "BAD"
  
            #************* incrementally find the (max matching subseq.)/instru. between ref./target *************#
            
    searchStep = 1
    # Keep going if we have a perfect match
    goodchk = 0
    while (chk != -1):
      # Get some more of each file
      ## get next ref. char(s) -- looking out of the current subref. window
#***
#      if memFlag == 1:
#        temp2 = refString[refStop:refStop+searchStep]
#      else:
#        refTemp.seek(refStop)
#        temp2 = refTemp.read(searchStep)
####
      # $$  
      temp2 = SubseqPicker.PickSubseq(Rfile, refStop, searchStep, RheaderSize, Rlinelen)
#      temp3 = SubseqPicker.PickSubseq(Rfile2, refStop, searchStep, RheaderSize, Rlinelen)
#      if temp2 <> temp3:
#        print searchStep

      ## increase window size -- extend subref.
      refStop = refStop + searchStep
  
      ## increasing subtarget with searchstep char(s)
      # How much we read from the file for the reference is based on how much we have in the buffer
      if (searchStep <= len(targetBuffer)):             ## append searchstep char(s) from buffer to subtarget, then decrease the buffer from the left
        temp = targetBuffer[:searchStep]
        targetBuffer = targetBuffer[searchStep:]
      elif (len(targetBuffer) > 0):                     ## get the remaining searchstep char(s) from buffer + next chars from maintarget chars
#***        
#        if memFlag == 1:
#          temp = targetBuffer + targetString[targetStop:targetStop + (searchStep-len(targetBuffer))]
#          targetStop = targetStop + (searchStep - len(targetBuffer))
#        else:
#          temp = targetBuffer + targetTemp.read(searchStep-len(targetBuffer))
####
        # $$  
        temp = targetBuffer + SubseqPicker.PickSubseq(Tfile, -1, searchStep-len(targetBuffer), TheaderSize, Tlinelen)
#        temp4 = targetBuffer + SubseqPicker.PickSubseq(Tfile2, -1, searchStep-len(targetBuffer), TheaderSize, Tlinelen)
#        if temp <> temp4:
#            print searchStep-len(targetBuffer)
        targetBuffer = ''
      else:
#***
#        if memFlag == 1:                                ## read all the searchstep char(s) from the maintarget stream
#          temp = targetString[targetStop:targetStop+searchStep] 
#          targetStop = targetStop + searchStep
#        else:
#          temp = targetBuffer + targetTemp.read(searchStep)
####
        # $$ 
        temp = targetBuffer + SubseqPicker.PickSubseq(Tfile, -1, searchStep, TheaderSize, Tlinelen)
#        temp5 = targetBuffer + SubseqPicker.PickSubseq(Tfile2, -1, searchStep, TheaderSize, Tlinelen)
#        if temp <> temp5:
#            print searchStep
  
      if not temp:  ## no more enough char(s) in the target seq.
        done = 1
        break
      else:
        ## updating the old target/ref. subseq. with the newly fetched char(s) 
        target = target + temp
        myRef  = myRef  + temp2
	## fix 5 for memory consumption
	temp = ''
	temp2 = ''
        
        ## checking whether the new target subseq is matching the new ref. subseq.
        if searchStep < 100000:     ## Why?? can any ref./target have a single match with > 100000 char?
          chk    = myRef.find(target)
          if chk != -1:
            goodchk = chk
        else:           ## Why?? !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          if target != myRef[chk:chk+len(target)]: ## chk is not set yet, as done by the above find method, this check's purpose was to avoid callign the find method, but it is not logical to be done that way
            goodchk = chk
            chk = -1
    
      # Try to speed up the longest string match process:
      # If we had a match, double the size of searchStep
      if chk != -1:
        searchStep = searchStep * 2             ## double next search steps: 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 ...
  
            ############## End incrementally find the max matching subseq. between ref./target ##########

    # There was no more target, so just break out of the loop
    if done == 1:
      break

            #************* decrementally decrease the failed extended-searchstep trying to find max possible matching subseq. between ref./target *************#
    
    # We have a mismatch, so back off until we find the longest match
    ## parallel:
    ## if last searchstep was 64, then go back checking with searchsteps: 
    ## 32+16, if failed, then 32+8, if failed, then 32+4, if failed, then 32+2, if failed, then 32+1
    ## 32+16, if failed, then 32+8, if failed, then 32+4, if succee, then 32+6, if failed, then 32+5
    increment = searchStep/2
    length = -increment
    while increment > 0:
      # Look for a match
      ## Why?? the first iteration is absolutely true/redundant because it checks the successfulness of the PAST successfull searchstep !!
      ## I think it is for easy programmability/coding
      if target[:length] != myRef[goodchk:goodchk+len(target[:length])]:
        chk = -1
      else:
        chk = goodchk
  
      # Update increment
      increment = increment / 2
  
      # If we had a match, then we need to move length to the right
      ## if 32+16 is ok, then try 32+16+8, and so on ...
      ## if 32+16 fails, then try 32+8
      ## review again !! 
      if (chk != -1):
        length = length + increment
      else:
        length = length - increment
  
            ############## End decrementally decrease the searchstep trying to find max possible matching subseq. between ref./target ##########


            #************* adjusting indeces and building the instruction data *************#

    # Final adjustment:
    # If the last one did not match, then we need to move the length to the left
    ## A FACT: the final successful searchstep was the perfect match, if the next char of ref./target doesn't match
    if (chk == -1):
      length = length - 1
      chk = goodchk
  
    # Get the length of the longest match
    target_len = len(target[:length])
  
    # Update where we are in the file
    prev_cum       = cumulative_len
    cumulative_len = cumulative_len + target_len + 1    ## Why?? +1 ?? Because each instru. holds one more ending char to be encoded 
  
    # Where in the reference the match occurred
    refMatch = refStart + chk
  
    ## getting the different char occuring after the matched searchstep
    oldChar = ""
    charPos = actualStart+chk+target_len
    if (charPos < refLength):
#      if memFlag == 1:
#        oldChar = refString[charPos]
#      else:
#        refTemp.seek(charPos)
#        oldChar = refTemp.read(1)
      # $$
      oldChar = SubseqPicker.PickSubseq(Rfile, charPos, 1, RheaderSize, Rlinelen)
#      someChar = SubseqPicker.PickSubseq(Rfile2, charPos, 1, RheaderSize, Rlinelen)
#      if oldChar <> someChar:
#        print '1'  
    else:
      oldChar = 'N'
  
    # Position is 1 based - CHANGE THIS LATER (After we're sure this program works)
    if memFlag == 1:
      myInstructions.append((actualStart+chk+1, target_len, target[length], oldChar))
      numInstructions = numInstructions + 1
    else:
      instructionTemp.write(str(actualStart+chk+1) + " " + str(target_len) + " " + str(target[length]) + " " + oldChar + "\n")
      numInstructions = numInstructions + 1
  
            ############## End adjusting indeces and building the instruction data ##########

            #************* adjusting subtarget - targetbuffer - and the last 100 match positions *************#

    # Update target
    # Note special case: if we matched everything up until the last character,
    # then length+1 will wrap around to the beginning of the string, which is bad
    ## Why?? --> retrieving the un-matched chars from the last failed searchstep matching, into the left of the target buffer again, 
    ##     before resetting the subtarget  
    if length < -1:
      targetBuffer = target[length+1:] + targetBuffer
    target = ''
  
    # Update the array of chk
    # This is the thing with the 100 last good matches
    ## adding the last match position into the array of the 100 most recent match positions
    if (target_len > goodThresh):
      if len(chk_array) < chk_size:
        chk_array = chk_array + [chk]
      else: 
        chk_array = chk_array[1:] + [chk]   ## NOT re-allocation to extend the full chk_array
        ## THIS IS FOR APPENDING THE START_POSITION OF THE NEW MATCH INTO THE ARRAY
        ## helps in finding the min/median of the RECENT match positions 
  
            ############## End adjusting subtarget - targetbuffer - and the last 100 match positions ##########

            #************* adjusting the ref. window *************#

    # Every 100 matches, see if we need to shift by an extra amount
    # We want to replace min with median, but maybe some other time
    ## AFTER 100 NEW MATCHES: re-adjusting the ref. window according to the min. found match of the last 100 matches  
    if (count%100 == 0):
      if len(chk_array) > 1:
        refStart += min(chk_array) - insSize
  
    # Always move by at least the length of the match
    ## AFTER EACH MATCH: usual adjust of window
    refStart += target_len
  
    # Update the reference window
    ## AVOID GETTING -VE START POSITION: determine the window start, then fetch the new subref.
    actualStart = max(0,refStart-insSize)
#***
#    if memFlag == 1:
#      myRef = refString[actualStart:actualStart+winLen]
#    else:
#      refTemp.seek(actualStart)
#      myRef = refTemp.read(winLen)
####
    # $$
    myRef = SubseqPicker.PickSubseq(Rfile, actualStart, winLen, RheaderSize, Rlinelen)
#    myRef2 = SubseqPicker.PickSubseq(Rfile2, actualStart, winLen, RheaderSize, Rlinelen)
#    if myRef <> myRef2:
#        print winLen
    ## determine the window end
    refStop = actualStart + winLen
  
                ############## End adjusting the ref. window ##########

    count += 1
            ############## End starting loop of finding subsequent matches -- INSTRUCTIONS ##############
                                ##################### End Traversing Reference & Target strings to find matches(instru.s) ########################            
  
  # Print the final match: the last character, N, is just a dummy bp
  ## Why?? dummy instruction?? kind of PADDING?
  actualStart = max(0,refStart-insSize)
  chk = myRef.find(target)
  length = len(target)
  if memFlag == 1:
    myInstructions.append((actualStart+chk+1, length, 'N', 'N'))
    numInstructions = numInstructions + 1
  else:
    instructionTemp.write(str(actualStart+chk+1) + " " + str(length) + " N N" + "\n")
    numInstructions = numInstructions + 1
    #refTemp.close()
    #targetTemp.close()
    instructionTemp.close()
    
  SubseqPicker.finalizeAndClose(Rfile)
  SubseqPicker.finalizeAndClose(Tfile)                                  

  #te0 = time()
  #print "all Hs = %f"%(te0-ts0)

  return (Theader, myInstructions, numInstructions)


############################################################################################################################
############################################################################################################################
############################################################################################################################

# This function takes as input a list of (position, length, new, old) tuples
# and splits them into a new list of these tuples and a set of substitutions
def splitSubs(myInstructions, memFlag, tempInstructionFile, numInstructions, tempSubFile):
  # Initialize some variables

            #************* loading the first instruction - position, length *************#
  
  numNewInstructions = 0
  numSubs = 0
  prevLine = ''
  currLine = ''
  if memFlag == 1:
    prevPos  =  myInstructions[0][0]
    prevLen  =  myInstructions[0][1]
  else:
    instructionTemp  = open(tempInstructionFile, 'r')
    instructionTemp2 = open(tempInstructionFile+"A", 'w')
    myLine  = instructionTemp.readline()
    vals    = myLine.split()
    prevPos = int(vals[0])
    prevLen = int(vals[1])
    subTemp = open(tempSubFile, 'w')

            ############## End loading the first instruction - position, length ##############

            #************* Trying to merge the current instruction with the next instructions *************#

  prevDelete = 0
  currDelete = 0
  currLength = 0

  ## start preparing the first new_instr[pos,.,.,.]
  newInstructions = []
  if memFlag == 1:
    newInstructions = [[prevPos]]
  else:
    instructionTemp2.write(str(prevPos) + " ")
  numNewInstructions = numNewInstructions + 1
  ## initiating the substtu. array
  newSubs = []
  cumLen  = prevLen             ##--------------------->>> this index is for keeping the current absolute position at the TARGET seq. (needed by substtu. entry)

  # Move through the rest of the instructions, figure out which lines will be combined
  for ind in xrange(1, numInstructions):
    ## reading the nxt_instr[pos,len,.,.], prv_instr[.,.,Tchar,Rchar]  
    if memFlag == 1:
      newPos = myInstructions[ind][0]
      newLen = myInstructions[ind][1]
      myChars =  [myInstructions[ind-1][2], myInstructions[ind-1][3]]
    else:
      myChars = [vals[2], vals[3]]
      myLine = instructionTemp.readline()
      vals = myLine.split()
      newPos = int(vals[0])
      newLen = int(vals[1])

    # This instruction can be replaced by a substitution, so we update the length for the new instruction
    ## see building substtu. in PAPER page 3.right.top
    ## check whether this is a substtu.,  
    if (prevPos + prevLen + 1) == newPos:
      currDelete = 1                            ## the current instr. will be deleted.,
      if (prevDelete == 1):
        currLength = currLength + prevLen + 1   ## its data will be merged with the prev. old instr.(s) which involved substtu.s
      else:
        currLength = prevLen + 1                ## resetting the currLength (cummulative length) bcz this instru is the 1st involved substtu. in this new_instr.                

      ## add the new substtu. entry
      numSubs = numSubs + 1
      if memFlag == 1:
        newSubs.append([cumLen + 1] + myChars)
      else:
        subTemp.write(str(cumLen+1) + " " + myChars[0] + " " + myChars[1] + "\n")
    
    # Current line/instru. cannot be replaced by a substitution, so we finish the
    # previous new instruction and start a new one
    else:
      currDelete = 0                            ## don't delete the current instr., because no substtu. is found at the current instr.
      ## write the current new_instr. (resulted from merging 2 old instr. and deducing a substtu.), and open a new instr. for possible next substtu./mergings-of-old-instr.s 
      # Finish the entry of the previous new instruction
      if (prevDelete == 0):         ## write the only prev. old instr. as a new instr. 
        if memFlag == 1:
          newInstructions[-1] = newInstructions[-1] + [prevLen] + myChars
        else:
          instructionTemp2.write(str(prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")
      else:             ## write all (prev) instr.s resulted in different substtu.s -- into the new instr.
        if memFlag == 1:
          newInstructions[-1] = newInstructions[-1] + [currLength + prevLen] + myChars
        else:
          instructionTemp2.write(str(currLength + prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")

      # Start a new entry ## a new instr. with the pos of the current old instr.
      if memFlag == 1:
        newInstructions.append([newPos])
      else:
        instructionTemp2.write(str(newPos) + " ")
      numNewInstructions = numNewInstructions + 1


    ## update temp variables/indeces
    cumLen = cumLen + newLen + 1

    prevPos = newPos
    prevLen = newLen
    prevDelete = currDelete

                    #********* finish the last entry of the last iteration of the for loop ***********#
                    
  # Finish the entry of the previous ## LAST ## new instruction and substitution
  if memFlag == 1:
    myChars =  [myInstructions[-1][2], myInstructions[-1][3]]
  else:
    myChars = [vals[2], vals[3]]
    instructionTemp.close()

  if (prevDelete == 0):
    if memFlag == 1:
      newInstructions[-1] = newInstructions[-1] + [prevLen] + myChars
    else:
      instructionTemp2.write(str(prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")
  else:
    if memFlag == 1:
      newInstructions[-1] = newInstructions[-1] + [currLength + prevLen] + myChars
    else:
      instructionTemp2.write(str(currLength + prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")

  if prevDelete == 1:
    numSubs = numSubs + 1
    if memFlag == 1:
      newSubs.append([cumLen + 1] + myChars)
    else:
      subTemp.write(str(cumLen+1) + " " + myChars[0] + " " + myChars[1] + "\n")

            ############## End Trying to merge the current instruction with the next instructions ##############

  # Overwrite the instruction file ## with the new file of merged instructions
  if memFlag == 0:
    instructionTemp2.close()
    os.rename(tempInstructionFile+"A", tempInstructionFile)
    subTemp.close()

  return (newInstructions, newSubs, numNewInstructions, numSubs)

############################################################################################################################
############################################################################################################################
############################################################################################################################

# This function takes as input a list of (position, length, new, old) tuples
# and splits them into a new list of these tuples and a set of length 1 insertions
def splitIns(myInstructions, memFlag, tempInstructionFile, numInstructions, tempInsFile):
  numNewInstructions = 0
  numIns = 0
  # Initialize some variables

            #************* loading the first instruction - position, length *************#
  
  if memFlag == 1:
    prevPos    =  myInstructions[0][0]
    prevLen    =  myInstructions[0][1]
  else:
    instructionTemp = open(tempInstructionFile, 'r')
    instructionTemp2 = open(tempInstructionFile+"A", 'w')
    myLine = instructionTemp.readline()
    vals = myLine.split()
    prevPos = int(vals[0])
    prevLen = int(vals[1])
    insTemp = open(tempInsFile, 'w')

            ############## End loading the first instruction - position, length ##############

          #************* Trying to merge the current instruction with the next instructions *************#

  prevDelete = 0
  currDelete = 0
  currLength = 0

  ## start preparing the first new_instr[pos,.,.,.]
  newInstructions = []
  if memFlag == 1:
    newInstructions = [[prevPos]]
  else:
    instructionTemp2.write(str(prevPos) + " ")
  numNewInstructions = numNewInstructions + 1
  ## initiating the inss. array
  newIns  = []
  cumLen  = prevLen             ##--------------------->>> this index is for keeping the current absolute position at the TARGET seq. (needed by ins. entry)

  # Move through the rest of the instructions, figure out which lines will be
  # combined
  for ind in xrange(1, numInstructions):
    ## reading the nxt_instr[pos,len,.,.], prv_instr[.,.,Tchar,Rchar]
    if memFlag == 1:
      newPos = myInstructions[ind][0]
      newLen = myInstructions[ind][1]
      myChars =  [myInstructions[ind-1][2], myInstructions[ind-1][3]]
    else:
      myChars = [vals[2], vals[3]]
      myLine  = instructionTemp.readline()
      vals    = myLine.split()
      newPos  = int(vals[0])
      newLen  = int(vals[1])

    # This instruction can be replaced by an insertion, so we update the
    # length for the new instruction
    # We only replace lines which do not have 0 for a length    ## Why?? is this possible?
    if ((prevPos + prevLen) == newPos) and (newLen != 0):
      currDelete = 1
      if (prevDelete == 1):
        currLength = currLength + prevLen
      else:
        currLength = prevLen

      numIns = numIns + 1;
      if memFlag == 1:
        newIns.append([cumLen + 1] + myChars)
      else:
        insTemp.write(str(cumLen+1) + " " + myChars[0] + " " + myChars[1] + "\n")
    
    # Current line cannot be replaced by an insertion, so we finish the
    # previous new instruction and start a new one
    else:
      currDelete = 0

      # Finish the entry of the previous new instruction
      if (prevDelete == 0):
        if memFlag == 1:
          newInstructions[-1] = newInstructions[-1] + [prevLen] + myChars
        else:
          instructionTemp2.write(str(prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")
      else:
        if memFlag == 1:
          newInstructions[-1] = newInstructions[-1] + [currLength + prevLen] + myChars
        else:
          instructionTemp2.write(str(currLength + prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")

      # Start a new entry
      if memFlag == 1:
        newInstructions.append([newPos])
      else:
        instructionTemp2.write(str(newPos) + " ")
      numNewInstructions = numNewInstructions + 1

    cumLen = cumLen + newLen + 1

    prevPos = newPos
    prevLen = newLen
    prevDelete = currDelete
            
  # Finish the entry of the previous new instruction and insertion
  if memFlag == 1:
    myChars =  [myInstructions[-1][2], myInstructions[-1][3]]
  else:
    myChars =  [vals[2], vals[3]]
    instructionTemp.close()

  if (prevDelete == 0):
    if memFlag == 1:
      newInstructions[-1] = newInstructions[-1] + [prevLen] + myChars
    else:
      instructionTemp2.write(str(prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")
  else:
    if memFlag == 1:
      newInstructions[-1] = newInstructions[-1] + [currLength + prevLen] + myChars
    else:
      instructionTemp2.write(str(currLength + prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")

  if prevDelete == 1:
    # Skip this insertion if it's the dummy insertion
    if (myChars[0] != "N") or (myChars[1] != "N"):
      numIns = numIns + 1
      if memFlag == 1:
        newIns.append([cumLen + 1, myChars[0], myChars[1]])
      else:
        insTemp.write(str(cumLen+1) + " " + myChars[0] + " " + myChars[1] + "\n")

            ############## End Trying to merge the current instruction with the next instructions ##############

  # Overwrite the instruction file
  if memFlag == 0:
    instructionTemp2.close()
    os.rename(tempInstructionFile+"A", tempInstructionFile)
    insTemp.close()
    
  return (newInstructions, newIns, numNewInstructions, numIns)

############################################################################################################################
############################################################################################################################
############################################################################################################################

# This function takes as input a list of (position, length, new, old) tuples
# and splits them into a new list of these tuples and a set of deletions (with
# length <= 1000)
def splitDel(myInstructions, refFile, memFlag, tempRefFile, tempInstructionFile, numInstructions, tempDelFile):
  # Initialize some variables

            #************* loading the first instruction - position, length *************#

  numNewInstructions = 0
  numDels = 0
  if memFlag == 1:
    prevPos    =  myInstructions[0][0]
    prevLen    =  myInstructions[0][1]
  else:
    instructionTemp  = open(tempInstructionFile, 'r')
    instructionTemp2 = open(tempInstructionFile+"A", 'w')
    myLine = instructionTemp.readline()
    vals = myLine.split()
    prevPos = int(vals[0])
    prevLen = int(vals[1])
    delTemp = open(tempDelFile, 'w')

            ############## End loading the first instruction - position, length ##############

          #************* Trying to merge the current instruction with the next instructions *************#

  prevDelete = 0
  currDelete = 0
  currLength = 0

  delLen  = 0
  delPos  = 0
  tempLen = 0

  ## start preparing the first new_instr[pos,.,.,.]
  newInstructions = []
  if memFlag == 1:
    newInstructions = [[prevPos]]
  else:
    instructionTemp2.write(str(prevPos) + " ")
  numNewInstructions = numNewInstructions + 1
  ## initiating the dels. array
  newDel  = []
  cumLen  = prevLen             ##--------------------->>> this index is for keeping the current absolute position at the TARGET seq.

        #***************************** new part - reading ref again !! *************************#

#***
#  if memFlag == 1:
#    # Read in the reference
#    inFile = open(refFile)
#  
#    # Get the header if it exists
#    refString = ''
#    firstLine = inFile.readline()
#    firstLine = firstLine[:-1]
#  
#    if not isHeader(firstLine):
#      refString = firstLine
#  
#    # Get the entire reference sequence
#    while 1:
#      line = inFile.readline()
#      if not line:
#        break
#  
#      # Append the new line to the string
#      if line[-1] == "\n":
#        refString = refString + line[:-1].upper()
#      else:
#        refString = refString + line.upper()
#    inFile.close()
#  else:
#    refTemp = open(tempRefFile, "r")
####
  # $$
  (Rfile, RheaderSize, Rlinelen,Rheader) = SubseqPicker.openAndPrepare(refFile)
        ########################## End reading ref again !! ################################
        ########################## End reading ref again !! ################################

  # Move through the rest of the instructions, figure out which lines will be
  # combined
  for ind in xrange(1, numInstructions):
    ## reading the nxt_instr[pos,len,.,.], prv_instr[.,.,Tchar,Rchar]
    if memFlag == 1:
      newPos = myInstructions[ind][0]
      newLen = myInstructions[ind][1]
      prevChar = myInstructions[ind-1][2]                               ## prev target char of the prev instru.
      myChars  = [myInstructions[ind-1][2], myInstructions[ind-1][3]]
    else:
      prevChar = vals[2]
      myChars  = [vals[2], vals[3]]
      myLine   = instructionTemp.readline()
      vals     = myLine.split()
      newPos   = int(vals[0])
      newLen   = int(vals[1])

    refChar = ""
    if newPos-2 >= 0:
#***
#      if memFlag == 1:
#        refChar = refString[newPos - 2]
#      else:
#        refTemp.seek(newPos-2)
#        refChar = refTemp.read(1)
####
      # $$
      refChar = SubseqPicker.PickSubseq(Rfile, newPos-2, 1, RheaderSize, Rlinelen)  ## Why?? ------------->>>> ???
      
    # This instruction can be replaced by a deletion, so we update the
    # length for the new instruction
    if (((prevPos + prevLen + 2) <= newPos) and  
        (refChar == prevChar) and                       ## Why?? ------------->>>> ??? assertion of prev. instru. end !!!, but why (NEWPOS-2) b4 5 lines?? ---> all dels will be 2
        (newPos - 1 - prevPos - prevLen) < 1000):       ## ------------------------>>> length of max. allowed del. per instru.
      currDelete = 1
      if (prevDelete == 0):
        currLength = prevPos
      delPos    = tempLen + prevLen + 1
      delLength = newPos - 1 - prevPos - prevLen

      numDels = numDels + 1
      if memFlag == 1:
        newDel.append([delPos, delLength])
      else:
        delTemp.write(str(delPos) + " " + str(delLength) + "\n")

      tempLen = tempLen + newPos - prevPos
    
    # Current line cannot be replaced by a deletion, so we finish the
    # previous new instruction and start a new one
    else:
      currDelete = 0

      # Finish the entry of the previous new instruction
      if (prevDelete == 0):
        if memFlag == 1:
          newInstructions[-1] = newInstructions[-1] + [prevLen] + myChars
        else:
          instructionTemp2.write(str(prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")
      else:
        if memFlag == 1:
          newInstructions[-1] = newInstructions[-1] + [prevLen + prevPos - currLength] + myChars
        else:
          instructionTemp2.write(str(prevLen + prevPos - currLength) + " " + myChars[0] + " " + myChars[1] + "\n")

      # Start a new entry
      if memFlag == 1:
        newInstructions.append([newPos])
      else:
        instructionTemp2.write(str(newPos) + " ")
      numNewInstructions = numNewInstructions + 1

      tempLen = tempLen + prevLen + 1

    cumLen = cumLen + newLen + 1

    prevPos = newPos
    prevLen = newLen
    prevDelete = currDelete

  # Finish the entry of the previous new instruction ##(deletion is finished above as it depends only on position/length)##
  if memFlag == 1:
    myChars =  [myInstructions[-1][2], myInstructions[-1][3]]
  else:
    myChars = [vals[2], vals[3]]
    instructionTemp.close()

  if (prevDelete == 0):
    if memFlag == 1:
      newInstructions[-1] = newInstructions[-1] + [prevLen] + myChars
    else:
      instructionTemp2.write(str(prevLen) + " " + myChars[0] + " " + myChars[1] + "\n")
  else:
    if memFlag == 1:
      newInstructions[-1] = newInstructions[-1] + [prevLen + prevPos - currLength] + myChars
    else:
      instructionTemp2.write(str(prevLen + prevPos - currLength) + " " + myChars[0] + " " + myChars[1] + "\n")

            ############## End Trying to merge the current instruction with the next instructions ##############

  # Overwrite the instruction file
  if memFlag == 0:
    instructionTemp2.close()
    os.rename(tempInstructionFile+"A", tempInstructionFile)
    delTemp.close()
  SubseqPicker.finalizeAndClose(Rfile)
  return (newInstructions, newDel, numNewInstructions, numDels)

############################################################################################################################

# This function reads from a bit file and gets all the instructions,
# substitions, insertions, and deletions
def getLists(f, huffTable):
  temp = ''
  
  # The first codeword tells us the number of base pairs per line
  (basePairsPerLine, temp) = huff.getKey(f, huffTable, temp)

  # Get second codeword: This tells us the number of files
  (numFiles, temp) = huff.getKey(f, huffTable, temp)
  
  totalElements = [0]*numFiles
  instructions  = [0]*numFiles
  substitutions = [0]*numFiles
  insertions    = [0]*numFiles
  deletions     = [0]*numFiles
  # Get the number of instructions, substitutions, insertions, and deletions
  for ind in xrange(numFiles):
    (numInstructions,  temp) = huff.getKey(f, huffTable, temp)
    (numSubstitutions, temp) = huff.getKey(f, huffTable, temp)
    (numInsertions,    temp) = huff.getKey(f, huffTable, temp)
    (numDeletions,     temp) = huff.getKey(f, huffTable, temp)
  
    totalElements[ind] = [numInstructions, numSubstitutions, numInsertions, numDeletions]
  
  # Keep reading in integers
  for ind in xrange(numFiles):
    #############################################################
    # Get the instructions
    # Get first position and length
    (position, temp)  = huff.getKey(f, huffTable, temp)
    (length, temp)    = huff.getKey(f, huffTable, temp)
    instructions[ind] = [[position, length]]
  
    #Get the rest of the instructions
    for ind2 in xrange(1,totalElements[ind][0]):
      (position, temp) = huff.getKey(f, huffTable, temp)
      (length, temp)   = huff.getKey(f, huffTable, temp)
      instructions[ind].append([position, length])
  
    #############################################################
    # Get the substitutions
    if totalElements[ind][1] > 0:
      # Get first position
      (position, temp) = huff.getKey(f, huffTable, temp)
      substitutions[ind] = [[position]]
      prevPos = position

      #Get the rest of the subsitutions
      for ind2 in xrange(1,totalElements[ind][1]):
        (currWord, temp) = huff.getCodeword(f, huffTable, temp)
        position = prevPos + huffTable[currWord]
        prevPos  = position
        substitutions[ind].append([position])
    else:
      substitutions[ind] = []
  
    #############################################################
    # Get the insertions
    if totalElements[ind][2] > 0:
      # Get first position
      (currWord, temp) = huff.getCodeword(f, huffTable, temp)
      position = huffTable[currWord]
      insertions[ind] = [[position]]
      prevPos = position
    
      #Get the rest of the insertions
      for ind2 in xrange(1,totalElements[ind][2]):
        (currWord, temp) = huff.getCodeword(f, huffTable, temp)
        position = prevPos + huffTable[currWord]
        prevPos  = position
        insertions[ind].append([position])
    else:
      insertions[ind] = []
  
    #############################################################
    # Get the deletions
    if totalElements[ind][3] > 0:
      # Get first position and length
      (position, temp) = huff.getKey(f, huffTable, temp)
      (length, temp)   = huff.getKey(f, huffTable, temp)
      deletions[ind] = [[position, length]]
      prevPos = position
    
      #Get the rest of the insertions
      for ind2 in xrange(1,totalElements[ind][3]):
        (currWord, temp) = huff.getCodeword(f, huffTable, temp)
        position = prevPos + huffTable[currWord]
        prevPos  = position
        (length, temp) = huff.getKey(f, huffTable, temp)
        deletions[ind].append([position, length])
    else:
      deletions[ind] = []

  # Now we need to get the sign bits to calculate the actual positions for the instructions
  for ind in xrange(numFiles):
    prevInt = 0
    for ind2 in xrange(totalElements[ind][0]):
      (sign, temp) = bits.getBits(f, 1, temp)
      if sign == '0':
        instructions[ind][ind2][0] = prevInt + instructions[ind][ind2][0]
      else:
        instructions[ind][ind2][0] = prevInt - instructions[ind][ind2][0]
      prevInt = instructions[ind][ind2][0] + instructions[ind][ind2][1]

  return (basePairsPerLine, numFiles, instructions, substitutions, insertions, deletions)

############################################################################################################################

# This function takes as input a reference file and a list of instructions,
# substitutions, insertions, deletions, and characters.  It makes a target
# string based on the reference and the lists.
def getChromosome(refFile, instructionList, subList, insList, delList, f, temp, memFlag, tempRefFile, tempTargetFile):
    ## refFile           filename for refFile 
    ## f                 characterFileMap
    ## tempRefFile       filename for temp RefFile
    ## tempTargetFile    filename for temp TargetFile 
                        #************* start reading reference as a single non-lined stream ******************#
#***
#  # Open the reference file
#  try:
#    inFile = open(refFile)
#  except IOError:
#    print >> sys.stderr, "Reference file " + refFile + " not found!"
#    sys.exit()
#
#  # Open the reference for writing
#  if memFlag == 0:
#    refTemp = open(tempRefFile, "w")
#
#  # Length of reference
#  refLength = 0
#
#  # Skip the header if it exists
#  refString = ''
#  firstLine = inFile.readline()
#  firstLine = firstLine[:-1]
#
#  if not isHeader(firstLine):
#    refLength = refLength + len(firstLine)
#    if memFlag == 1:
#      refString = firstLine  
#    else:
#      refTemp.write(firstLine)
#
#  # Get the entire reference sequence
#  while 1:
#    line = inFile.readline()
#    if not line:
#      break
#
#    # Append the new line to the string
#    if line[-1] == "\n":
#      refLength = refLength + len(line) - 1
#      # If memFlag = 1, store in refString.  Otherwise, write to disk
#      if memFlag == 1:
#        refString = refString + line[:-1].upper()
#      else:
#        refTemp.write(line[:-1].upper())
#    else:
#      refLength = refLength + len(line)
#      if memFlag == 1:
#        refString = refString + line.upper()
#      else:
#        refTemp.write(line.upper())
#  inFile.close()
#
#  if memFlag == 0:
#    refTemp.close()
#    refTemp = open(tempRefFile, "r")
####
  refLength = SubseqPicker.getActualFileSize(refFile)
  (Rfile, RheaderSize, Rlinelen,Rheader) = SubseqPicker.openAndPrepare(refFile)
                        
                        ############ End reading reference as a single non-lined stream #######################

                        #********* Start generating the target seq. from the ref. seq. **************************#
  if memFlag == 0:
    targetTemp = open(tempTargetFile, "w")

  targetString = ''

  # Length of target after all the instructions
  tempTargetLength = 0

  # First is follow all the instructions
  ## Building initial target seq. from the ref. seq. - by applying all instructions - copying compressed matched subseq.s from the ref.
######## inCompressi: will need to copy from ref. only the subseq.s related to the instru. which its interval contains part/all of the subseq.  
  bitsRead = 0
  for ind in xrange(len(instructionList)):
    start  = instructionList[ind][0]-1 # Because start is 1-based
    length = instructionList[ind][1]
    stop   = start + length
    tempTargetLength = tempTargetLength + length
#***    
#    if memFlag == 1:
#      targetString = targetString + refString[start:stop]
#    else:
#      refTemp.seek(start)
#      targetTemp.write(refTemp.read(stop-start))

    ## reading the subref referred to by the current instruction's position->length 
    # $$
    subRef = SubseqPicker.PickSubseq(Rfile, start, stop-start, RheaderSize, Rlinelen)

    if memFlag == 1:
      targetString = targetString + subRef
    else:
      targetTemp.write(subRef)
      ## fix 3 for memory consumption  
      subRef = ''  
####

    # Skip the last instruction character
    ## if the current instru. is the last one, no need to read its associated char.
    
    if ind < len(instructionList)-1:
      tempTargetLength = tempTargetLength + 1

    ###if not (newChar == 'N' and oldChar == 'N'):

      if stop == refLength:
        refChar = 'N'
        #newChar = ''
      else:
#***          
#        if memFlag == 1:
#          (newChar, temp) = chromeMap.getNewChar(f, refString[stop], temp)
#        else:
#          (newChar, temp) = chromeMap.getNewChar(f, refTemp.read(1), temp)
####
         # $$
        refChar = SubseqPicker.PickSubseq(Rfile, -1, 1, RheaderSize, Rlinelen)
        (newChar, temp) = chromeMap.getNewChar(f, refChar, temp)   
    else:  
      (newChar, temp) = chromeMap.getNewChar(f, 'N', temp)   

    if memFlag == 1:
      targetString = targetString + newChar
    else:
      targetTemp.write(newChar)

    #print 'H ', newChar, '-', refChar, '-', temp

  if memFlag == 1:
    # Turn target into a list for easier manipulation
    targetString = list(targetString)
  else:
    ##refTemp.close()
    targetTemp.close()
  SubseqPicker.finalizeAndClose(Rfile)  

                        ########### End generating the target seq. from the ref. seq. ################

                        #********* Start applying del.s on the target seq. **************************#

  # Now do all the deletions
  if (len(delList) > 0) and (memFlag == 0):
    targetTemp = open(tempTargetFile, "r")
    targetTemp2 = open(tempTargetFile+"A", "w")

  currPointer = 0
  offset = 0
  newTempTargetLength = 0
  for ind in xrange(len(delList)):
    if memFlag == 1:
      # Because we're 1-based, and deleting base pairs will change the locations
      ## del.s need to be applied/reverted from end-to-start(when last del. applied first, it will not affect the pos.s of the prev. del.s), 
      # because its pos. is absolute to the original ref. seq.
      ## but in case we need to apply it from start-to-end (apply del.s from start to end)
      ## , we need to keep count of deleted chars till now in order to correct the absolute pos. of the next del.s
      start  = delList[ind][0] - offset - 1     ## consider how many char.s have been deleted by prev. del.s, bcz this will affect position of next del.s
      length = delList[ind][1]
      stop   = start + length
      del(targetString[start:stop])             ## delete this ref. subseq. from the immature target seq.
      offset = offset + length
    else:                                       
      ## skip the char.s of the prev. del. - don't write them into the new target file  
      targetTemp.seek(currPointer)               
      ## read/write the char(s) between the prev. del.-end and the current del.-pos
      targetTemp2.write(targetTemp.read(delList[ind][0]-currPointer-1))             
      ## update the total deleted chars till now
      newTempTargetLength = newTempTargetLength + (delList[ind][0]-currPointer-1)   
      ## point to the next char(s) NOT to be deleted - just jump this del. - add its position+length to the SEEKER
      currPointer = delList[ind][0] + delList[ind][1] - 1                           

  # Finish the deletions file
  ## read/write the remaining chars after the last del.
  if (memFlag == 0) and (len(delList) > 0):
    targetTemp.seek(currPointer)
    targetTemp2.write(targetTemp.read(tempTargetLength-currPointer))
    newTempTargetLength = newTempTargetLength + (tempTargetLength-currPointer)
    targetTemp.close()
    targetTemp2.close()
    os.rename(tempTargetFile+"A", tempTargetFile)
    tempTargetLength = newTempTargetLength

                        ########## End applying del.s on the target seq. #############################
#  start00=time()  

  #targetString = "".join(targetString)
                        #********* Start applying ins.s on the target seq. **************************#

  # Now do all the insertions
  if (len(insList) > 0) and (memFlag == 0):
    targetTemp = open(tempTargetFile, "r")
    targetTemp2 = open(tempTargetFile+"A", "w")

#  if memFlag == 1:
#      newTargetString = []
  currPointer = 0
#  index = 0
  #print len(insList)
  for ind in xrange(len(insList)):
    if memFlag == 1:
      position = insList[ind][0] - 1 # Because we're 1-based
#      newTargetString += targetString[currPointer:insList[ind][0]-currPointer-1]
#      oldChar = targetString[insList[ind][0]-currPointer-1]
      ## if ins. pos. occur at the end of the current target seq., just append it. 
      ## get the ins. char, then insert it into the target seq.  
      #print targetString[position]
      oldChar = targetString[position]
      (newChar, temp) = chromeMap.getNewChar(f, oldChar, temp)
#      newTargetString = newTargetString + [newChar] + [oldChar]
#      currPointer = insList[ind][0]+1 
        #print newChar, '-', temp
      targetString.insert(position, newChar)
        #targetString = targetString[:position] + [newChar] + targetString[position:]
    else:
      ## read/write  all the char.s before this ins.  
      targetTemp2.write(targetTemp.read(insList[ind][0]-currPointer-1))
      ## read the ref. char from the current immature target seq. which is supposed to be included by the ins. entry 
      oldChar = targetTemp.read(1)
      if oldChar == "":
        oldChar = 'N'
      ## get the original target char. which was encoded with the ref. char inside this ins. entry  
      (newChar, temp) = chromeMap.getNewChar(f, oldChar, temp)
      #print oldChar
      ## write both chars into the new target seq.
      targetTemp2.write(newChar+oldChar)
      # Add one because inserting a character has changed our positions ## the absolute position of the next ins.s
      currPointer = insList[ind][0]+1 

    #print 'I ', newChar, '-', oldChar, '-', temp 

  # Finish the insertions file
  if (memFlag == 0) and (len(insList) > 0):
    ## read/write the remaining chars after the last ins.  
    targetTemp2.write(targetTemp.read(tempTargetLength+(len(insList))-currPointer))
    targetTemp.close()
    targetTemp2.close()
    os.rename(tempTargetFile+"A", tempTargetFile)
    tempTargetLength = tempTargetLength + len(insList)      ## update the length of the current target seq. with the num. of ins.s (inserted chars)
#  elif memFlag == 1:
#    #targetString = []  
#    targetString = newTargetString
#    targetString = list(targetString)    

                        ########## End applying ins.s on the target seq. #############################
                        

#  end00=time()
#  print 'chromo %d : %f msec\n' % (0, ((end00-start00)*1000))
                        #********* Start applying substtu.s on the target seq. **************************#

  ## applying substtu.s from start to end or vice versa is the same, bcz no change will be done on the seq., and so, the length will be the same 
  # Now do all the substitutions
  if (len(subList) > 0) and (memFlag == 0):
    targetTemp = open(tempTargetFile, "r")
    targetTemp2 = open(tempTargetFile+"A", "w")

  currPointer = 0
  for ind in xrange(len(subList)):
    if memFlag == 1:
      position = subList[ind][0] - 1 # Because we're 1-based
      if position < len(targetString):
        oldChar = targetString[position]  
        (newChar, temp) = chromeMap.getNewChar(f, targetString[position], temp)
        targetString[position] = newChar
    else:
      ## read/write all the seq. chars till before this substtu.   
      targetTemp2.write(targetTemp.read(subList[ind][0]-currPointer-1))
      ## read the old ref. char to be subsitututed
      oldChar = targetTemp.read(1)
      if len(oldChar) <> 1:
        oldChar = 'N'  
      ## get/decode the original target char, using the ref. char  
      (newChar, temp) = chromeMap.getNewChar(f, oldChar, temp)
      ## write the target char.
      if not (oldChar == 'N' and newChar == 'N'):
        targetTemp2.write(newChar)            
      currPointer = subList[ind][0] 

    #print 'S ', newChar, '-', oldChar, '-', temp

  # Finish the substitutions file
  if (memFlag == 0) and (len(subList) > 0):
    ## read/write all the remaining chars after the last substtu.  
    targetTemp2.write(targetTemp.read(tempTargetLength-currPointer))
    targetTemp.close()
    targetTemp2.close()
    os.rename(tempTargetFile+"A", tempTargetFile)

                        ########## End applying substtu.s on the target seq. #############################

  if memFlag == 1:
    # Change back to string
    targetString = "".join(targetString)

  return (targetString, tempTargetLength, temp)

############################################################################################################################

