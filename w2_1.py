import more_itertools as mit

def skew(genome):
	skew = []
	skew.append(0)
	for i in range(0, len(genome)):
		if genome[i] == 'G':
			skew.append(skew[i] + 1)
		elif genome[i] == 'C':
			skew.append(skew[i] - 1)
		else:
			skew.append(skew[i])

	m = max(skew)
	ml = []
	for i in range(0, len(skew)):
		if skew[i] == m:
			ml.append(str(i))
	return ' '.join(ml)

genome = 'CATTCCAGTACTTCATGATGGCGTGAAGA'
print(skew(genome))



