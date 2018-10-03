from __future__ import division
from ch6 import *
import numpy

def reverseComplement(string):
	myStr = []
	for i in range(0, len(string)):
		if string[i] == 'A':
			myStr.append('T')
		elif string[i] == 'T':
			myStr.append('A')
		elif string[i] == 'G':
			myStr.append('C')
		elif string[i] == 'C':
			myStr.append('G')

	myStr = myStr[::-1]
	myStr = "".join(myStr)
	return myStr

def hammingDistance(genome1, genome2):
	hd = 0
	if len(genome1) == len(genome2):
		for i in range (0, len(genome1)):
			if genome1[i]!=genome2[i]:
				hd +=1
	return hd
def appxPatternCount(pattern, genome, d):
	a = []
	for i in range(0, (len(genome) - len(pattern) + 1)): 
		if(hammingDistance(genome[i:i+len(pattern)], pattern) <= d):
			a.append(str(i))
	return len(a)

def suffix(pattern):
	return pattern[1: ]
def firstSymbol(pattern):
	return pattern[0]

#d = 1
def immediateNeighbours(pattern):
	neighborhood = []
	neighborhood.append(pattern)
	bases = ['A', 'T', 'G', 'C']
	for i in range(0, len(pattern)):
		symbol = pattern[i]
		for j in range(0, len(bases)):
			if bases[j]!=symbol:
				pattern = list(pattern)
				pattern[i] = bases[j]
				pattern = ''.join(pattern)
				print pattern
				neighborhood.append(pattern)
				pattern = list(pattern)
				pattern[i] = symbol
				pattern = ''.join(pattern)
				print pattern
	return neighborhood

def neighbors(pattern, d):
	bases = ['A', 'T', 'G', 'C']
	if d == 0:
		return pattern
	if len(pattern) == 1:
		return bases
	neighborhood = []
	suffixNeighbors = neighbors(suffix(pattern), d)
	for text in suffixNeighbors:
		if hammingDistance(suffix(pattern), text) < d:
			for j in bases:
				neighborhood.append(j + text)
		else:
			neighborhood.append(firstSymbol(pattern) + text)

	return neighborhood

def iterativeNeighbors(pattern, d): #not working --> infinite loop
	neighborhood = ['A', 'T', 'G', 'C']
	for j in range(1, d+1):
		for pattern_ in neighborhood:
			x = immediateNeighbours(pattern_)
			for k in x:
				neighborhood.append(k)
	return neighborhood

def FrequentWordsWithMismatchesSorting(text, k, d):
	frequentPatterns = []
	neighborhood = []
	index = []
	count = []
	for i in range(0, len(text) - k + 1):
		n = neighbors(text[i:i+k], d)
		for j in range(0, len(n)):
			neighborhood.append(n[j])
		n = []

	neighborhoodArray = neighborhood
	for i in range(0, len(neighborhood)):
		pattern = neighborhoodArray[i]
		index.append(RecursivePatternToNumber(pattern))
		count.append(1)
	index.sort()
	for i in range(0, len(neighborhood) - 1):
		if index[i] == index[i+1]:
			count[i+1] = count[i] + 1
	maxCount = max(count)
	for i in range(0, len(neighborhood)):
		if count[i] == maxCount:
			pattern = RecursiveNumberToPattern(index[i], k)
			frequentPatterns.append(pattern)
	return frequentPatterns

def FrequentWordsWithMismatchesAndReverseComplement(text, k, d):
	rtext = reverseComplement(text)
	frequencyArray = []
	for i in range(0, 4**k):
		frequencyArray.append(0)
	for i in range(0, len(text) - k + 1):
		pattern = text[i: i+k]
		neighborhood = neighbors(pattern, d)
		for appxPattern in neighborhood:
			j = RecursivePatternToNumber(appxPattern)
			frequencyArray[j] += 1
	for i in range(0, len(rtext) - k + 1):
		pattern = rtext[i:i+k]
		neighborhood = neighbors(pattern,d)
		for appxPattern in neighborhood:
			j = RecursivePatternToNumber(appxPattern)
			frequencyArray[j] += 1

	frequentPatterns = []
	maxCount = max(frequencyArray)
	for i in range(0, len(frequencyArray)):
		if frequencyArray[i] == maxCount:
			frequentPatterns.append(RecursiveNumberToPattern(i, k))
	return frequentPatterns
	

