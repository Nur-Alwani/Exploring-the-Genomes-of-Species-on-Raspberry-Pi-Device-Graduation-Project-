#!/usr/bin/python
import sys
#sys.path.append('lib/')
import os
#import loc
#import bits
import huff
import lzmatch
import chromeMap
import SubseqPicker
#from time import time
#from twisted.python.util import println
import resource
#from array import array

timing = 1

############################################################################################################################

def loadEncodedLists(outHead):
  
  codebookFilename  = outHead+'codebook.ido'
  integerFilename   = outHead+'data.ido'
      
  # Read in the codebook
  f = open(codebookFilename, 'rb')
  huffTable = huff.readGolombCodedHuffTable(f)
  f.close()

  # Start reading in the integers 
  ## representing integers Instru.s, substtu.s, ins.s, del.s previously encoded FOR ALL CHROMOSOMES
  f = open(integerFilename,'rb')
  (basePairsPerLine, numFiles, instructionList, subList, insList, delList) = lzmatch.getLists(f, huffTable)
  f.close()
  return (basePairsPerLine, numFiles, instructionList, subList, insList, delList)

############################################################################################################################

def loadEncodedChars(outHead, instructionList, subList, insList, delList, whichChromosome):
    
  characterFilename = outHead+'char.ido'

  ## loading all the previously encoded/compressed chars from the chars file
  f = open(characterFilename, 'rb')
  temp = ''
  
  (instruChars, insChars, substtuChars) = loadEncodedCharsOfThisChromosome(f, instructionList, insList, subList, whichChromosome)
  f.close()
  
  return (instruChars, insChars, substtuChars)

############################################################################################################################

def manipulateSingleChromosome(refFile, whichChromosome, subseqStart, subseqLength, outHead, targetFile, BlockSize,
                                 basePairsPerLine, numFiles, instructionList, subList, insList, delList):

#  start00=time()  
  ## load the compressed data    
#  end00=time()
#  print 'chromo %d : %f msec\n' % (0, ((end00-start00)*1000))

  (instruChars, insChars, substtuChars) = loadEncodedChars(outHead, instructionList, subList, insList, delList, whichChromosome)

  ## check the total target length
  targetLength = getTotalChromosomeLength(refFile, whichChromosome, basePairsPerLine, numFiles, instructionList, subList, insList, delList)
  
  ## get all the chromosome
  if subseqLength == 0:
#    (extractedSeq, hitsCount, basePairsPerLine) = extractSubseq(refFile, whichChromosome, 0, targetLength,
#                                                                        basePairsPerLine, numFiles, instructionList, subList, insList, delList,
#                                                                        instruChars, insChars, substtuChars)
    (extractedSeq, hitsCount, basePairsPerLine) = extractSubseqInBlocks(refFile, whichChromosome, 0, targetLength, BlockSize,
                                                                        basePairsPerLine, numFiles, instructionList, subList, insList, delList,
                                                                        instruChars, insChars, substtuChars)

    saveChromosomeIntoFile(outHead, targetFile, basePairsPerLine, whichChromosome, extractedSeq, targetLength)  
  ## perform partial hits till all the requested subseq. length is obtained ...
  else:
    if subseqStart + subseqLength > targetLength:    
      subseqLength = targetLength - subseqStart      
#    (extractedSeq, hitsCount, basePairsPerLine) = extractSubseq(refFile, whichChromosome, subseqStart, subseqLength,
#                                                                        basePairsPerLine, numFiles, instructionList, subList, insList, delList,
#                                                                        instruChars, insChars, substtuChars)
    (extractedSeq, hitsCount, basePairsPerLine) = extractSubseqInBlocks(refFile, whichChromosome, subseqStart, subseqLength, BlockSize,
                                                                        basePairsPerLine, numFiles, instructionList, subList, insList, delList,
                                                                        instruChars, insChars, substtuChars)
                                                                        
  return (extractedSeq, hitsCount, targetLength)

############################################################################################################################

def searchSingleChromosome(refFile, whichChromosome, subseqStart, subseqLength, outHead, BlockSize, seq2search4, searchIndcs,
                                                     basePairsPerLine, numFiles, instructionList, subList, insList, delList):

  (instruChars, insChars, substtuChars) = loadEncodedChars(outHead, instructionList, subList, insList, delList, whichChromosome)

  ## check the total target length
  targetLength = getTotalChromosomeLength(refFile, whichChromosome, basePairsPerLine, numFiles, instructionList, subList, insList, delList)
  ## search all the chromosome
  if subseqLength == 0:
    subseqLength = targetLength  
  elif subseqStart + subseqLength > targetLength:    
    subseqLength = targetLength - subseqStart      

  (seqIndcs, hitsCount) = searchSeqsInBlocks(refFile, whichChromosome, subseqStart, subseqLength, BlockSize, seq2search4, searchIndcs,
                                                                        basePairsPerLine, numFiles, instructionList, subList, insList, delList,
                                                                        instruChars, insChars, substtuChars)
  return (seqIndcs, hitsCount)
  
############################################################################################################################

## skipping chars of prev. chromosome instru.s/ins.s/del.s, then loading the char.s of current chromosome instru.s/ins.s/del.s
def loadEncodedCharsOfThisChromosome(f, instructionList, insList, subList, whichChromosome):
  instruChars = []  
  insChars = []
  substtuChars = []
  temp = ''
  charsNum = 0

  ## skipping
  ind = 0
  while ind < whichChromosome:
    ## getting the num. of char.s of a prev. chromosome  
    charsNum = len(instructionList[ind])      
    charsNum += len(insList[ind])      
    charsNum += len(subList[ind])      
    ## skipping the char.s of instru.s/ins.s/del.s of this chromosome
    for ind2 in xrange(charsNum):
      temp = chromeMap.skipOneChar(f, temp)    
    ind += 1   
  
  ## getting the char.s of this
  charsNum = len(instructionList[whichChromosome])
  for ind in xrange(charsNum):
    (newCharBits, temp) = chromeMap.getNewCharBits(f, temp)
    instruChars.append(newCharBits)
  charsNum = len(insList[whichChromosome])
  for ind in xrange(charsNum):
    (newCharBits, temp) = chromeMap.getNewCharBits(f, temp)
    insChars.append(newCharBits)
  charsNum = len(subList[whichChromosome])
  for ind in xrange(charsNum):
    (newCharBits, temp) = chromeMap.getNewCharBits(f, temp)
    substtuChars.append(newCharBits)
  
  return (instruChars, insChars, substtuChars)

