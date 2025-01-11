# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np
from typing import List, Tuple
pos_to_num = {'AJ0': 0, 'AJC': 1, 'AJS': 2, 'AT0': 3, 'AV0': 4, 'AVP': 5, \
    'AVQ': 6, 'CJC': 7, 'CJS': 8, 'CJT': 9, 'CRD': 10, 'DPS': 11, 'DT0': 12, \
    'DTQ': 13, 'EX0': 14, 'ITJ': 15, 'NN0': 16, 'NN1': 17, 'NN2': 18, 'NP0': 19, \
    'ORD': 20, 'PNI': 21, 'PNP': 22, 'PNQ': 23, 'PNX': 24, 'POS': 25, 'PRF': 26, \
    'PRP': 27, 'PUL': 28, 'PUN': 29, 'PUQ': 30, 'PUR': 31, 'TO0': 32, 'UNC': 33, \
    'VBB': 34, 'VBD': 35, 'VBG': 36, 'VBI': 37, 'VBN': 38, 'VBZ': 39, 'VDB': 40, \
    'VDD': 41, 'VDG': 42, 'VDI': 43, 'VDN': 44, 'VDZ': 45, 'VHB': 46, 'VHD': 47, \
    'VHG': 48, 'VHI': 49, 'VHN': 50, 'VHZ': 51, 'VM0': 52, 'VVB': 53, 'VVD': 54, \
    'VVG': 55, 'VVI': 56, 'VVN': 57, 'VVZ': 58, 'XX0': 59, 'ZZ0': 60, \
    'AJ0-AV0': 61, 'AJ0-VVN': 62, 'AJ0-VVD': 63, 'AJ0-NN1': 64, 'AJ0-VVG': 65, \
    'AVP-PRP': 66, 'AVQ-CJS': 67, 'CJS-PRP': 68, 'CJT-DT0': 69, 'CRD-PNI': 70, \
    'NN1-NP0': 71, 'NN1-VVB': 72, 'NN1-VVG': 73, 'NN2-VVZ': 74, 'VVD-VVN': 75}
num_to_pos = {0: 'AJ0', 1: 'AJC', 2: 'AJS', 3: 'AT0', 4: 'AV0', 5: 'AVP', \
    6: 'AVQ', 7: 'CJC', 8: 'CJS', 9: 'CJT', 10: 'CRD', 11: 'DPS', 12: 'DT0', \
    13: 'DTQ', 14: 'EX0', 15: 'ITJ', 16: 'NN0', 17: 'NN1', 18: 'NN2', 19: 'NP0', \
    20: 'ORD', 21: 'PNI', 22: 'PNP', 23: 'PNQ', 24: 'PNX', 25: 'POS', 26: 'PRF', \
    27: 'PRP', 28: 'PUL', 29: 'PUN', 30: 'PUQ', 31: 'PUR', 32: 'TO0', 33: 'UNC', \
    34: 'VBB', 35: 'VBD', 36: 'VBG', 37: 'VBI', 38: 'VBN', 39: 'VBZ', 40: 'VDB', \
    41: 'VDD', 42: 'VDG', 43: 'VDI', 44: 'VDN', 45: 'VDZ', 46: 'VHB', 47: 'VHD', \
    48: 'VHG', 49: 'VHI', 50: 'VHN', 51: 'VHZ', 52: 'VM0', 53: 'VVB', 54: 'VVD', \
    55: 'VVG', 56: 'VVI', 57: 'VVN', 58: 'VVZ', 59: 'XX0', 60: 'ZZ0', \
    61: 'AJ0-AV0', 62: 'AJ0-VVN', 63: 'AJ0-VVD', 64: 'AJ0-NN1', 65: 'AJ0-VVG', \
    66: 'AVP-PRP', 67: 'AVQ-CJS', 68: 'CJS-PRP', 69: 'CJT-DT0', 70: 'CRD-PNI', \
    71: 'NN1-NP0', 72: 'NN1-VVB', 73: 'NN1-VVG', 74: 'NN2-VVZ', 75: 'VVD-VVN'}
init_prob = np.full(76, 0.001)
transition_prob = np.full((76, 76), 0.001)
emission_prob = None
emission_dict = {'AJ0': {}, 'AJC': {}, 'AJS': {}, 'AT0': {}, 'AV0': {}, \
    'AVP': {}, 'AVQ': {}, 'CJC': {}, 'CJS': {}, 'CJT': {}, 'CRD': {}, \
    'DPS': {}, 'DT0': {}, 'DTQ': {}, 'EX0': {}, 'ITJ': {}, 'NN0': {}, \
    'NN1': {}, 'NN2': {}, 'NP0': {}, 'ORD': {}, 'PNI': {}, 'PNP': {}, \
    'PNQ': {}, 'PNX': {}, 'POS': {}, 'PRF': {}, 'PRP': {}, 'PUL': {}, \
    'PUN': {}, 'PUQ': {}, 'PUR': {}, 'TO0': {}, 'UNC': {}, 'VBB': {}, \
    'VBD': {}, 'VBG': {}, 'VBI': {}, 'VBN': {}, 'VBZ': {}, 'VDB': {}, \
    'VDD': {}, 'VDG': {}, 'VDI': {}, 'VDN': {}, 'VDZ': {}, 'VHB': {}, \
    'VHD': {}, 'VHG': {}, 'VHI': {}, 'VHN': {}, 'VHZ': {}, 'VM0': {}, \
    'VVB': {}, 'VVD': {}, 'VVG': {}, 'VVI': {}, 'VVN': {}, 'VVZ': {}, \
    'XX0': {}, 'ZZ0': {}, 'AJ0-AV0': {}, 'AJ0-VVN': {}, 'AJ0-VVD': {}, \
    'AJ0-NN1': {}, 'AJ0-VVG': {}, 'AVP-PRP': {}, 'AVQ-CJS': {}, \
    'CJS-PRP': {}, 'CJT-DT0': {}, 'CRD-PNI': {}, 'NN1-NP0': {}, \
    'NN1-VVB': {}, 'NN1-VVG': {}, 'NN2-VVZ': {}, 'VVD-VVN': {}}