def computingFrequenciesWithMismatches(text, k , d):
	frequencyArray = []
	for i in range(0, 4**k):
		frequencyArray.append(0)
	for i in range(0, len(text) - k + 1):
		pattern = text[i: i+k]
		neighborhood = neighbors(pattern, d)
		for appxPattern in neighborhood:
			j = RecursivePatternToNumber(appxPattern)
			frequencyArray[j] += 1
	frequentPatterns = []
	maxCount = max(frequencyArray)
	for i in range(0, len(frequencyArray)):
		if frequencyArray[i] == maxCount:
			frequentPatterns.append(RecursiveNumberToPattern(i, k))
	return frequentPatterns
	
def MotifEnumeration(dna, k, d):
	pattern = []
	neighborhood = []
	for dna_ in dna:
		myneigh = []
		for i in range(0, len(dna_) - k + 1):
			n = neighbors(dna_[i:i+k], d)
			for j in n:
				if j not in myneigh:
					myneigh.append(j)
		neighborhood.append(myneigh)

	pattern =  list(set(neighborhood[0]).intersection(*neighborhood))
	return pattern

def DistanceBetweenPatternAndStrings(pattern, dna):
	k = len(pattern)
	distance = 0
	for dna_ in dna:
		hd = 9999999
		for i in range(0, len(dna_) - k + 1):
			pattern_ = dna_[i:i+k]
			if hd > hammingDistance(pattern, pattern_):
				hd = hammingDistance(pattern, pattern_)
		distance += hd
	return distance

def MedianString(dna, k):
	distance = 9999999
	median = ''
	for i in range(0, 4**k):
		pattern = RecursiveNumberToPattern(i, k)
		if distance > DistanceBetweenPatternAndStrings(pattern, dna):
			distance = DistanceBetweenPatternAndStrings(pattern, dna)
			median = pattern
	return median

def ProfileMostProbable(text, k ,profile_mat):
	#profile mat is a dictionary
	probs = []
	kmers = []
	for i in range(0, len(text) - k + 1):
		pattern = text[i:i+k]
		prob = 1
		for j in range(0, len(pattern)):
			if pattern[j] == 'A':
				prob *= profile_mat['A'][j]
			elif pattern[j] == 'C':
				prob *= profile_mat['C'][j]
			elif pattern[j] == 'G':
				prob *= profile_mat['G'][j]
			elif pattern[j] == 'T':
				prob *= profile_mat['T'][j]

		probs.append(prob)
		kmers.append(pattern)
	most_prob = ''
	max_prob = max(probs)
	for i in range(0, len(kmers)):
		if probs[i] == max_prob:
			most_prob = kmers[i]
			break
	return most_prob

def ProfileMatrixFromMotifs(motifs):
	profile_mat = {}
	profile_mat = {'A': [], 'C': [],'G': [], 'T': []}
	bases = ['A','C', 'G','T']
	for key in profile_mat.keys():
		for i in range(0, len(motifs[0])):
			profile_mat[key].append(0)
	for i in range(0, len(motifs)):
		mymotif = motifs[i]
		for j in range(0, len(mymotif)):
			if mymotif[j] == 'A':
				profile_mat['A'][j] += 1			
			elif mymotif[j] == 'C':
				profile_mat['C'][j] += 1
			elif mymotif[j] == 'G':
				profile_mat['G'][j] += 1
			elif mymotif[j] == 'T':
				profile_mat['T'][j] += 1
	for key in profile_mat.keys():
		l = profile_mat[key]
		for i in range(0, len(l)):
			l[i] /= len(motifs[0])
	return profile_mat

def score(motifs):
	profile = ProfileMatrixFromMotifs(motifs)
	consensus = []
	for i in range(0, len(motifs[0])):
		m = profile['A'][i]
		let = 'A'
		if profile['C'][i] > m:
			let = 'C'
			m = profile['C'][i]
		if profile['G'][i] > m:
			let = 'G'
			m = profile['G'][i]
		if profile['T'][i] > m:
			let = 'T'
			m = profile['T'][i]
		consensus.append(let)
	consensus = ''.join(consensus)
	score = 0
	for i in range(0, len(motifs)):
		score += hammingDistance(motifs[i],consensus)
	return score

def GreedyMotifSearch(dna, k, t):
	best_motifs = []
	best_score = 999999
	for i in range(0, len(dna[0]) - k + 1):
		motifs = []
		motifs.append(dna[0][i:i+k])
		for j in range(1,t):
			profile = ProfileMatrixFromMotifs(motifs)
			mymotif = ProfileMostProbable(dna[j], k, profile)
			motifs.append(mymotif)
		current_score = score(motifs)
		if current_score < best_score:
			best_score = current_score
			best_motifs = motifs

	return best_motifs


