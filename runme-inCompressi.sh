#clear

#./inCompressiTester tair8/chr2.fas 2 0 100000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 0.009369 sec
#SubseqPicker : 0.001257 sec

#./inCompressiTester tair8/chr2.fas 2 100000 100000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 0.014626 sec
#SubseqPicker : 0.002553 sec

#./inCompressiTester tair8/chr2.fas 2 300000 400000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 0.026067 sec
#SubseqPicker : 0.005997 sec

#./inCompressiTester tair8/chr2.fas 2 100000 100000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 200000 100000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 300000 100000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 400000 100000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 500000 100000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 800000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 100000 700000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 1000000 600000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 1000000 1000000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 1000000 1100000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 1000000 1120000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 700000 100000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 895000 1000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 896200 30 tair/tair_ tair9/TAIR9_chr2.fas

## fixed in new chrome map, except for 'Z'
#./inCompressiTester tair8/chr2.fas 2 896200 40 tair/tair_ tair9/TAIR9_chr2.fas

## perform more hits to reimburse dels ... fixed
#./inCompressiTester tair8/chr2.fas 2 859500 50 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 860000 2000 tair/tair_ tair9/TAIR9_chr2.fas

## fixed by subtracting non-executed ins.s b4 instru. from the actual ins. pos. b4 executing it inside subseq.
#./inCompressiTester tair8/chr2.fas 2 859000 1900 tair/tair_ tair9/TAIR9_chr2.fas

## fixed by setting codes of chromeMap in 3 bits, because NN pastly coded by '', make a bug when loading codes, it took the 2-bit code of the next encoding
#./inCompressiTester tair8/chr2.fas 2 838250 15 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 2000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 0.225238 sec
#SubseqPicker : 0.058852 sec

#./inCompressiTester tair8/chr2.fas 2 0 5000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 0.864944 sec
#SubseqPicker : 0.098708 sec

#./inCompressiTester tair8/chr2.fas 2 0 10000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 1.967932 sec
#SubseqPicker : 0.197233 sec

## fixed by subtracting non-executed ins.s/del.s (the shift/difference between fake/actual subseq. pos.) from the actual ins.s pos. 
#./inCompressiTester tair8/chr2.fas 2 10410800 35 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 10000000 410835 tair/tair_ tair9/TAIR9_chr2.fas

## fixed by subtracting non-executed ins.s/del.s (the shift/difference between fake/actual subseq. pos.) from the actual substtu.s pos. 
#./inCompressiTester tair8/chr2.fas 2 10417370 25 tair/tair_ tair9/TAIR9_chr2.fas

########## was delegated but now ok
#./inCompressiTester tair8/chr2.fas 2 0 838300 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 1000000 1130000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 800000 100000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 400000 410000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10671350 800 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 10600000 100000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 10670390 200000 tair/tair_ tair9/TAIR9_chr2.fas

## fixed, was returning extra chars of lastSubFetch with first extra char lost ----- overlap 3 instru.s
#./inCompressiTester tair8/chr2.fas 2 10400000 275000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 10671000 3000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 10400000 280000 tair/tair_ tair9/TAIR9_chr2.fas

# overlap 3 instru.s 
# fixed ... was comparing the fake pos of ins.s with the actual subseq. pos. to exit the ins.s execution loop
#./inCompressiTester tair8/chr2.fas 2 10000000 1000000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 10000000 5000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 0.469226 sec
#SubseqPicker : 0.086705 sec

#./inCompressiTester tair8/chr2.fas 2 10000000 9000000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 15000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 3.087148 sec
#SubseqPicker : 0.555876 sec

#./inCompressiTester tair8/chr2.fas 2 0 18000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 2.663524 sec
#SubseqPicker : 0.368052 sec

## fixed by adjusting the del.pos. 2 b executed as follows: original-1-based-del - 2 + shifts b4 subseq. + past shifts inside subseq.
#./inCompressiTester tair8/chr2.fas 2 10000000 9200000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10500000 9000000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 20000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 2.879828 sec
#SubseqPicker : 0.335508 sec

#./inCompressiTester tair8/chr2.fas 2 0 25000000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 3.421593 sec
#SubseqPicker : 0.477683 sec

#./inCompressiTester tair8/chr2.fas 2 0 30300000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 30400000 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 3.570204 sec
#SubseqPicker : 0.606478 sec

#./inCompressiTester tair8/chr2.fas 2 0 30425000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 0 30427668 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 10671395 50 tair/tair_ tair9/TAIR9_chr2.fas

## fixed by adding third case: if subseq. starts b4,after, in the end-encoded char of some instru.
#./inCompressiTester tair8/chr2.fas 2 10671396 50 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10671393 50 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10671394 50 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10671395 50 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10671396 50 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10671397 50 tair/tair_ tair9/TAIR9_chr2.fas

