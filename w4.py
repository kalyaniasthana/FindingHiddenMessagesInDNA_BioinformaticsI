#from __future__ import division
from w2_2 import *
from ch6 import *
import numpy
import random
from numpy.random import choice

def inputFile(file):
    lines = file.readline().split()
    k = int(lines[0])
    t = int(lines[1])
    N = int(lines[2])
    dna = []
    for i in range(t):
        dna.append(file.readline().strip())
    return (dna,k,t,N)

def MotifsFromProfileMatrix(dna, profile, k):
	motifs = []
	for dna_ in dna:
		most_prob = ProfileMostProbable(dna_, k, profile)
		motifs.append(most_prob)
	return motifs

def RandomizedMotifSearch(dna, k, t):
	best_motifs = []
	for dna_ in dna:
			random_number = random.randint(0,len(dna_) - k)
			kmer = dna_[random_number: random_number + k]
			best_motifs.append(kmer)
	best_score = score(best_motifs)
	while True:
		profile = ProfileMatrixFromMotifsWithPseudocounts(best_motifs, 1)
		motifs = MotifsFromProfileMatrix(dna, profile, k)
		my_score = score(motifs)
		if my_score < best_score:
			best_motifs = motifs
			best_score = my_score
		else:
			return best_motifs

def RandomizedMotifSearchWithIterations(dna, k, t):
	best_score = 999999
	best_motifs = []
	iterations = 0
	while True:
		motifs = RandomizedMotifSearch(dna, k, t)
		my_score = score(motifs)
		if my_score < best_score:
			best_score = my_score
			best_motifs = motifs
			iterations = 0
			print(best_score)
		else:
			iterations += 1
		if iterations > 500:
			break
	return best_motifs

def Probabilities(motifs, profile):
	probs = []
	for motif in motifs:
		prob = 1
		for j in range(len(motif)):
			prob = prob*profile[motif[j]][j]
		probs.append(prob)
	return probs

def RandomMotif(probs, dna_string, k):
	sums = float(sum(probs))
	random_prob = random.random()
	my_sum = 0.0
	for i in range(len(probs)):
		my_sum += probs[i]
		if random_prob <= my_sum/sums:
			return dna_string[i:i+k]


def GibbsSampler(dna, k, t, N):
	motifs = []
	best_motifs = []
	for dna_ in dna:
			random_number = random.randint(0,len(dna_) - k)
			kmer = dna_[random_number: random_number + k]
			motifs.append(kmer)
	best_motifs = motifs
	best_score = score(best_motifs)
	for j in range(0, N):
		i = random.randrange(t)
		motifs.remove(motifs[i])
		profile = ProfileMatrixFromMotifsWithPseudocounts(motifs, 1)
		dnai_motifs= []

		for l in range(len(dna[i]) - k + 1):
			dnai_motifs.append(dna[i][l:l+k])

		probs = Probabilities(dnai_motifs, profile)
		my_motif = RandomMotif(probs, dna[i], k)
		motifs.insert(i, my_motif)
		my_score = score(motifs)
		if my_score < best_score:
			best_motifs = motifs
			best_score = my_score

	return (best_motifs, best_score)

def GibbsSamplerIterative(dna, k, t, N):
	best_motifs = []
	for dna_ in dna:
			random_number = random.randint(0,len(dna_) - k)
			kmer = dna_[random_number: random_number + k]
			best_motifs.append(kmer)
	best_score = score(best_motifs)
	for i in range(0, 250):
		(motifs, my_score) = GibbsSampler(dna, k, t, N)
		if my_score < best_score:
			best_motifs = motifs
			best_score = my_score

	return best_motifs
'''
file = inputFile(open('../Downloads/dataset_163_4.txt'))
dna = file[0]
k = file[1]
t = file[2]
N = file[3]
N = N//10

motifs = GibbsSamplerIterative(dna, k, t, N)
for motif in motifs:
	print(motif)
'''