k = 12
t = 25
dna = 'AAACCCTACCATTATGGTTACCTCAGCAGGGTCTGGGAAGCACTTGCTTCGATTCCGTGTTCAACCCAGAGAAAGCCAACTTTTCACTTGTAATTAGGAATAATGGCTTTTAACTGTATAATGGCACTTAGGTTATTAGCCCAAGCCGATTGTCTA TTTCTCCGTAATAGTAACAAGCCATAGAAACTTTCGCGAGGCTGACCGGATACGAGTACTTCATCCGTGAGCTAGAGATTAGATTGTGGTTCCAGCCTCAATTGGTGCCATACAAGAACACAGGACAGCCGGTGCTAGCCGGCGTTAACTTATTTT CTTAAATCACGGATACCTGGTGCATTCGCCCTAGGCTTGGCGACGTTTCCCAGGAAGACTATTGTGTCACCAATGAGTTCACAGATCGAAGGAGGTTTGAATATAGCATCAACTACCACTCTTTTCGTTGCGACTTTAAAACCATCAACCAAGAGA ACGCGGCACGTCAGCGTTGTACAGCCCCCGCCTCTTCTTGAGAAGGCATATGAAGCTTGACTGTCTGTGTGGACGCGCTTAGCGCCGGACGTGGAGGAAGCGCCTCCTCCAGTTGGATAGCGCAAGACAGAGTCAGCCCGGAGTGAACAATACGAC CCGTCCGATTGACGCGCTTGGACGTCATTTCACTCAATAAGGGATAAGCTGGTGCCACTATCATCCCCGAGCTTCTAAATTTGCAGACACGCCACCATCGTATGGGGGAGTGTATCGTATCTCAAGATGTAGCAGTCAAAAGGCCATGCACATGTC CAGAGGGCGGCGTGTGCGAGATAATTGGTGGGCAACTTGACCCGCGTCGACAATCGAACAGTCTGTCGTAGCTCTCATCGAGTAATTCGTCAAGCTGCATTTATTTATAATTGCTTCTCCTCAACCGAGAGTCGAACGCCTAGGGACTGCGATTAG TCAACCAAGAGTAATGATGTCAACGCGCCCCTAAATCTAAATTGTCCATGTGCTCCACCGGGACAAATGAAGCAACCCTGACATGGAGCATAGACAAGTCCCCTAAGGACTGTCCTGTGGTTCATCCGTGCCATGCAGTTCTGTGACAACTGGACC AATTCCGTACACCCGCGGTTATTTTTATAACTACTAGTCTGCACGCATGGCAGTTGGTATTCAACCCGGAGTTTCCCGGGTGTGGAGCCTATTGCAATACCAGCTTATTCGTGACGGAAGCAGCAATTACCCGCATGCCCGAACCGAAGATCACAT CATGCGACCACGCTGAACATCGGGACGTCCATATGGATAAGCGCGTAACCGACGTACGGCTCCGATCTCTGGATAGCCATTGGCTTGAGAGCTGGTAATAGCAAGCAGTCACCCAAGAGACCGTGAATCGCTGTGCCCTATTTTATGTGCCCTTAA AGAATCTCCTCTCGTAGATAACAGGTGCGATGTACTTCAACCTAGAGCCCACCATGTTTGGCCTGTCACACGTGGCCAGCGCGCGTATCTAGCCGATCTCCAATTGCGCTATTCGCCGCAAATGGCTGGAAGCGGGTCCTCTGTGGCCTTAGTACT CAGCCCTAAGAGCGCCGGCCGTAAAAACAATAGATGTCACCCCCGAGAGTACAGGCCTTCCAGTAGTGGCTATCACTAACAAACCAGCTATGCCCAAAACAGTTAATCCATTGATTTAGATTGATGGACTTCGGCTCTTCAGGGATCGCGAAATGT ACAATACTTGAAGCCAGGTACTAATCAGCCCCGAGCATGTAGCCGACGACTACACGTGCACACGAAGTTCGATGCTGCCCGGGACTACGGGCTAACTATGTGAAGGTTTGCTGAACGGCAGGTGAGGCTATTGTAATTATGCGCCTCAGAGCTAGA CGAGGTGCCGGAATTAAACCTACAGATTGATGTGGTATCCGTGGGAAGGGACTGTGTTAATCAGCCCAGAGGTGAAACGAAAATGCCGTTATTAGTTGGACGGCTGAGTGGGACGCCAGTTATCGACTCTCTCGTCCAGATCCGATTGGGCTCAAA CGACTATATACAATCGATACGTTCCTACATACTCGCGTGTGTTTTCACTCAGCCTCGAGGCTATTGCTGGCTTAGGCTCCCCCTGAGGCGGTCCGGCTGTCACAGAGGTTGTTAACTGGGCGAGTACATTGCTTTATCACAGTTTGATCACTCCGA AAAATATCCTATAGCTTGAAAGGAGCCGACAGACATGTGGTTTGTAAATCAGCCACGAGTCTTTACCTCTTAAACGAATTGACGACGCCCGTCATTACATCTATATCGCTCAACCACATGATCACTGAGCCCTGGGTAACTCAGTTTAAATAAAGA GTGTTATTGCGTCCTGCGACGGCGAGAAACTGCGGTTGTTTGCCACGATACAATACGATCGGGTTCAGCCTGCGTTATAGAGGAGCCAAAAAGGCCCGTATGTGACGTCCCCGCGATCAAGGGTTTTCACGAGGCAGTTAACATTCACCCATGAGT CCACGCTCACACTGCAGCCGAGATTTCCAGTAACCATGCCCTTGCATCCCCGACGGAAAGGCAGGTACTTTTCCACTTTGCTAGCTGCGCTTGACGCCCCCTTTTCGGGAGTCCAGAGACTCTTCACTAGACATTAGGAATATATCACCCTAGAGT TCAGATTGAGTACTCTACTCCGTCTCATCCACGAGGCGAGTATGTTCAAATCGCGGTCAATCCGCCACGAAAGGTTATTTGGTGCTACTTGTCTTGAGTGCGACGTTAGGTGAGTCGTCGCGCGACCCCGGGTGTAGTCGGGAACAACGCGTCGTA TATTTCCCGGACTGTTTAGGTTATAGGTCACGTTGCGCAGTACGATCGCAACCCCCGATTGCCGGTTCTTGTTGTCTCTGGGATCGACGATACGCGCATACAGACAACCAAAACACCAGCTCACCCATGAGGGAGCTAGCCTGTAAGAAGGGGTCC TACCGGTAGGTCAATCGGGTCACCGGACGATTGTCACATAACACACTTTATAGGGTCCCAAAGTAGGACATATCAGCCTGGAGAAAGACGCAGCGACAGCGTCACATAAGCGAAAAGTACTCAAACGCCCGAATTGCTAGATCTGGATCCATCAAC GTGGTTTATGATGCACCTGTCAGGTCAGAAGGTCACTCTACCCTATTTGCACCATCCCTGTCAACCGCGAGGCCAGTACATCGGCAAGCACGCCAATTAATCTCTGAGACAAAGTGGGTCAGATGAGTGTCGCGTGGGGTTAGCTCTGTTCATCTA TCAGCCCCGAGTACACCCGACGGGAGCGCCCTAGTATGAACGCGATTAATACCGCGGCGGAGACTAGCACTGCCATCCCTCGGGGGGCCACCGGGCCGTGCGATCATAATCTCGTCTTGGACAAGGCCCGGCCCCCAATCTGGTTTTCCACCAGCA CTTGGTCTCACGCTACTACAATTGAGGTGTTCCTGCGCCTGATCCCGGCTGCGAGCTCAGTCAGCCAAGAGAGTATTTCAAGCAGGTGAAACAACGGGAGTGAATAATGATTCTGCTGAGACTATTTCTACATATCGTCTTCTGCTCGACACTGGA CACGGCTAAGCTTTCATGGTTGGGTTGTTATGTGAAATAAAAGCTATCCCCATGGCTTATGTCCTATACTCTCCCACCCTATGGGATCGCCGTCAAATATGTTACGGCCGATCGTTTCATCAAGCACGCATGAGTCTTACGGACTCACCCTGGAGC AATAGCACGATCCTTTTTTAAAACTCGGGCGTCGGGGGGTGCAGGCTAGCGCTAAAATTTTCAGCCGAGAGTTGTGAGGGCTGCCAGTTCTCGCCACGGGAGCGCGCTCTTGGTCTGATTCCTAGTCTCACATATCGCCACTCGCATCATTCGAGG'
dna = dna.split(' ')
best_motifs = GreedyMotifSearch(dna, k, t)
for motif in best_motifs:
	print motif







