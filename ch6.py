def PatternToNumber(pattern):
	num = 0
	d = {'a' : 0, 't': 3, 'g': 2, 'c': 1}
	pattern = pattern.lower()
	p = len(pattern) - 1
	for i in range(0,len(pattern)):
		num += d[pattern[i]]*(4**p)
		p -= 1
	return num

#def NumberToPattern(number, k):




print PatternToNumber('ATGCAA')