## fixed by adding <= instead of == to the last case
#./inCompressiTester tair8/chr2.fas 2 10671397 50 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 10671397 1000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 15000000 100 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 19000000 500000 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 0 30427669 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 30427669 tair/tair_ tair9/TAIR9_chr2.fas

### ALL THE SEQUENCE, BUT < ORIGINAL FASTA FILE BCZ NO HEADER OR \n's ADDED YET
#./inCompressiTester tair8/chr2.fas 2 0 30427672 tair/tair_ tair9/TAIR9_chr2.fas
#inCompressi  : 3.385643 sec
#SubseqPicker : 0.605587 sec

## fix for longer request
#./inCompressiTester tair8/chr2.fas 2 0 30500000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 0 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 0 1000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 11800000 7898289 tair/tair_ tair9/TAIR9_chr2.fas

# fixed -- added the needEncodedCharOnly=1 if the subseq. ends by an encoded char of some instru., also, a bug in adjusting subseqLength with length of chromosome
#./inCompressiTester tair8/chr2.fas 2 11800000 7898290 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr2.fas 2 18000000 2000000 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 0 0 tair/tair_ tair9/TAIR9_chr2.fas

#./inCompressiTester tair8/chr3.fas 3 13838000 700 tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 8981000 500 tair/tair_ tair9/TAIR9_chr4.fas

#./inCompressiTester tair8/chr3.fas 3 0 14000000 tair/tair_ tair9/TAIR9_chr3.fas

#./inCompressiTester tair8/chr3.fas 3 0 24000000 tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr3.fas 3 0 0 tair/tair_ tair9/TAIR9_chr3.fas

#./inCompressiTester tair8/chr4.fas 4 0 8985000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 8981000 100 tair/tair_ tair9/TAIR9_chr4.fas

#./inCompressiTester tair8/chr4.fas 4 0 19000000 tair/tair_ tair9/TAIR9_chr4.fas

#./inCompressiTester tair8/chr4.fas 4 15000000 500000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 16000000 1000000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 12000000 2000000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 8000000 5000000 tair/tair_ tair9/TAIR9_chr4.fas

#./inCompressiTester tair8/chr4.fas 4 8981000 100 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 0 0 tair/tair_ tair9/TAIR9_chr4.fas

#./inCompressiTester tair8/chr5.fas 5 0 28974700 tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr5.fas 5 0 30000000 tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr5.fas 5 0 0 tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr5.fas 5 13000000 1000000 tair/tair_ tair9/TAIR9_chr5.fas

################################ above are all ok #############################################


## complete decompression 
	## without seqpick testing the done decompression
#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 0 0 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 0 0 tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 0 0 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 0 0 tair/tair_ tair9/TAIR9_chr5.fas
	## using uncool: 
#time taken = 10.746567
	## using inCompressi

#time taken = 12.928869 = (((3.692348 + 1.880611 + 2.248443 + 1.989133 + 3.118334)))


#./inCompressiTester tair8/chr1.fas 1 10000000 10       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 10000000 100      tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 10000000 1000     tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 10000000 10000    tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 10000000 100000   tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 10000000 1000000  tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 10000000 10000000 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ tair9/TAIR9_chr1.fas
#==========================
#./inCompressiTester tair8/chr5.fas 5 0 5        tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 10       tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 50       tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 100      tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 500      tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 1000     tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 5000     tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 10000    tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 50000    tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 100000   tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 500000   tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 1000000  tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 5000000  tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 10000000 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 0        tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr5.fas 5 5000000 5       tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 5000000 50      tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 5000000 500     tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 5000000 5000    tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 5000000 50000   tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 5000000 500000  tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 5000000 5000000 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 0        tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr5.fas 5 10000000 5       tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 50      tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 500     tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 5000    tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 50000   tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 500000  tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 5000000 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 0        tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr5.fas 5 15000000 5       tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15000000 50      tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15000000 500     tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15000000 5000    tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15000000 50000   tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15000000 500000  tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15000000 5000000 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 0 0        tair/tair_ tair9/TAIR9_chr5.fas

#==========================


#./inCompressiTester tair8/chr4.fas 4 5000000 10       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 5000000 100      tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 5000000 1000     tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 5000000 10000    tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 5000000 100000   tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 5000000 1000000  tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 5000000 10000000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 0 0        tair/tair_ tair9/TAIR9_chr4.fas

#./inCompressiTester tair8/chr4.fas 4 15000000 10       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 100      tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 1000     tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 10000    tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 100000   tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 1000000  tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 10000000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr1.fas 1 0 0        tair/tair_ tair9/TAIR9_chr1.fas


#++++++++++++++++++
#./inCompressiTester tair8/chr4.fas 4 15000000 5        tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 10       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 50       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 100      tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 500      tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 1000     tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 5000     tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 10000    tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 50000    tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 100000   tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 500000   tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 1000000  tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 5000000  tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 15000000 10000000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 0 0        tair/tair_ tair9/TAIR9_chr4.fas

#+++++++++++++++++++++++++++++