# A set of sentences represented by tuples whose elements are tags in the
# corresponding sentences respectively. In other words, it is a set of 
# sequences of observations.
sentences = set()
test_sentences = []
word_to_num = {}

def start(file_lst: List[str]) -> None:
    for file in file_lst:
        f = open(file, "r", encoding='utf-8')
        temp = []
        for line in f:
            n = line.index(" ")
            word = line[:n]
            if word not in word_to_num:
                word_to_num[word] = len(word)
            tag = line[n+3:-1]
            if tag not in pos_to_num:
                tag = tag[:3]

            if len(temp) == 0:
                init_prob[pos_to_num[tag]] += 1
            
            if word in emission_dict[tag]:
                emission_dict[tag][word] += 1
            else:
                emission_dict[tag][word] = 1
            
            temp.append(tag) 

            if word == "." or  word == "?" or word == "!":
                sentences.add(tuple(temp))
                temp = []
        if len(temp) !=0:
            sentences.add(tuple(temp))
        f.close()
    return None

def init() -> None:
    """Compute the initial probabilities over the POS tags 
    and modify <init_prob>.
    """
    global init_prob
    init_prob = init_prob/init_prob.sum()
    return None

def transition() -> None:
    """Compute the transition probabilities from one POS tag to another
    and modify <transition_prob>.
    """
    global transition_prob
    for s in sentences:
        if len(s) == 1:
            pass
        else:
            for i in range(0, len(s)-1):
                transition_prob[pos_to_num[s[i]]][pos_to_num[s[i+1]]] += 1
    transition_prob = transition_prob/transition_prob.sum(axis=1)[:,None]
    return None

def emission() -> None:
    """Compute the emission probabilities from each POS tag to 
    each observed word and modify <emission_prob>.
    """
    global emission_prob
    emission_prob = np.full((76, len(word_to_num)), 0.00001)
    for i in emission_dict:
        for j in emission_dict[i]:
            emission_prob[pos_to_num[i]][word_to_num[j]] = emission_dict[i][j]
    emission_prob = emission_prob/emission_prob.sum(axis=1)[:,None]
    return None

def test(file: List[str]) -> None:
    f = open(file)
    temp = []
    for line in f:
        word = line[:-1]
        temp.append(word) 
        if word == "." or  word == "?" or word == "!" or word == ",":
            test_sentences.append(tuple(temp))
            temp = []
    if len(temp) !=0:
        test_sentences.append(tuple(temp))
    f.close()
    return None

def Viterbi(E: Tuple[str]) -> List[str]:
    """<E> is a sequence of observations.
    """
    path = []
    prob = np.full((len(E), 76), 0.00001)
    prev = np.full((len(E), 76), None)

    for i in range(0, 76):
        if E[0] in word_to_num:
            prob[0][i] = init_prob[i] * emission_prob[i][word_to_num[E[0]]]
        else:
            prob[0][i] = init_prob[i] * 0.0001

    for t in range(1, len(E)):
        for i in range(0, 76):
            if E[t] in word_to_num:
                x = max(list(range(76)), \
                    key=lambda x: prob[t-1][x]*transition_prob[x][i]*\
                        emission_prob[i][word_to_num[E[t]]])
                prob[t][i] = prob[t-1][x] * \
                    transition_prob[x][i] * emission_prob[i][word_to_num[E[t]]]
            else:
                x = max(list(range(76)), \
                    key=lambda x: prob[t-1][x]*transition_prob[x][i]*0.0001)
                prob[t][i] = prob[t-1][x] * transition_prob[x][i] * 0.0001
            prev[t][i] = x

    final = np.argmax(prob[-1])
    j = len(E) - 1
    while j >= 0:
        path.append(num_to_pos[final])
        final = prev[j][final]
        j -= 1
    return path[::-1]

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    start(training_list)
    init()
    transition()
    emission()
    test(test_file)
    f = open(output_file, 'w', encoding='utf-8')
    for s in test_sentences:
        results = Viterbi(s)
        for w in range(0, len(s)):
            f.write(s[w] + " : " + results[w] + "\n")
    f.close()

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Output file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)