############################################################################################################################

def getTotalChromosomeLengthFromScratch(refFile, whichChromosome, outHead):
  (basePairsPerLine, numFiles, instructionList, subList, insList, delList) = loadEncodedLists(outHead)    
  return getTotalChromosomeLength(refFile, whichChromosome, basePairsPerLine, numFiles, instructionList, subList, insList, delList)
  
def getTotalChromosomeLength(refFile, whichChromosome, basePairsPerLine, numFiles, instructionList, subList, insList, delList):
      
  ## start decoding/traversing all the instru.s
  nextStart = 0
  targetLen = 0
  chromoInstrus = instructionList[whichChromosome]
  for ind in xrange(len(chromoInstrus)):  
    targetLen += chromoInstrus[ind][1] + 1      # counting the end encoded char. of each instru. 
  targetLen -= 1                                # except the end dummy 'N' char of the last instru.
  
  inssList = insList[whichChromosome]  
  for ind in xrange(len(inssList)):
    targetLen += 1

  delsList = delList[whichChromosome]  
  for ind in xrange(len(delsList)):
    targetLen -= delsList[ind][1]
    
  return targetLen

############################################################################################################################

def extractSubseq(refFile, whichChromosome, subseqStart, subseqLength,
                          basePairsPerLine, numFiles, instructionList, subList, insList, delList,
                          instruChars, insChars, substtuChars):

  refLength = SubseqPicker.getActualFileSize(refFile)
  (Rfile, RheaderSize, Rlinelen,Rheader) = SubseqPicker.openAndPrepare(refFile)

  nextDelIndx = 0
  nextInsIndx = 0
  nextSubIndx = 0

  ## start decoding the subsequence
  hitsCount = 1
  (myChromeSubseq, nextDelIndx, nextInsIndx, nextSubIndx) = getSubSeqFromChromosome(Rfile, refLength, RheaderSize, Rlinelen, Rheader, 
							instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
                                                              instruChars, insChars, substtuChars, subseqStart, subseqLength,
                                                                                    nextDelIndx, nextInsIndx, nextSubIndx)
  currentSeqLen = len(myChromeSubseq)
#  tempSubseq = ''
  while currentSeqLen < subseqLength:
    hitsCount += 1  
    (tempSubseq, nextDelIndx, nextInsIndx, nextSubIndx) = getSubSeqFromChromosome(Rfile, refLength, RheaderSize, Rlinelen, Rheader, 
							instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
                                                              instruChars, insChars, substtuChars, subseqStart+currentSeqLen, subseqLength-currentSeqLen,
                                                                                    nextDelIndx, nextInsIndx, nextSubIndx)
    myChromeSubseq = myChromeSubseq + tempSubseq
#    tempSubseq = ''

    currentSeqLen = len(myChromeSubseq)  

  return (myChromeSubseq[:subseqLength], hitsCount, basePairsPerLine)
  
############################################################################################################################

def extractSubseqInBlocks(refFile, whichChromosome, subseqStart, subseqLength, BlockSize,
                          basePairsPerLine, numFiles, instructionList, subList, insList, delList,
                          instruChars, insChars, substtuChars):
  
  refLength = SubseqPicker.getActualFileSize(refFile)
  (Rfile, RheaderSize, Rlinelen,Rheader) = SubseqPicker.openAndPrepare(refFile)

  tempSubseqLength = subseqLength
  if subseqLength > BlockSize:
    subseqLength = BlockSize
    
  nextDelIndx = 0
  nextInsIndx = 0
  nextSubIndx = 0
    

  ## start decoding the subsequence
  hitsCount = 1
  (myChromeSubseq, nextDelIndx, nextInsIndx, nextSubIndx) = getSubSeqFromChromosome(Rfile, refLength, RheaderSize, Rlinelen, Rheader, 
										instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
                                                                                    instruChars, insChars, substtuChars, subseqStart, subseqLength,
                                                                                    nextDelIndx, nextInsIndx, nextSubIndx)
  currentSeqLen = len(myChromeSubseq)
  while currentSeqLen < tempSubseqLength:
    hitsCount += 1  
    (myChromeSubseqTmp, nextDelIndx, nextInsIndx, nextSubIndx) = getSubSeqFromChromosome(Rfile, refLength, RheaderSize, Rlinelen, Rheader, 
										instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
                                                                                    instruChars, insChars, substtuChars, subseqStart+currentSeqLen, subseqLength,
                                                                                    nextDelIndx, nextInsIndx, nextSubIndx)
    myChromeSubseq += myChromeSubseqTmp
    currentSeqLen += len(myChromeSubseqTmp)

  SubseqPicker.finalizeAndClose(Rfile)  

  return (myChromeSubseq[:tempSubseqLength], hitsCount, basePairsPerLine)
  
############################################################################################################################