#./inCompressiTester tair8/chr4.fas 4 10000000 500000        tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 10000000 1000000       tair/tair_ tair9/TAIR9_chr4.fas

#./inCompressiTester tair8/chr1.fas 1 0 5000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 0 5000000       tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 0 5000000       tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 0 10000000       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 0 10000000       tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 5000000 10000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 5000000 10000000       tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 5000000 10000000       tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 5000000 10000000       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 5000000 10000000       tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 10000000 10000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 10000000 10000000       tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 10000000 10000000       tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 10000000 10000000       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 10000000       tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 15000000 10000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr5.fas 5 15000000 10000000       tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 0 0        tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 0 0        tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr5.fas 5 0 0        tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 8760289 100 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 4479484 100 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 4479485 100 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 4479486 100 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 4479487 100 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 4479488 100 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 4479489 100 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 4479490 100 tair/tair_ tair9/TAIR9_chr1.fas

#./inCompressiTester tair8/chr4.fas 4 9672990 10000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 9672995 10000 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 9673000 10000 tair/tair_ tair9/TAIR9_chr4.fas


#./inCompressiTester tair8/chr1.fas 1 0 0        tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 0 0        tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 0 0        tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 0 0        tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 0 0        tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 0 0 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 0 0 tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 0 0 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 0 0 tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 10000000 2000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 10000000 2000000       tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 10000000 2000000       tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 10000000 2000000       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 2000000       tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 10000000 3000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 10000000 3000000       tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 10000000 3000000       tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 10000000 3000000       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 3000000       tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 10000000 4000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 10000000 4000000       tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 10000000 4000000       tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 10000000 4000000       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 4000000       tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester tair8/chr1.fas 1 10000000 5000000       tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 10000000 5000000       tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 10000000 5000000       tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 10000000 5000000       tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 10000000 5000000       tair/tair_ tair9/TAIR9_chr5.fas

#******************************************************************************

#./inCompressiTester tair8/chr1.fas 1 15000000 50000    tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 100000   tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 200000   tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 300000   tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 400000   tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 500000   tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 1000000  tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 5000000  tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 15000000 10000000 tair/tair_ tair9/TAIR9_chr1.fas

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ tair9/TAIR9_chr

#==========================********************************************** SEARCH
#==========================********************************************** SEARCH
#==========================********************************************** SEARCH
#==========================********************************************** SEARCH
#==========================********************************************** SEARCH

#./inCompressiTester tair8/chr1.fas 1 2804 10 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 3088 10 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 19878 10 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 30425440 10 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @GGCGT
# 6669 hits (with no overlapped blocks
# 6674 hits (i.e. more 5 hits overlapped between blocks)

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @
# 28 hits

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @GGCGTGTGGTT
# 2 hits
#./inCompressiTester tair8/chr1.fas 1 0 3000000 tair/tair_ @GGCGTGTGGTT
# first hit
#./inCompressiTester tair8/chr1.fas 1 3000000 10100000 tair/tair_ @GGCGTGTGGTT
# second hit

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @GGCGTGTGGTTAAGATGTTGCAAGAAATTGG
# 1 hit

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @GGCGTGTGGTT
# 2 hits [2073304, 10000038]
#./inCompressiTester tair8/chr2.fas 2 0 0 tair/tair_ @GGCGTGTGGTT
# 4 hits [4532206, 8577505, 8880275, 9210325]
#./inCompressiTester tair8/chr3.fas 3 0 0 tair/tair_ @GGCGTGTGGTT
# 2 hits [4381474, 12181214]
#./inCompressiTester tair8/chr4.fas 4 0 0 tair/tair_ @GGCGTGTGGTT
# 1 hits [585591]
#./inCompressiTester tair8/chr5.fas 5 0 0 tair/tair_ @GGCGTGTGGTT
# 3 hits [702359, 14320990, 22205307]

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAA
# 35 MB - 
# 879534 hits
# 879705 overlapped hits

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAAA
# 18 MB - 
# 324877 hits
# 324959 overlapped hits

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAAATTTT
# 8 MB - 
# 3979 hits
# 3980 overlapped hits

