def PatternToNumber(pattern):
	num = 0
	d = {'a' : 0, 't': 3, 'g': 2, 'c': 1}
	pattern = pattern.lower()
	p = len(pattern) - 1
	for i in range(0,len(pattern)):
		num += d[pattern[i]]*(4**p)
		p -= 1
	return num

def NumberToPattern(number, k):
	pattern = ""
	d = {0: 'a', 1: 'c', 2: 'g', 3: 't'}
	for i in range(0, k):
		div = number/4
		temp = number%4
		pattern = pattern + d[temp]
		number = div
	return pattern[:: - 1].upper()

print PatternToNumber('CCCAGGC')
print NumberToPattern(5437, 7)