def searchSeqsInBlocks(refFile, whichChromosome, subseqStart, subseqLength, BlockSize, seq2search4, searchIndcs,
                          basePairsPerLine, numFiles, instructionList, subList, insList, delList,
                          instruChars, insChars, substtuChars):

  refLength = SubseqPicker.getActualFileSize(refFile)
  (Rfile, RheaderSize, Rlinelen,Rheader) = SubseqPicker.openAndPrepare(refFile)
  
  tempSubseqLength = subseqLength
  if subseqLength > BlockSize:
    subseqLength = BlockSize
  else:
    BlockSize = subseqLength

  nextDelIndx = 0
  nextInsIndx = 0
  nextSubIndx = 0
    
  ## start decoding and searching the first subsequence block
  bfrBetweenBlocks = ''             # keeps the last len(seq2search4)-1 chars of the last block to handle the case seq2search4 is overlapping 2 subsequent blocks 
  #seqLen = len(seq2search4)
  hitsCount = 1
  indcs = []

  (myChromeBlock, nextDelIndx, nextInsIndx, nextSubIndx) = getSubSeqFromChromosome(Rfile, refLength, RheaderSize, Rlinelen, Rheader, 
										instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
                                                              			instruChars, insChars, substtuChars, subseqStart, subseqLength,
                                                                                    nextDelIndx, nextInsIndx, nextSubIndx)
  #searchSubseqInOneBlock(seq2search4, seqLen, myChromeBlock, indcs, subseqStart)
  searchSubseqInTwoOverlappedBlocks(seq2search4, bfrBetweenBlocks, myChromeBlock, searchIndcs, subseqStart)
  currentSeqLen = len(myChromeBlock)
  
  exit = 0
  while currentSeqLen < tempSubseqLength and exit <> 1:
    hitsCount += 1  
    #### keep the last len(seq2search4)-1 chars from the prev. fetched big-seq.
    #bfrBetweenBlocks = myChromeBlock[-(len(seq2search4)-1):]
    bfrBetweenBlocks = myChromeBlock[-(getMaxPatternLength(seq2search4)-1):]
#    if subseqStart+currentSeqLen+subseqLength > subseqStart+tempSubseqLength:
#      print 'shrinking the last search block ...\n'
#      subseqLength = currentSeqLen+subseqLength-tempSubseqLength+1
#      exit = 1

    (myChromeBlock, nextDelIndx, nextInsIndx, nextSubIndx) = getSubSeqFromChromosome(Rfile, refLength, RheaderSize, Rlinelen, Rheader, 
										instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
        			                                                    instruChars, insChars, substtuChars, subseqStart+currentSeqLen, subseqLength,
                                                                                    nextDelIndx, nextInsIndx, nextSubIndx)
    #searchSubseqInOneBlock(seq2search4, seqLen, myChromeBlock, indcs, subseqStart+currentSeqLen)
    searchSubseqInTwoOverlappedBlocks(seq2search4, bfrBetweenBlocks, myChromeBlock, searchIndcs, subseqStart+currentSeqLen)
    currentSeqLen += len(myChromeBlock)

  SubseqPicker.finalizeAndClose(Rfile)  

  return (indcs, hitsCount)
  
############################################################################################################################
#  if seq2search4.find('-') > -1:  
#    (seqIndcs, hitsCount) = searchSubseqWithDashsInBlocks(refFile, whichChromosome, subseqStart, subseqLength, outHead, BlockSize, seq2search4,  searchIndcs)
#  else:  

#def searchSubseqWithDashsInBlocks(refFile, whichChromosome, subseqStart, subseqLength, outHead, BlockSize, seq2search4):
#
#  (basePairsPerLine, numFiles, instructionList, subList, insList, delList) = loadEncodedLists(outHead) 
#  
#  (instruChars, insChars, substtuChars) = loadEncodedChars(outHead, instructionList, subList, insList, delList, whichChromosome)
#  
#  tempSubseqLength = subseqLength
#  if subseqLength > BlockSize:
#    subseqLength = BlockSize
#  ## split the seq2search4 into 2 subsequences ...
#  dashIndx = seq2search4.find('-')
#  dashCount = seq2search4.count('-')
#  #seq2search4 = seq2search4.replace('-', '') 
#  seq2search4_1 = seq2search4[:dashIndx]
#  seq2search4_2 = seq2search4[dashIndx+dashCount:]  
#  ## start decoding and searching the first subsequence block
#  bfrBetweenBlocks = ''             # keeps the last len(seq2search4)-1 chars of the last block to handle the case seq2search4 is overlapping 2 subsequent blocks 
#  seqLen = len(seq2search4_1)
#  hitsCount = 1
#  indcs = []
#  myChromeBlock = getSubSeqFromChromosome(refFile, instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
#                                                              instruChars, insChars, substtuChars, subseqStart, subseqLength)
#  #searchSubseqInOneBlock(seq2search4, seqLen, myChromeBlock, indcs, subseqStart)
#  searchSubseqWithDashsInTwoOverlappedBlocks(seq2search4_1, dashCount, seq2search4_2, seqLen, bfrBetweenBlocks, myChromeBlock, indcs, subseqStart)
#  currentSeqLen = len(myChromeBlock)
#
#  exit = 0  
#  while currentSeqLen < tempSubseqLength and exit <> 1:
#    hitsCount += 1  
#    #### keep the last len(seq2search4)-1 chars from the prev. fetched big-seq.
#    bfrBetweenBlocks = myChromeBlock[-(len(seq2search4)-1):]
#
##    if subseqStart+currentSeqLen+subseqLength > subseqStart+tempSubseqLength:
##      print 'shrinking the last search block ...\n'
##      subseqLength = currentSeqLen+subseqLength-tempSubseqLength+1
##      exit = 1
#
#    myChromeBlock = getSubSeqFromChromosome(refFile, instructionList[whichChromosome], subList[whichChromosome], insList[whichChromosome], delList[whichChromosome],
#                                                              instruChars, insChars, substtuChars, subseqStart+currentSeqLen, subseqLength)
#    #searchSubseqInOneBlock(seq2search4, seqLen, myChromeBlock, indcs, subseqStart+currentSeqLen)
#    searchSubseqWithDashsInTwoOverlappedBlocks(seq2search4_1, dashCount, seq2search4_2, seqLen, bfrBetweenBlocks, myChromeBlock, indcs, subseqStart+currentSeqLen)
#    currentSeqLen += len(myChromeBlock)
#
#  return (indcs, hitsCount)
#  
############################################################################################################################

def getMaxPatternLength(seq2search4):
  seqLen = 0
  maxLen = 0
  for seq in seq2search4:
    seqLen = len(seq)   
    if seqLen > maxLen:
      maxLen = seqLen      
  return maxLen