#./inCompressiTester tair8/chr1.fas 1 23158614 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 25067069 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 25170816 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAAATTTTCCCC
# 8 MB - 
# 3 hits [23158616, 25067071, 25170818]
# 3 overlapped hits

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAAATTTTCCCCAAAA
# 8 MB - 
# 1 hits
# 1 overlapped hits

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAATTTTCCCC
# 8 MB
# 8 overlapped hits

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAATTTTCCCCAAAA
# 8 MB
# 1 overlapped hits

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAAAAAA
# 8 MB
# 22418 overlapped hits
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAAA
# 8 MB
#Chromosome 1 - 22418 hits -> 
#Chromosome 2 - 14736 hits -> 
#Chromosome 3 - 17202 hits -> 
#Chromosome 4 - 13232 hits -> 
#Chromosome 5 - 19992 hits -> 
# 87580 overlapped hits

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAAACC
#Chromosome 1 - 640 hits -> 
#Chromosome 2 - 454 hits -> 
#Chromosome 3 - 558 hits -> 
#Chromosome 4 - 382 hits -> 
#Chromosome 5 - 685 hits -> 
# 2719 overall hits
# 1000 -> 1000000
# 7    - 7   - 9   - 27 MB
# 33.5 - 7.4 - 7.6 - 13.2 sec

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @ACGTACGT
#Chromosome 1 - 278 hits -> 
#Chromosome 2 - 178 hits -> 
#Chromosome 3 - 216 hits -> 
#Chromosome 4 - 197 hits -> 
#Chromosome 5 - 238 hits -> 
# 1107 overall hits
# 10000 -> 100000
# 7    - 9  MB
# 13.6 - 13.5 -  sec

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AACCGGTT
#Chromosome 1 - 683 hits -> 
#Chromosome 2 - 407 hits -> 
#Chromosome 3 - 502 hits -> 
#Chromosome 4 - 454 hits -> 
#Chromosome 5 - 662 hits -> 
# 2708 overall hits
# 7 MB
# 8.5  sec

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAACCCGGGTTT
#Chromosome 1 - 3 hits -> [1061791, 11468046, 20675696]
#Chromosome 2 - 4 hits -> [6442547, 7739463, 9915426, 15193105]
#Chromosome 3 - 1 hits -> [17548995]
#Chromosome 4 - 1 hits -> [15444888]
#Chromosome 5 - 5 hits -> [55415, 6951615, 9403854, 17806902, 18684836]
# 14 overall hits
# 7 MB
# 8.6  sec

# ensuring chromosome 1 offsets of AAACCCGGGTTT
#./inCompressiTester tair8/chr1.fas 1 1061788 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 11468043 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 20675693 20 tair/tair_ tair9/TAIR9_chr1.fas


#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAACCCGGGTTTAAACCCGGGTTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAACCCCGGGGTTTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @CCCCGGGGTTTTAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAATTTTTCCCCC
# 0 hits

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAATTTTT
# 409 hits

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTCCCCC
# 260 hits

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTCCCCCAAAAA
#./inCompressiTester tair8/chr1.fas 1 11370520 25 tair/tair_ tair9/TAIR9_chr1.fas
# 5 hits
#inCompressi  : 7463.219166 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCA
# 50 overall hits
# inCompressi  : 7278.847933 msec
# Memory Usage : 7 MB 


#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCAAAAAAAA
# 3 hits
#inCompressi  : 7776.840210 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr1.fas 1 11370520 30 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCAAAAAAAA----CAAAAA
#1 overall hits

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTT-----AAAAA
#Chromosome 1 - 1607 hits ->  [18261, 55750, 56115, 56224, 76798, 81513, 86416, 106811, 129455, 217863]
#Chromosome 2 - 1064 hits ->  [78742, 98912, 99278, 112558, 112767, 187163, 190455, 192192, 215580, 266309]
#Chromosome 3 - 1221 hits ->  [14798, 21384, 30656, 66242, 75935, 102600, 116806, 116847, 161791, 193758]
#Chromosome 4 - 942 hits ->  [2023, 7382, 32053, 115506, 119188, 157057, 166964, 167150, 209022, 257888]
#Chromosome 5 - 1339 hits ->  [13356, 17057, 37784, 75052, 76783, 116030, 142522, 162541, 179420, 183096]
# 6173 overall hits
### to ensure
#./inCompressiTester tair8/chr1.fas 1 18260 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 55749 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 56114 20 tair/tair_ tair9/TAIR9_chr1.fas
# TTTTT ----- AAAAA
# TTTTT TGAAT AAAAA GTAGT
# TTTTT TTAGA AAAAA ATACA
# TTTTT CCGCC AAAAA CACAA


#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTT----------AAAAA
#Chromosome 1 - 1416 hits ->  [2387, 81672, 82823, 102039, 103546, 104139, 107150, 129449, 141849, 146711]
#Chromosome 2 - 948 hits ->  [70737, 144862, 169550, 170527, 205513, 240950, 241145, 298140, 352855, 370123]
#Chromosome 3 - 1147 hits ->  [14794, 30656, 66241, 75935, 79327, 84342, 89648, 116187, 116806, 117218]
#Chromosome 4 - 860 hits ->  [3313, 32049, 68981, 79811, 157054, 159893, 200310, 248563, 258081, 279622]
#Chromosome 5 - 1288 hits ->  [17580, 22392, 53812, 56843, 78864, 95927, 146599, 176495, 251450, 260710]
# 5659 overall hits
### to ensure
#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @TTTTT----------AAAAA
#1416 hits ->  [2387, 81672, 82823, 102039, 103546] [30338091, 30354882, 30357985, 30361255, 30371801]
### to ensure
#./inCompressiTester tair8/chr1.fas 1 30338090 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 30361254 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 103545 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 2386 20 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 30371800 20 tair/tair_ tair9/TAIR9_chr1.fas
# TTTTT ---------- AAAAA
# TTTTT GTATGTTCAT AAAAA
# TTTTT CTCCAGAAAC AAAAA
# TTTTT GGCATTCAAG AAAAA

