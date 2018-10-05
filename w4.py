from __future__ import division
from w2_2 import *
from ch6 import *
import numpy
import random

def inputFile(file):
    lines = file.readline().split()
    k = int(lines[0])
    t = int(lines[1])
    dna = []
    for i in range(t):
        dna.append(file.readline().strip())
    return (dna,k,t)

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
			print best_score
		else:
			iterations += 1
		if iterations > 500:
			break
	return best_motifs


file = inputFile(open('../Downloads/dataset_161_5 (1).txt'))
dna = file[0]
k = file[1]
t = file[2]
motifs = RandomizedMotifSearchWithIterations(dna, k, t)
for motif in motifs:
	print motif