#def BruteForceSearch(pattern, sequence, hits, startIndex, globalOffsetShift):
#  j = startIndex
#  count = 0
#  m = len(pattern)
#  n = len(sequence)
#  while j <= n-m:
#    i = 0
#    while i < m and pattern[i] == sequence[i+j]:
#      i += 1
#    if i >= m:
#      hits.append(globalOffsetShift + j + 1)
#      count += 1
#    j += 1  
#  return count


def BruteForceSearch(pattern, m, sequence, n, startIndex):
  j = startIndex
  #m = len(pattern)
  #n = len(sequence)
  while j <= n-m:
    i = 0
    while i < m and pattern[i] == sequence[i+j]:
      i += 1
    if i >= m:
      return j
    j += 1  
  return -1
#    sequence = asequence[startIndex:]
#    m = len(pattern)
#    n = len(sequence)
#    if m > n: return -1
#    skip = []
#    for k in range(256): skip.append(m)
#    for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1
#    skip = tuple(skip)
#    k = m - 1
#    while k < n:
#        j = m - 1; i = k
#        while j >= 0 and sequence[i] == pattern[j]:
#            j -= 1; i -= 1
#        if j == -1: 
#            return startIndex + i + 1
#        k += skip[ord(sequence[k])]
#    return -1



def searchSubseqInTwoOverlappedBlocks(seq2search4, bfrBetweenBlocks, myChromeBlock, searchIndcs, blockAbsoluteStart):
  overlappedChars = len(bfrBetweenBlocks)  
  overlappedBlock = bfrBetweenBlocks + myChromeBlock
  BlockLen = len(overlappedBlock)
  hits = 0
  hitIndx = -1
  
  for i in xrange(len(seq2search4)):
    seq = seq2search4[i]   
    SeqLen = len(seq)
    correction = overlappedChars - len(seq) + 1
    indcs = searchIndcs[i]
    if seq.find('-') == -1:         ## searching by exact pattern      
        ###BruteForceSearch(seq, overlappedBlock, indcs, correction, (blockAbsoluteStart-overlappedChars))
        indx = overlappedBlock.find(seq, correction)
        #$$$$$$$$$$indx = BruteForceSearch(seq, SeqLen, overlappedBlock, BlockLen, correction)
        while indx <> -1:
          hitIndx = (blockAbsoluteStart-overlappedChars)+(indx)
          indcs.append(hitIndx)
          ## search for the next match starting from the 2nd character in this match
          indx = overlappedBlock.find(seq, indx+1)
          #$$$$$$$$$$indx = BruteForceSearch(seq, SeqLen, overlappedBlock, BlockLen, indx+1)
          ## we should use the following instru. instead if we want to search for matches occuring next to the current overall match
          ##indx = overlappedBlock.find(seq2search4[i], indx+seqLen)
    else:                                   ## searching by incomplete pattern
        ## split the seq2search4 into 2 subsequences ...
        dashIndx = seq.find('-')
        dashCount = seq.count('-')
        seq2search4_1 = seq[:dashIndx]
        seq2search4_2 = seq[dashIndx+dashCount:]  
        indx1 = overlappedBlock.find(seq2search4_1, correction)
        SeqLen = len(seq2search4_1)
        SeqLen2 = len(seq2search4_2)
        #$$$$$$$$$$indx1 = BruteForceSearch(seq2search4_1, SeqLen, overlappedBlock, BlockLen, correction)
        ## if found, search for second part immediately after dashs
        while indx1 <> -1:
          start = indx1+SeqLen+dashCount
          ## if part2 is found immediately after dashs, add this hit, and start searching after the overall hit
          if overlappedBlock[start:start+SeqLen2] == seq2search4_2:
            hitIndx = (blockAbsoluteStart-overlappedChars)+(indx1)
            indcs.append(hitIndx)
            ##indx1 = overlappedBlock.find(seq2search4_1, indx2+len(seq2search4_2)+1)
          indx1 = overlappedBlock.find(seq2search4_1, indx1+1)
          #$$$$$$$$$$indx1 = BruteForceSearch(seq2search4_1, SeqLen, overlappedBlock, BlockLen, indx1+1)

############################################################################################################################

####################### ONLINE ADJUSTMENT/SHIFTING OF INSTRU./SUBSEQ. TARGET-BASED POS. #############################
## instru. pos. is relative to del.s and ins.s, so, to find the instru. abs. target pos., - prev. dels, + prev. ins. (as if they are already executed)
## subseq. pos. is abs. to original target, so,:
##         we should either:
##                * execute del.s, ins.s of occuring inside instru. b4 the subseq. 
##                or
##                * find subseq. pos. relative to prev. del.s, ins.s inside this instru., AND DON'T EXECUTE THEM:  + prev. dels, - prev. ins. (as if they are NOT executed)