## new interleaved matches results
#Chromosome 1 - 1824 hits ->  [2387, 81672, 82823, 102039, 103546, 104139, 107150, 129449, 141849, 141850]
#Chromosome 2 - 1225 hits ->  [70737, 144862, 169550, 169551, 170527, 205513, 240950, 241145, 298140, 298141]
#Chromosome 3 - 1486 hits ->  [14794, 14795, 14796, 14797, 30656, 66241, 75935, 79327, 84342, 89648]
#Chromosome 4 - 1111 hits ->  [3313, 32049, 68981, 79811, 157054, 157055, 159893, 200310, 248563, 258081]
#Chromosome 5 - 1664 hits ->  [17580, 17581, 22392, 53812, 56843, 78864, 78865, 78866, 95927, 146599]
#7310 overall hits
 #inCompressi  : 9023.990154 msec

#========================================== increment pattern length
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCAAAAAAAACAAACAAAAA
#./inCompressiTester tair8/chr1.fas 1 11370520 30 tair/tair_ tair9/TAIR9_chr1.fas
# 1 overall hits
# inCompressi  : 7583.584070 msec
# Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCAAAAAAAA-----AAAAA
#1 overall hits
#inCompressi  : 7439.821005 msec

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTT----------------TTT
#Chromosome 1 - 82497 hits ->  [438, 682, 715, 740, 1158, 1329, 1840, 2135, 2284, 2285]
#Chromosome 2 - 53443 hits ->  [2043, 2627, 2937, 3645, 14566, 17795, 21264, 25725, 38309, 42062]
#Chromosome 3 - 59842 hits ->  [483, 484, 500, 501, 745, 920, 1187, 1379, 1557, 2247]
#Chromosome 4 - 48431 hits ->  [1750, 2498, 3379, 3486, 3487, 3488, 3505, 3506, 3507, 4395]
#Chromosome 5 - 72840 hits ->  [255, 262, 363, 364, 370, 615, 934, 953, 960, 1004]
#317053 overall hits
#inCompressi  : 13502.798796 msec - 13254.390955 msec
#Memory Usage : 11 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTT----------------TTTTT
#Chromosome 1 - 3012 hits ->  [1156, 21879, 43060, 61033, 61034, 88749, 120991, 120992, 120993, 140271]
#Chromosome 2 - 2010 hits ->  [56226, 56227, 56228, 56229, 56230, 56231, 70355, 77786, 106277, 150552]
#Chromosome 3 - 2366 hits ->  [11282, 18815, 18816, 18817, 42322, 74290, 116785, 133064, 135924, 141083]
#Chromosome 4 - 1839 hits ->  [38212, 40151, 46552, 67645, 72420, 78242, 132190, 154053, 157801, 157802]
#Chromosome 5 - 2777 hits ->  [16800, 26370, 27982, 28344, 56915, 56916, 56917, 56918, 56919, 56937]
#12004 overall hits
#inCompressi  : 8820.011854 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTT----------------TTTTTTT
#1307 overall hits
#inCompressi  : 8040.972948 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTT----------------TTTTTTTT
## distinct
#269 overall hits
#inCompressi  : 7793.201923 msec
#Memory Usage : 8 MB 
## overlapped
#612 overall hits
#inCompressi  : 7752.274990 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTTTT----------------TTTTTTTTTT
## not
#58 overall hits
#inCompressi  : 7499.592066 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTTTT--------------------TTTTTTTTTT
## not, 10-20-10
#37 overall hits
#inCompressi  : 7411.091805 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTTTT------------------------------TTTTTTTTTT
## not, 10-30-10
#Chromosome 1 - 5 hits ->  [575029, 11575837, 19559753, 22935448, 23128596]
#Chromosome 2 - 7 hits ->  [5598369, 8277177, 8733587, 10493631, 11160993, 11754253, 16568924]
#Chromosome 3 - 7 hits ->  [1210902, 6620124, 19383196, 19569654, 19858379, 23165894, 23175019]
#Chromosome 4 - 12 hits ->  [595255, 3739180, 4577190, 4578145, 4580605, 4581560, 4584955, 5495657, 8644883, 8763860]
#Chromosome 5 - 6 hits ->  [8538379, 15877043, 19769882, 21846886, 23313056, 24702605]
#37 overall hits
#inCompressi  : 7410.336971 msec
#Memory Usage : 7 MB 
################################################# testings
#./inCompressiTester tair8/chr1.fas 1 23128592 55 tair/tair_ tair9/TAIR9_chr1.fas
#GAT TTTTTTTTTT TAAATATATCTTGAAAAATGATTCTAAAGC TTTTTTTTTT TT
#./inCompressiTester tair8/chr3.fas 3 19858375 55 tair/tair_ tair9/TAIR9_chr3.fas
#AAC TTTTTTTTTT GGTATCAAGTTTTTTTATGAACTTTTTTTT TTTTTTTTTT GA
#./inCompressiTester tair8/chr5.fas 5 23313052 55 tair/tair_ tair9/TAIR9_chr5.fas
#AAC TTTTTTTTTT TTTTTTTTATGTTATAAAACTTGTTCTTCT TTTTTTTTTT TT

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTTTTTT------------------------------TTTTTTTTTTTT
## not, 12-30-12
#6 overall hits
#inCompressi  : 7297.639132 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTTTTTTT------------------------------TTTTTTTTTTTTT
## not, 13-30-13
#Chromosome 1 - 0 hits ->  []
#Chromosome 2 - 1 hits ->  [16568922]
#Chromosome 3 - 1 hits ->  [23175016]
#Chromosome 4 - 0 hits ->  []
#Chromosome 5 - 1 hits ->  [15877081]
#3 overall hits
#inCompressi  : 7314.155102 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr3.fas 3 23175011 62 tair/tair_ tair9/TAIR9_chr3.fas
#TTTT TTTTTTTTTTTTT TAATCTTTTTGTTTCTCTAGTGCTTGACTC TTTTTTTTTTTTT TT
#./inCompressiTester tair8/chr5.fas 5 15877076 60 tair/tair_ tair9/TAIR9_chr5.fas
#GTTC TTTTTTTTTTTTT TTTTACAATATAGTTCATTCAAGTTCTTTT TTTTTTTTTTTTT

