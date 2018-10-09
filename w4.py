from __future__ import division
from w2_2 import *
from ch6 import *
import numpy
import random
import numpy as np

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

def ProbabilityMatrix(motifs, profile):
	probs = []
	for motif in motifs:
		prob = 1
		for j in range(0, len(motif)):
			if motif[j] == 'A':
				prob *= profile['A'][j]
			elif motif[j] == 'C':
				prob *= profile['C'][j]
			elif motif[j] == 'G':
				prob *= profile['G'][j]
			elif motif[j] == 'T':
				prob *= profile['T'][j]

		probs.append(prob)
	if sum(probs) != 1:
		my_sum = sum(probs)
		for prob in probs:
			prob /= my_sum
	return probs


def ProfileRandomlyGeneratedKmer(probability_list, dnai, k):
	list_of_candidate_kmers = []
	for i in range(0, len(dnai) - k + 1):
		list_of_candidate_kmers.append(dnai[i:i+k])
	motif_i = list_of_candidate_kmers[np.argmin((np.cumsum(probability_list) / sum(probability_list)) < np.random.rand())]
	return motif_i


'''
def RandomChoice(probs, dnai):
	my_prob = random.choice(probs)
	my_motif = ''
	#for prob in probs:
		#if prob == my_probs:
	for i in range(0, len(motifs)):
		if probs[i] == my_prob:
			my_motif = motifs[i]
			break
	return my_motif'''

def GibbsSampler(dna, k, t, N):
	motifs = []
	best_motifs = []
	for dna_ in dna:
			random_number = random.randint(0,len(dna_) - k)
			kmer = dna_[random_number: random_number + k]
			motifs.append(kmer)
	best_motifs = motifs
	best_score = 99999
	for j in range(0, 20):
		i = random.choice(range(t))
		motifs.remove(motifs[i])
		profile = ProfileMatrixFromMotifsWithPseudocounts(motifs, 1)
		probability_list = ProbabilityMatrix(motifs, profile)
		my_motif = ProfileRandomlyGeneratedKmer(probability_list, dna[i], k)
		motifs.insert(i, my_motif)
		my_score = score(motifs)
		if my_score < best_score:
			best_motifs = motifs
			best_score = my_score


	return best_motifs

dna = 'CGCCCCTCTCGGGGGTGTTCAGTAACCGGCCA GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG TAGTACCGAGACCGAAAGAAGTATACAGGCGT TAGATCAAGTTTCAGGTGCACGTCGGTGAACC AATCCACCAGCTCCACGTGCAATGTTGGCCTA'
dna = dna.split(' ')

print GibbsSampler(dna, 8, 5, 100)


