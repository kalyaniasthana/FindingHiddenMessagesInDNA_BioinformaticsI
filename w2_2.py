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
	return ' '.join(neighborhood)

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

def iterativeNeighbors(pattern, d):
	neighborhood = ['A', 'T', 'G', 'C']
	for i in range(1, d + 1):
		for text in neighborhood:
			neighborhood.append(immediateNeighbours(text))
	return set(neighborhood)