###########./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTTTTTTTT------------------------------TTTTTTTTTTTTTT
# not, 14+30+14
#1 overall hits -- chr3
# overlapped
# 2 overall hits -- chr3

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAA
## not
#3430611 overall hits
#inCompressi  : 9517.647028 msec
#Memory Usage : 58 MB notification+a00fojj6@facebookmail.com
## overlap
#5250463 overall hits
#inCompressi  : 10884.494066 msec
#Memory Usage : 85 MB
#### testing
#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAA

#./inCompressiTester tair8/chr3.fas 3 0 23175150 tair/tair_ @TTTTTTTTTTTTTT------------------------------TTTTTTTTTTTTTT
# not, 14+30+14
#1 overall hits -- chr3
# overlapped
# 2 overall hits -- chr3

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTTTTTTTTT--TTTTTTTTTTTTTT
#339 overall hits
#inCompressi  : 7299.577951 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AA
## distinct 13 sec 154 mb		> genome size
## overlapped 16 sec 209 mb
########### down to 8 mb if dumping indexes into file, and time down by 3 sec if no indeces kept, but time grows to 24 or 41 sec if dumped to file


#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AA
#3519618 hits ->  [5, 6, 12, 13, 19] [30427584, 30427585, 30427589, 30427590, 30427611]
#inCompressi  : 4317.563057 msec
#Memory Usage : 119 MB 
####### using dumping of indexes, time down by 1 sec, to 8 mb

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAAAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAAAAAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAAAAAAAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAAAAAAAAAAAAA

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCA

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AACCGGTT---AACCGGTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AACCGGTT-----AACCGGTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AACCGGTT----------AACCGGTT
# 1 HIT
## testing
#./inCompressiTester tair8/chr2.fas 2 15042140 30 tair/tair_ tair9/TAIR9_chr2.fas	--> TTG
#./inCompressiTester tair8/chr2.fas 2 12042835 30 tair/tair_ tair9/TAIR9_chr2.fas	--> TTTTA
#./inCompressiTester tair8/chr5.fas 5 21618410 40 tair/tair_ tair9/TAIR9_chr5.fas	#--> TCTCCTCAAT

#./inCompressiTester tair8/chr1.fas 1 10000000 5000000       tair/tair_ tair9/TAIR9_chr1.fas

