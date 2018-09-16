def PatternToNumber(pattern):
	num = 0
	pattern = pattern.lower()
	p = len(pattern) - 1
	for i in range(0,len(pattern)):
		if pattern[i] == 'a':
			num += 0*(4**p)
		elif pattern[i] == 't':
			num += 3*(4**p)
		elif pattern[i] == 'g':
			num += 2*(4**p)
		elif pattern[i] == 'c':
			num += 1*(4**p)

		p -= 1
	return num

print PatternToNumber('ATGCAA')