def getSubSeqFromChromosome(Rfile, refLength, RheaderSize, Rlinelen, Rheader, 
				instructionList, subList, insList, delList, instruChars, insChars, substtuChars, subseqStart, subseqLength,
                                                nextDelIndx, nextInsIndx, nextSubIndx):
  
                        #************* start reading reference as a single non-lined stream ******************#
  originalSubseqStart = subseqStart
  originalSubseqLength = subseqLength

  #refLength = SubseqPicker.getActualFileSize(refFile)
  #(Rfile, RheaderSize, Rlinelen,Rheader) = SubseqPicker.openAndPrepare(refFile)
                        
                        ############ End reading reference as a single non-lined stream #######################

  (fakeSubseqStart, countedDels, countedInss) = getFakeSubseqPos(subseqStart, delList, insList)
  actualShiftB4Subseq = subseqStart - fakeSubseqStart
                        
                        #********* Start fetching the instru. containing this subseq., then loading it from the ref. seq. **************************#
  
  ## required subseq info
  targetString = ''
  needToVisitNextInstru = 0
  nextSubseqStart = -1
  remainingSubseqLength = 0
  needCharEncodedAtEndOfInstru = 0
  needEncodedCharOnly = 0
  
  totalCountedInss = 0
  totalCountedDels = 0

  # Length of target after all the instructions
  nextTargetLength = 0
  actualShiftInsideSubseqFromPrevInstru = 0

  ## traverse all the instructions to find the instruction containing the subsequence start position
  for ind in xrange(len(instructionList)):
    actualInstruPosInRef  = instructionList[ind][0]-1 # Because start is 1-based
    length = instructionList[ind][1]
    stop   = actualInstruPosInRef + length
    subRefInstruFakeTargetPos = nextTargetLength      ## GETING CURRENT TARGET-BASED POS. OF THIS INSTRU. 
    ###### determine whether this instru. will pass (plus the length of current the target seq.) after the required subseq. interval ?? 
    nextTargetLength = nextTargetLength + length
    ## check whether the current instruction contains the needed TARGET-BASED subseq.
    ## fix > -->> >=
    ## if the whole subseq. is included inside one instru.
    if subRefInstruFakeTargetPos <= fakeSubseqStart and subRefInstruFakeTargetPos + length + 1 >= (fakeSubseqStart + subseqLength):  
      needToVisitNextInstru = 0
      if subRefInstruFakeTargetPos + length + 1 == (fakeSubseqStart + subseqLength):  ## the subseq. ends by the encoded char of this instru.
        needCharEncodedAtEndOfInstru = 1
        if subseqLength == 1 :
          needEncodedCharOnly = 1  
        subseqLength -= 1  
      else:
        needCharEncodedAtEndOfInstru = 0
      nextSubseqStart = -1
      remainingSubseqLength = 0
    ## if the subseq. starts inside this instru., but extends after the end of this instru.
    elif subRefInstruFakeTargetPos <= fakeSubseqStart and subRefInstruFakeTargetPos + length > fakeSubseqStart:
      needToVisitNextInstru = 1
      needCharEncodedAtEndOfInstru = 1  
      nextSubseqStart = nextTargetLength + 1    ## jumping the encoded char of this instru. -- start of next. instru.
      remainingSubseqLength = subseqLength - (nextTargetLength - fakeSubseqStart)
      subseqLength -= remainingSubseqLength     ## don't consider the encoded char of this instru.
      #println
    ## if the subseq. starts at the encoded char of this instru.  
    elif subRefInstruFakeTargetPos + length == fakeSubseqStart:
      needToVisitNextInstru = 1
      needEncodedCharOnly = 1
      needCharEncodedAtEndOfInstru = 1
      nextSubseqStart = nextTargetLength + 1    ## jumping the encoded char of this instru. -- start of next. instru.
      remainingSubseqLength = subseqLength  
    ## this case to skip the current instru. without altering any info. of the subseq.   
    ## if the subseq. starts after the end of this instru, then skip all the instru. (including its encoded char: 
    ##            start = length of this. instru. + 1 (of encoded char)
    elif subRefInstruFakeTargetPos + length + 1 <= fakeSubseqStart:  
      #needEncodedCharOnly = 1
      #needToVisitNextInstru = 1
      nextTargetLength += 1                 ## adding the encoded char of this instru. to the total cumulative count
      #fakeSubseqStart = nextTargetLength    ## jumping the encoded char of this instru.
      continue  
        
    if subseqLength == 0:
        needEncodedCharOnly = 1    
    ## fetch the determined subseq. with the determined boundaries ...
    if not needEncodedCharOnly:
      (subtargetString, extraCharsResultedFromInss, countedInss, countedDels, nextDelIndx, nextInsIndx, nextSubIndx) = extractSubseqFromInstru(subseqStart, fakeSubseqStart, subseqLength, totalCountedDels, totalCountedInss, 
                                            actualInstruPosInRef, subRefInstruFakeTargetPos, actualShiftB4Subseq, actualShiftInsideSubseqFromPrevInstru,  
                                            delList, insList, subList, insChars, substtuChars, Rfile, RheaderSize, Rlinelen,
                                            nextDelIndx, nextInsIndx, nextSubIndx)
      executedInssDelsWillAffectNextInssDels = countedInss - countedDels
      totalCountedInss += countedInss
      totalCountedDels += countedDels  
      targetString += subtargetString
      actualShiftInsideSubseqFromPrevInstru += executedInssDelsWillAffectNextInssDels
    
    ## checking the obtained more/less char.s in order to adjust the next required char.s
      adjustedLen = 0
      if needToVisitNextInstru == 1:
        extraLen = len(extraCharsResultedFromInss)   
        if extraLen > 0:  
          targetString += extraCharsResultedFromInss
          adjustedLen = extraLen
        currentLen = len(subtargetString)  
        if currentLen < subseqLength:
          lessLen = subseqLength - currentLen  
          adjustedLen = -lessLen     

      #if adjustedLen > 0:  
      nextTargetLength += adjustedLen
      nextSubseqStart += adjustedLen
      remainingSubseqLength -= adjustedLen
      
      ## fix 1 for memory consumption
      #subtargetString = ''
    #actualShift += executedInssDelsWillAffectNextInssDels
      
    # get the instru.'s end encoded char: either to use it, or to read it to seek to the next chromeMap char.
    if ind < len(instructionList)-1 and needCharEncodedAtEndOfInstru == 1:
      nextTargetLength = nextTargetLength + 1
      remainingSubseqLength -= 1    ## subtract this char from the remaining char.s
      #subseqLength += 1             ## add this char to the current length
      needCharEncodedAtEndOfInstru = 0
      needEncodedCharOnly = 0
      if stop == refLength:
        newChar = chromeMap.bitToChrome['N'+instruChars[ind]]       ## I think this line became useless
      else:
        refChar = SubseqPicker.PickSubseq(Rfile, stop, 1, RheaderSize, Rlinelen)
        newChar = chromeMap.bitToChrome[refChar+instruChars[ind]]
        targetString = targetString + newChar           