################################################################################################## searching by multiple patterns

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAAAATTTTT
#98 hits ->  [687532, 792245, 822082, 1545883, 1884154] [27022245, 28333907, 28471600, 28568027, 29856239]
#inCompressi  : 1902.070999 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @AAAAATTTTT,TTTTTCCCCC
#98 hits ->  [687532, 792245, 822082, 1545883, 1884154] [27022245, 28333907, 28471600, 28568027, 29856239]
#67 hits ->  [142373, 390575, 470727, 491126, 560747] [29306068, 29307445, 29903849, 30217069, 30225664]
#inCompressi  : 1963.600874 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @GGCGTGTGGTTAAGATGTTGCAAGAAATTGG,AAAATTTTCCCC,ACGTACGT,AAACCCGGGTTT,TTTTTCCCCC
#1 hits ->  [10000038] [10000038]
#3 hits ->  [23158616, 25067071, 25170818] [23158616, 25067071, 25170818]
#283 hits ->  [19830, 175104, 207911, 371669, 927986] [30034731, 30035497, 30035996, 30127741, 30348516]
#3 hits ->  [1061791, 11468046, 20675696] [1061791, 11468046, 20675696]
#67 hits ->  [142373, 390575, 470727, 491126, 560747] [29306068, 29307445, 29903849, 30217069, 30225664]
#inCompressi  : 2820.693016 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr1.fas 1 0 0 tair/tair_ @TTTTTTCCCCCA,GGCGTGTGG,GGCGTGTGGTT,GGCGTGTGGTTAAGATGTTGCAAGAAATTGG,AAAATTTTCCCC,ACGTACGT,AAACCCGGGTTT,TTTTTCCCCC,TTTTTTCCCCCAAAAAAAA,TTTTTTTTTTTTTT--TTTTTTTTTTTTTT
#17 hits ->  [142372, 1231774, 1408110, 1844011, 1901508] [18451976, 21088950, 22462922, 29307444, 30225663]
#29 hits ->  [1800791, 2073304, 3680320, 4137768, 5868013] [28101284, 28767548, 29398989, 30011028, 30043363]
#2 hits ->  [2073304, 10000038] [2073304, 10000038]
#1 hits ->  [10000038] [10000038]
#3 hits ->  [23158616, 25067071, 25170818] [23158616, 25067071, 25170818]
#283 hits ->  [19830, 175104, 207911, 371669, 927986] [30034731, 30035497, 30035996, 30127741, 30348516]
#3 hits ->  [1061791, 11468046, 20675696] [1061791, 11468046, 20675696]
#67 hits ->  [142373, 390575, 470727, 491126, 560747] [29306068, 29307445, 29903849, 30217069, 30225664]
#1 hits ->  [11370522] [11370522]
#0 hits ->  [] []
#inCompressi  : 3167.365074 msec
#Memory Usage : 7 MB 

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCA,GGCGTGTGG,GGCGTGTGGTT,GGCGTGTGGTTAAGATGTTGCAAGAAATTGG,AAAATTTTCCCC,ACGTACGT,AAACCCGGGTTT,TTTTTCCCCC,TTTTTTCCCCCAAAAAAAA,TTTTTTTTTTTTTT--TTTTTTTTTTTTTT
#AAAATTTTCCCC : 8 overall hits ->
#  first 5 hits:  ['CHR1->', 23158616, 25067071, 25170818, 'CHR2->'] last 5 hits:  [8535856, 'CHR5->', 2905912, 4600751, 26605669]
#AAACCCGGGTTT : 14 overall hits ->
#  first 5 hits:  ['CHR1->', 1061791, 11468046, 20675696, 'CHR2->'] last 5 hits:  [55415, 6951615, 9403854, 17806902, 18684836]
#TTTTTTCCCCCAAAAAAAA : 3 overall hits ->
#  first 5 hits:  ['CHR1->', 11370522, 'CHR2->', 'CHR3->', 8186987] last 5 hits:  ['CHR3->', 8186987, 'CHR4->', 8808391, 'CHR5->']
#inCompressi  : 12392.393827 msec
#Memory Usage : 7 MB 

#==========================********************************************** SEARCH
#==========================********************************************** SEARCH
#==========================********************************************** SEARCH

#==========================********************************************** DECOMPRESSION VS. SEARCH
#==========================********************************************** DECOMPRESSION VS. SEARCH
#==========================********************************************** DECOMPRESSION VS. SEARCH

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ tair9/TAIR9_chr
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ tair9/TAIR9_chr
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ tair9/TAIR9_chr

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAAATTTTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTCCCCC
# 7.4 sec
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTT----------------TTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTT----------------TTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTT----------------TTT

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTT-----AAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTT-----AAAAA
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTT-----AAAAA

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTTCCCCCAAAAAAAA-----AAAAA

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAACCCGGGTTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAACCCGGGTTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAACCCGGGTTT

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @ACGTACGT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @ACGTACGT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @ACGTACGT

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @ACGT---ACGT

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AACCGGTT

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TATAT-----CGCGC
# new incomplete 7907

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @AAAA

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTCCCCC,ACGTACGT,AACCGGTT,AAACCCGGGTTT,AAAA,ACGT---ACGT,TATAT-----CGCGC,TTTTT-----AAAAA,TTT----------------TTT
#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TTTTTCCCCC,ACGTACGT,AACCGGTT,AAACCCGGGTTT,AAAA

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ @TGCGA---ACGCT
# 15 hits
#./inCompressiTester tair8/chr1.fas 1 17531395 13 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr1.fas 1 29972471 13 tair/tair_ tair9/TAIR9_chr1.fas
#./inCompressiTester tair8/chr2.fas 2 8406310 13 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr2.fas 2 9116713 13 tair/tair_ tair9/TAIR9_chr2.fas
#./inCompressiTester tair8/chr3.fas 3 10735230 13 tair/tair_ tair9/TAIR9_chr3.fas
#./inCompressiTester tair8/chr4.fas 4 2574159 13 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr4.fas 4 11956656 13 tair/tair_ tair9/TAIR9_chr4.fas
#./inCompressiTester tair8/chr5.fas 5 1961615 13 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 1970333 13 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 10169321 13 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 13335108 13 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15068649 13 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 15708289 13 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 17422226 13 tair/tair_ tair9/TAIR9_chr5.fas
#./inCompressiTester tair8/chr5.fas 5 24440860 13 tair/tair_ tair9/TAIR9_chr5.fas


