# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 17:25:54 2018

@author: weiho
"""
import os
import numpy as np
import random

#takes the chord data of the chorales, separates data into major and minor
chorales = []
basedir = "C:/Users/weiho/OneDrive/Duke/Fall 2018/Math 163F/bhchorale"
for root, dirs, files in os.walk("C:/Users/weiho/OneDrive/Duke/Fall 2018/Math 163F/bhchorale"):
    for i in files:
        if i.__contains__('.krn'):
            chorales.append(os.path.join(basedir, i))

files = [open(i, "r") for i in chorales]
choralesmajor = []
choralesminor = []
for f in files:
    major = True
    chords = []
    for line in zip(f):
        data = line[0]
        x = data.split("\t")
        if len(x[0])>2 and x[0][0] == '*' and x[0][2] == ':':
            if x[0][1].islower():
                major = False
        if x[0][0] not in ('!', '*', '.', '=', 'r'):
            if x[0][-1] == ';':
                chords.append(x[0][:-1])
            else:
                chords.append(x[0])
    if major:
        choralesmajor.append(chords)
    else: 
        choralesminor.append(chords)

#randomly chooses 10 chorales to create the Markov matrix from
choralesamplesize = 5
trainingmajor = [choralesmajor[i] for i in random.sample(range(0, len(choralesmajor)), choralesamplesize)]
trainingminor = [choralesminor[i] for i in random.sample(range(0, len(choralesminor)), choralesamplesize)]

#creates the Markov matrix
chordlistmajor = []
chordlistminor = []
for chorale in trainingmajor:
    for chord in chorale:
        if chord not in chordlistmajor:
            chordlistmajor.append(chord)
for chorale in trainingminor:
    for chord in chorale:
        if chord not in chordlistminor:
            chordlistminor.append(chord)

matrixmajor = np.zeros((len(chordlistmajor), len(chordlistmajor)))
matrixminor = np.zeros((len(chordlistminor), len(chordlistminor)))

for chorale in trainingmajor:
    for i in range(0, len(chorale)-1):
        matrixmajor[chordlistmajor.index(chorale[i])][chordlistmajor.index(chorale[i+1])] += 1
for chorale in trainingminor:
    for i in range(0, len(chorale)-1):
        matrixminor[chordlistminor.index(chorale[i])][chordlistminor.index(chorale[i+1])] += 1
#normalize Markov matrix
for i in range(0, len(matrixmajor)):
    if np.sum(matrixmajor[i]) > 0:
        matrixmajor[i] = np.multiply(matrixmajor[i], 1/np.sum(matrixmajor[i]))
    else:
        matrixmajor[i] = np.multiply(np.ones(len(chordlistmajor)), 1/len(chordlistmajor))
for i in range(0, len(matrixminor)):
    if np.sum(matrixminor[i]) > 0:
        matrixminor[i] = np.multiply(matrixminor[i], 1/np.sum(matrixminor[i]))
    else:
        matrixminor[i] = np.multiply(np.ones(len(chordlistminor)), 1/len(chordlistminor))

#calculate stationary distributions
probmajor = np.linalg.eig(np.transpose(matrixmajor))[1][:,0].real
probminor = np.linalg.eig(np.transpose(matrixminor))[1][:,0].real
probmajor = np.multiply(probmajor, 1/np.sum(probmajor))
probminor = np.multiply(probminor, 1/np.sum(probminor))

#generates a random chord based on stationary distribution
#prob = probabilities
#names = chord names
def generaterandchord(prob, names):
    dist = []
    for i in range(0, len(prob)):
        dist.append(prob[i])
    n = random.uniform(0, 1)
    i = 0
    while n >= 0:
        n -= dist[i]
        i += 1
    return names[i-1]

#generates a random chord sequence based on stationary distribution and transition matrix
#n = number of chords in sequence
#prob = stationary distribution
#mat = transition matrix
#names = chord names
def generatesequence(n, prob, mat, names):
    seq = []
    currentprob = prob
    for i in range(0, n):
        seq.append(generaterandchord(currentprob, names))
        currentprob = mat[names.index(seq[i])]
    return seq

#generate sequences of length 16
print(generatesequence(16, probmajor, matrixmajor, chordlistmajor))
print(generatesequence(16, probminor, matrixminor, chordlistminor))

#print most common chords
chordprobmajor = []
for i in range(0, len(chordlistmajor)):
    chordprobmajor.append([probmajor[i], chordlistmajor[i]])
chordprobminor = []
for i in range(0, len(chordlistminor)):
    chordprobminor.append([probminor[i], chordlistminor[i]])
chordprobmajor.sort(reverse=True)
chordprobminor.sort(reverse=True)

print(chordprobmajor[0:5])
print(chordprobminor[0:5])