#    (Tfile, TheaderSize, Tlinelen, Theader) = SubseqPicker.openAndPrepare('t_yh/chr5.fa3')
#    originalSubseq = SubseqPicker.PickSubseq(Tfile, subseqStart, len(targetString), TheaderSize, Tlinelen)
#    if originalSubseq <> targetString:
#        print originalSubseqStart, '-', len(targetString), '\t'
#    SubseqPicker.finalizeAndClose(Tfile)

    if needToVisitNextInstru == 0 or ind == len(instructionList)-1 or remainingSubseqLength <= 0 or len(targetString) >= originalSubseqLength:
      break

    ## re-adjust the new start, according to the more/less char.s obtained by ins.s/del.s inside the last subseq. picks
#    subseqStart += len(target) 
    fakeSubseqStart = nextSubseqStart
    subseqLength = remainingSubseqLength  #print "seqpicker", originalSubseq, "\n"
  #originalSubseq += 't'

#  (Tfile, TheaderSize, Tlinelen, Theader) = SubseqPicker.openAndPrepare('t_yh/chr7.fa')
#  originalSubseq = SubseqPicker.PickSubseq(Tfile, originalSubseqStart, len(targetString), TheaderSize, Tlinelen)
#  if originalSubseq <> targetString:
#      print originalSubseqStart, '-', len(targetString), '\t'
#  SubseqPicker.finalizeAndClose(Tfile)


  return (targetString, nextDelIndx, nextInsIndx, nextSubIndx)

############################################################################################################################

def getActualInstruTargetPos(subRefInstruFakeTargetPos, delList, insList):
                        #********* Start finding del.s occuring b4 instru. - forcing shift left of instru. abs. target-pos **************************#
                        ## FACT: POS. OF DEL.S IS TARGET-BASED (INCLUDING NON-EXECUTED PREV. DEL.S)(i.e. WITHOUT EXECUTING PREV. DELS)
  subRefInstruActualTargetPos = subRefInstruFakeTargetPos
  ## traverse all the del.s which have occured before this instru., then sum their lengths
  ## we will NOT execute them, just adjust the instru. abs. target pos. as if they are executed (cut from the instru. pos.)
  if len(delList) > 0: 
    ind = 0
    ## checking for complete dels occuring b4 this instru. - adjusting instru. target-pos. with these del.s
    while ind < len(delList) and (delList[ind][0]+delList[ind][1]) < subRefInstruFakeTargetPos:
      subRefInstruActualTargetPos -= delList[ind][1]
      ind += 1

    ##subseqStart += subRefInstruActualTargetPos                   ## bcz the subseq. should be shifted just like its container instru.
               
                        ########## End finding del.s occuring b4 instru. #############################

                        #********* Start finding ins.s occuring b4 instru. - forcing shift right of instru. abs. target-pos **************************#

  ## traverse all the ins.s which have occured before this instru., then count them
  ## we will NOT execute them, just adjust the instru. actual target pos. as if they are executed (inserted chars b4 instru. -> add to instru. pos.)
  subRefInstruFakeTargetPos = subRefInstruActualTargetPos
  if len(insList) > 0: 
    ind = 0
    while ind < len(insList) and insList[ind][0] < subRefInstruFakeTargetPos :
      subRefInstruActualTargetPos += 1
      ind += 1

    #subRefInstruActualTargetPos -= insCountB4Instru       ## bcz we won't make these ins.s
    #subseqStart -= insCountB4Instru                     ## bcz the subseq. should be shifted just like its container instru.

                        ########## End finding ins.s occuring b4 required subseq. #############################
  return subRefInstruActualTargetPos

############################################################################################################################
    
# virtually undelete the deleted char.s and uninsert the inserted char.s before this subseq. pos.    
def getFakeSubseqPos(subseqStart, delList, insList):
                                #********* Start finding del.s occuring b4 required subseq. - forcing shift right **************************#
  fakeSubseqStart = subseqStart
  countedDels = 0
  countedInss = 0
  #### dels, inss, instrus were 1 based during compression###########################################

#  delsInd = 0
#  inssInd = 0
#  while delsInd < len(delList) or inssInd < len(insList):
#    if delsInd == len(delList):     ## apply remaining inss only 
#      if insList[inssInd][0] < fakeSubseqStart:  
#        fakeSubseqStart -= 1
#        countedInss -= 1
#        inssInd += 1
#      else:
#        inssInd = len(insList)    
#    elif inssInd == len(insList):   ## apply remaining dels only
#      if delList[delsInd][0] < fakeSubseqStart:  
#        fakeSubseqStart += delList[delsInd][1]
#        countedDels += delList[delsInd][1]
#        delsInd += 1
#      else:
#        delsInd = len(delList)    
#    elif delList[delsInd][0] < insList[inssInd][0]:
#      if delList[delsInd][0] < fakeSubseqStart:  
#        fakeSubseqStart += delList[delsInd][1]
#        countedDels += delList[delsInd][1]
#        delsInd += 1
#      else:
#        delsInd = len(delList)    
#    else:
#      if insList[inssInd][0] < fakeSubseqStart:  
#        fakeSubseqStart -= 1
#        countedInss -= 1
#        inssInd += 1
#      else:
#        inssInd = len(insList)    
#        
#  #fakeSubseqStart += countedDels  
#  #fakeSubseqStart += countedInss

  fakeSubseqStart = subseqStart
  ## traverse all the ins.s which have occured before this subseq., then count them
  ## we will NOT execute them, just adjust the subseq. start as if they are executed
  if len(insList) > 0: 
    ##insCountB4Subseq = 0
    ind = len(insList)-1
    while ind >= 0:
      if insList[ind][0] - 1 < fakeSubseqStart:  
        fakeSubseqStart -= 1
        countedInss -= 1
      ind -= 1

  #fakeSubseqStart = subseqStart
  ## traverse all the del.s which have occured before this subseq., then sum their lengths
  ## we will NOT execute them, just adjust the subseq. start as if they are NOT executed
  if len(delList) > 0: 
    ##delLengthsB4Subseq = 0
    ind = 0
    ## checking for COMPLETE dels occuring inside this instru. and b4 the subseq.
    for ind in xrange(len(delList)):  
      if delList[ind][0] - 1 < fakeSubseqStart:  
        fakeSubseqStart += delList[ind][1]
        countedDels += delList[ind][1]
      else:
        break
                        ########## End finding del.s occuring b4 required subseq. #############################