#==========================********************************************** DECOMPRESSION VS. SEARCH
#==========================********************************************** DECOMPRESSION VS. SEARCH
#==========================********************************************** DECOMPRESSION VS. SEARCH


#./inCompressiTester r_hg18/chr1.fa 1 0 0 homo/homo_ t_yh/chr1.fa
#./inCompressiTester r_hg18/chr1.fa 1 100000000 10000000 homo/homo_ t_yh/chr1.fa
#./inCompressiTester r_hg18/chr1.fa 1 100000000 20000000 homo/homo_ t_yh/chr1.fa
#./inCompressiTester r_hg18/chr1.fa 1 100000000 2000 homo/homo_ t_yh/chr1.fa

#./inCompressiTester r_hg18/chr1.fa 1 100000000 200 homo/homo_ t_yh/chr1.fa
#./inCompressiTester r_hg18/chr1.fa 1 100000010 10 homo/homo_ t_yh/chr1.fa
# 554 mb 66 sec

#./inCompressiTester r_hg18/chr7.fa 7 0 0 homo/homo_ t_yh/chr7.fa

#./inCompressiTester r_hg18/chr7.fa 1 16840180 50 homo/homo_ t_yh/chr7.fa
#./inCompressiTester r_hg18/chr7.fa 1 16840199 50 homo/homo_ t_yh/chr7.fa
#./inCompressiTester r_hg18/chr7.fa 1 16840200 50 homo/homo_ t_yh/chr7.fa
#./inCompressiTester r_hg18/chr7.fa 1 16840240 50 homo/homo_ t_yh/chr7.fa
#./inCompressiTester r_hg18/chr7.fa 1 16840280 50 homo/homo_ t_yh/chr7.fa
#./inCompressiTester r_hg18/chr7.fa 1 16840320 50 homo/homo_ t_yh/chr7.fa
#./inCompressiTester r_hg18/chr7.fa 7 16830201 10000 homo/homo_ t_yh/chr7.fa

#./inCompressiTester r_hg18/chr7.fa 1 79330831 23731 homo/homo_ t_yh/chr7.fa
#./inCompressiTester r_hg18/chr7.fa 1 79330831 10000 homo/homo_ t_yh/chr7.fa

#./inCompressiTester r_hg18/chr2.fa 2 79073689 7592 homo/homo_ t_yh/chr2.fa

#./inCompressiTester r_hg18/chr1.fa 1 909985 10000 homo/homo_ t_yh/chr1.fa

#./inCompressiTester tair8/chr -1 0 0 tair/tair_ tair9/TAIR9_chr

#./inCompressiTester tair8/chr5.fas 5 0 0 tair/tair_ tair9/TAIR9_chr5.fas

#./inCompressiTester r_hg18/chr5.fa 5 168592744 4578 homo/homo_ t_yh/chr5.fa
#./inCompressiTester r_hg18/chr6.fa 6 125189929 10981 homo/homo_ t_yh/chr6.fa

#./inCompressiTester r_hg18/chr1.fa 1 0 0 homo/homo_ @AAAAA----------TTTTT
#5743 hits ->  [23371, 108063, 134757, 158709, 254380] [246776288, 246847113, 246907846, 246948111, 247154070]
#inCompressi  : 1198387.793064 msec - Memory Usage : 88 MB 


#final bugs fixed:
#=================
# if(adjusted > 0) --> was preventing from adjustment of remaining if dels > inss in the extracted seq. incompressi
# fixing problem of seq check with instru.s				incompressi
# fixing problem of requesting bigger sequence than chromosome end
# chromoLen-1/pairsPerLine --> should put () for chromoLen-1 to prevent the division priority	uncool-seq-mem
# order of ins.s before dels. in getting fakeSeqOffset: subtract ins.s from Lseq before adding dels.
# attempted: shrinking the last search block if it will come with chars in offsets greater than the required length

# XXXXX 12.17+12.06+12.06+15.25+17.65+17.76+18+12.03+12+12.03+12.24+12+12 = 13.63
# XXXXXX 12.14+12.12+15.09+18+18+18.25+17.87+18.39+17.84+17.96 = 16.57
# 12.20+12.47+12.67+12.26+12.18+12.20+12.16+12.25+12.18+12.45 = 12.30

#mplayer alarm.mp3