##  fakeSubseqStart = subseqStart
#  ## traverse all the ins.s which have occured before this subseq., then count them
#  ## we will NOT execute them, just adjust the subseq. start as if they are executed
#  if len(insList) > 0: 
#    ##insCountB4Subseq = 0
#    ind = 0
#    for ind in xrange(len(insList)):
#      insList[ind][0] -= 1  
#      if insList[ind][0] < fakeSubseqStart:  
#        fakeSubseqStart -= 1
#        countedInss -= 1
#      else:
#        break  

                        #********* Start finding ins.s occuring b4 required subseq. - forcing shift left **************************#


#    fakeSubseqStart += countedDels  
#    fakeSubseqStart += countedInss
                        ########## End finding ins.s occuring b4 required subseq. #############################
  ##fakeSubseqStart += (subRefInstruFakeTargetPos - subRefInstruActualTargetPos)
  return (fakeSubseqStart, countedDels, countedInss)

############################################################################################################################

def extractSubseqFromInstru(subseqStart, fakeSubseqStart, subseqLength, totalCountedDels, totalCountedInss, 
                            actualInstruPosInRef, subRefInstruFakeTargetPos, actualShift, actualShiftInsideSubseqFromPrevInstru,
                            delList, insList, subList, insChars, substtuChars, Rfile, RheaderSize, Rlinelen,
                            nextDelIndx, nextInsIndx, nextSubIndx):

        ####################### FETCHING SUBSEQ. FROM INSTRU. ######################3

  #subRefInstruActualTargetPos = getActualInstruTargetPos(subRefInstruFakeTargetPos, delList, insList)
  ## ins.s/del.s occuring b4 the instru. - previously ADDED to the instru.immature.target.pos to get instru.actual.target.pos
  ## becomes invalid when fakesubseq. became changeable every overlapping instru.
  ##InssDelsB4Instru = (subRefInstruActualTargetPos - subRefInstruFakeTargetPos)
  ## ins.s/del.s occuring b4 the subseq. - previously ADDED to the subseq.actual.given.pos to get subseq.immature.target.pos
  ##   ## becomes invalid when fakesubseq. became changeable every overlapping instru. 
  ##InssDelsAfterInstruB4Subseq = subseqStart - fakeSubseqStart
  ## distance from instru.ref.pos to subseq.ref.pos. (num. of chars from start of instru till subseq.) - with 3 valid ways:
  ## will be zero if subseq. is starting from the start of the instru.
  fakeDistanceFromInstruToSubseq = (fakeSubseqStart - subRefInstruFakeTargetPos)
    ## initially, seek to the stat of the instru.ref.pos
  fakeSubseqPosInRef = actualInstruPosInRef + fakeDistanceFromInstruToSubseq

  targetContent = SubseqPicker.PickSubseq(Rfile, fakeSubseqPosInRef, subseqLength, RheaderSize, Rlinelen)

  #printMemUse('1')
#  targetString = list(targetContent)
  #targetContent = ''
  #printMemUse('2')

                        #********* Start applying del.s inside the target subseq. **************************#
  fakeSubseqEnd = fakeSubseqStart+subseqLength

  # Now do all the deletions
  delsCount = 0
  allDels = len(delList)

  if allDels > 0:
    ind = nextDelIndx-10	## go back 10 dels in the dels list in order to re-apply the dels that were applied and trimmed during trimming the extra chars of the past block
    if ind < 0:
      ind = 0
    while ind < len(delList):
      # dels were already built with fake positions (During compression) where every del had an offset that depends on the existance of its all prev. dels
      # -delsCount:                                del. fake offset is affected (goes backward) by the recently executed dels inside this subseq.
      # +actualShiftInsideSubseqFromPrevInstru:    - deleted dels executed inside this subseq in previous instru.s
      #                                            + inserted inss executed inside this subseq in previous instru.s (would be executed after finishing all dels)
      start  = delList[ind][0] - 1 - delsCount + actualShiftInsideSubseqFromPrevInstru     ## consider how many char.s have been deleted by prev. del.s, bcz this will affect position of next del.s      
      length = delList[ind][1]
      if start >= fakeSubseqStart and start < (fakeSubseqEnd - delsCount):
        start -= fakeSubseqStart                     ## adjust the del. start relative to the subseq. start
        stop   = start + length
#        del(targetString[start:stop])             ## delete this ref. subseq. from the immature target seq.
        targetContent = targetContent[:start] + targetContent[stop:]
        delsCount += length
#        nextDelIndx += 1
    # might be a deletion is not executed completely during the end of the past block
#      elif start < fakeSubseqStart and start + length > fakeSubseqStart:
#        print 'broken del found !!!' 
#        newlen = length - (fakeSubseqStart-start)
#        del(targetString[0:newlen])
#        delsCount += newlen
      elif start >= (fakeSubseqEnd - delsCount):
        break    
      ind += 1
    nextDelIndx = ind    

#  if targetString <> list(targetContent):
#    print 'oh 1'
                        ########## End applying del.s inside the target subseq. #############################

                        #********* Start applying ins.s inside the target subseq. **************************#
  # Now do all the insertions
  fakeSubseqEnd -= delsCount
  ## should shift the ins. pos. by non-executed ins.s/del.s to know how much the fakeSubseq. pos. is affected/shifted from the actual subseq. pos.
  inssCount = 0
  allInss = len(insList)
 
  if allInss > 0:
    ind = nextInsIndx-10	## go back 10 inss in the inss list in order to re-apply the inss that were applied and trimmed during trimming the extra chars of the past block
    if ind < 0:
      ind = 0
    while ind < len(insList):
      # -1 Because we're 1-based
      ## getting fake ins. pos. by subtracting num of not executed (inserted/deleted) ins.s/dels. b4 this subseq. 
      # -actualShift:                              + non-deleted dels previous to this subseq offset
      #                                            - non-inserted inss previous to this subseq offset
      position = insList[ind][0] - 1 - actualShift# - totalCountedInss
      if position >= fakeSubseqStart and position < (fakeSubseqEnd + inssCount):		# extending the subseqLength by the newly added inss.
        inssCount += 1    
        ## if ins. pos. occur at the end of the current target subseq., just append it. 
        ## get the ins. char, then insert it into the target subseq.
#        try:
        start = position-fakeSubseqStart  
        refChar = targetContent[start]
        newChar = chromeMap.bitToChrome[refChar+insChars[ind]]  
#        targetString.insert(start, newChar)          ## adjusting the ins. position to the start of the subseq.
        targetContent = targetContent[:start] + newChar + targetContent[start:]
#        if targetString <> list(targetContent):
#          print 'oh 2'
#          print targetContent[start-5:10]
#        nextInsIndx += 1
#        except Exception:
#          print fakeSubseqStart 
#          print '  '
#          print insList[ind][0]     
#          print '  '
#          print actualShift
#          print '  '
#          print totalCountedInss
#          print '  '
#          print totalCountedDels
#          print '  '
        #######targetString = targetString[:position-fakeSubseqStart-1] + newChar + targetString[position-fakeSubseqStart:]          ## adjusting the ins. position to the start of the subseq.          
      elif position >= fakeSubseqEnd + inssCount:        ## skip ins.s occuring after the subseq. interval
        break
      ind += 1
    nextInsIndx = ind    
                       ########## End applying ins.s inside the target subseq. #############################
#  if targetString <> list(targetContent):
#    print 'oh 2'
 
                        #********* Start applying substtu.s inside the target subseq. **************************#
  currlen = len(targetContent)
  #fakeSubseqEnd += inssCount
#  fakeSubseqEnd += delsCount
  fakeSubseqEnd = fakeSubseqStart+currlen
  ## should shift the substtu. pos. by non-executed ins.s/del.s to know how much the fakeSubseq. pos. is affected/shifted from the actual subseq. pos.
  # Now do all the substitutions
  allSubs = len(subList)
  
  if allSubs > 0:
    ind = nextSubIndx-10	## go back 10 subs in the subs list in order to re-apply the subs that were applied and trimmed during trimming the extra chars of the past block
    if ind < 0:
      ind = 0
    while ind < len(subList):
      # -1 Because we're 1-based
      ## getting fake sub.s pos. by subtracting num of not executed (inserted/deleted) ins.s/dels. b4 this subseq. 
      # -actualShift:                              + non-deleted dels previous to this subseq offset
      #                                            - non-inserted inss previous to this subseq offset
      ## but because the del.s/ins.s starting from this subseq. till before these substtu.s are all supposed to be executed, there is no need to 
      ##     alter the position anymore
      position = subList[ind][0] - 1 - actualShift# - totalCountedInss
      if position >= fakeSubseqStart and position < fakeSubseqEnd:
        position -= fakeSubseqStart
        #if position < len(targetString):
        refChar = targetContent[position]
        newChar = chromeMap.bitToChrome[refChar+substtuChars[ind]]  
#        targetString[position] = newChar
        targetContent = targetContent[:position] + newChar + targetContent[position+1:]
#        nextSubIndx += 1
      elif position >= fakeSubseqEnd:        ## skip substtu.s occuring after the subseq. interval
        break
      ind += 1
    nextSubIndx = ind    

                        ########## End applying substtu.s inside the target subseq. #############################
#  if targetString <> list(targetContent):
#    print 'oh 3'

                        ########### End fetching the instru. containing this subseq., then loading it from the ref. seq. ################

  # Change back to string, returning the extra char.s if any
#  extraCharsResultedFromInss = "".join(targetString[subseqLength:])
  extraCharsResultedFromInss = targetContent[subseqLength:]
  ##printMemUse('1')
#  printMemUse('1')             
#  targetContent = "".join(targetString[:subseqLength])   # trim any extra char.s resulting from ins.s executed inside the extracted subseq.
  #del(targetString[:])
#  printMemUse('2')
  ##targetContent = str(targetString[:subseqLength])                                299 -> 834
  ###targetContent = array('B', map(ord,targetString[:subseqLength])).tostring()    299 -> 416
  ###targetContent = str(targetString[:subseqLength]).replace("', '","")           299 -> 807 and fail
  
#  targetContent=''                                                                299 -> 447 and fail
#  for i in range(0,subseqLength):
#    targetContent=targetContent+targetString[i]
  ##printMemUse('2')

  return (targetContent[:subseqLength], extraCharsResultedFromInss, inssCount, delsCount, nextDelIndx, nextInsIndx, nextSubIndx)  
  
###########################################################################################################################################

def saveChromosomeIntoFile(outHead, targetFile, basePairsPerLine, whichChromosome, targetString, targetLength):  
  # Read in the headers
  myHeader = ''
  headerFilename    = outHead+'headers.ido'
  f = open(headerFilename, 'rb')
  ind = 0
  while ind < whichChromosome:
    temp = f.readline()
    ind += 1
  temp = f.readline()  
  myHeader = temp[:-1]
  f.close()

  # Write out the chromosome
  f2 = open(targetFile + 'NEW', 'w')

  # Print a header if there is one
  if len(myHeader) > 0:
    f2.write(myHeader + "\n")

  ## writing lined file from the generated non-lined data
  lines = targetLength/basePairsPerLine
# to write extra non-complete line, use the following two lines with the line before f2.close:
#  if targetLength % basePairsPerLine == 0:
#    lines -= 1
  for ind in xrange(lines):
    f2.write(targetString[ind*basePairsPerLine:(ind+1)*basePairsPerLine] + "\n")
  # or alternatively use these three lines:
  remainder = targetString[(ind+1)*basePairsPerLine:]
  if remainder <> '':
    f2.write(remainder+"\n")
  #f2.write(targetString[(ind+1)*basePairsPerLine:]+"\n")
  f2.close()  

###########################################################################################################################################

def printMemUse(tag):
  memUse = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  memUse = memUse / 1024.0
  print tag, '\t Memory Usage : %d MB' %memUse
    
