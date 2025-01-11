# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
from typing import List, Tuple
init_prob = {'AJ0': 0.001, 'AJC': 0.001, 'AJS': 0.001, 'AT0': 0.001, 'AV0': 0.001, \
    'AVP': 0.001, 'AVQ': 0.001, 'CJC': 0.001, 'CJS': 0.001, 'CJT': 0.001, 'CRD': 0.001, \
    'DPS': 0.001, 'DT0': 0.001, 'DTQ': 0.001, 'EX0': 0.001, 'ITJ': 0.001, 'NN0': 0.001, \
    'NN1': 0.001, 'NN2': 0.001, 'NP0': 0.001, 'ORD': 0.001, 'PNI': 0.001, 'PNP': 0.001, \
    'PNQ': 0.001, 'PNX': 0.001, 'POS': 0.001, 'PRF': 0.001, 'PRP': 0.001, 'PUL': 0.001, \
    'PUN': 0.001, 'PUQ': 0.001, 'PUR': 0.001, 'TO0': 0.001, 'UNC': 0.001, 'VBB': 0.001, \
    'VBD': 0.001, 'VBG': 0.001, 'VBI': 0.001, 'VBN': 0.001, 'VBZ': 0.001, 'VDB': 0.001, \
    'VDD': 0.001, 'VDG': 0.001, 'VDI': 0.001, 'VDN': 0.001, 'VDZ': 0.001, 'VHB': 0.001, \
    'VHD': 0.001, 'VHG': 0.001, 'VHI': 0.001, 'VHN': 0.001, 'VHZ': 0.001, 'VM0': 0.001, \
    'VVB': 0.001, 'VVD': 0.001, 'VVG': 0.001, 'VVI': 0.001, 'VVN': 0.001, 'VVZ': 0.001, \
    'XX0': 0.001, 'ZZ0': 0.001, 'AJ0-AV0': 0.001, 'AJ0-VVN': 0.001, 'AJ0-VVD': 0.001, \
    'AJ0-NN1': 0.001, 'AJ0-VVG': 0.001, 'AVP-PRP': 0.001, 'AVQ-CJS': 0.001, \
    'CJS-PRP': 0.001, 'CJT-DT0': 0.001, 'CRD-PNI': 0.001, 'NN1-NP0': 0.001, \
    'NN1-VVB': 0.001, 'NN1-VVG': 0.001, 'NN2-VVZ': 0.001, 'VVD-VVN': 0.001}
transition_prob = {'AJ0': {}, 'AJC': {}, 'AJS': {}, 'AT0': {}, 'AV0': {}, \
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
emission_prob = {}
# A set of sentences represented by tuples whose elements are tags in the
# corresponding sentences respectively. In other words, it is a set of 
# sequences of observations.
sentences = set()
test_sentences = []
# check = {'AJ0': 0, 'AJC': 0, 'AJS': 0, 'AT0': 0, 'AV0': 0, \
#     'AVP': 0, 'AVQ': 0, 'CJC': 0, 'CJS': 0, 'CJT': 0, 'CRD': 0, \
#     'DPS': 0, 'DT0': 0, 'DTQ': 0, 'EX0': 0, 'ITJ': 0, 'NN0': 0, \
#     'NN1': 0, 'NN2': 0, 'NP0': 0, 'ORD': 0, 'PNI': 0, 'PNP': 0, \
#     'PNQ': 0, 'PNX': 0, 'POS': 0, 'PRF': 0, 'PRP': 0, 'PUL': 0, \
#     'PUN': 0, 'PUQ': 0, 'PUR': 0, 'TO0': 0, 'UNC': 0, 'VBB': 0, \
#     'VBD': 0, 'VBG': 0, 'VBI': 0, 'VBN': 0, 'VBZ': 0, 'VDB': 0, \
#     'VDD': 0, 'VDG': 0, 'VDI': 0, 'VDN': 0, 'VDZ': 0, 'VHB': 0, \
#     'VHD': 0, 'VHG': 0, 'VHI': 0, 'VHN': 0, 'VHZ': 0, 'VM0': 0, \
#     'VVB': 0, 'VVD': 0, 'VVG': 0, 'VVI': 0, 'VVN': 0, 'VVZ': 0, \
#     'XX0': 0, 'ZZ0': 0, 'AJ0-AV0': 0, 'AJ0-VVN': 0, 'AJ0-VVD': 0, \
#     'AJ0-NN1': 0, 'AJ0-VVG': 0, 'AVP-PRP': 0, 'AVQ-CJS': 0, \
#     'CJS-PRP': 0, 'CJT-DT0': 0, 'CRD-PNI': 0, 'NN1-NP0': 0, \
#     'NN1-VVB': 0, 'NN1-VVG': 0, 'NN2-VVZ': 0, 'VVD-VVN': 0}

def start(file_lst: List[str]) -> None:
    for file in file_lst:
        f = open(file, "r", encoding='utf-8')
        temp = []
        for line in f:
            n = line.index(" ")
            word = line[:n]
            tag = line[n+3:-1]
            if tag not in init_prob and len(tag) == 7:
                tag = tag[4:] + "-" + tag[:3]
            if tag not in init_prob:
                if word in emission_prob and len(emission_prob[word]) != 0:
                    tag = max(emission_prob[word])
                else:
                    tag = "ZZ0"
            # check[tag] += 1

            if len(temp) == 0:
                init_prob[tag] += 1
            
            if word not in emission_prob:
                emission_prob[word] = {}
            if tag in emission_prob[word]:
                emission_prob[word][tag] += 1
            else:
                emission_prob[word][tag] = 1
            
            temp.append(tag) 

            if word == "." or  word == "?" or word == "!":
                sentences.add(tuple(temp))
                temp = []
        if len(temp) !=0:
            sentences.add(tuple(temp))
        f.close()
    # print(max(check))
    return None

def init() -> None:
    """Compute the initial probabilities over the POS tags 
    and modify <init_prob>.
    """
    global init_prob, sentences
    n = len(sentences)
    for i in init_prob:
        init_prob[i] = init_prob[i]/n
    return None

def transition() -> None:
    """Compute the transition probabilities from one POS tag to another
    and modify <transition_prob>.
    """
    global transition_prob, sentences
    for s in sentences:
        if len(s) == 1:
            pass
        else:
            for i in range(0, len(s)-1):
                if s[i+1] in transition_prob[s[i]]:
                    transition_prob[s[i]][s[i+1]] += 1
                else:
                    transition_prob[s[i]][s[i+1]] = 1
    for j in transition_prob:
        for k in init_prob:
            if k not in transition_prob[j]:
                transition_prob[j][k] = 0.001
        total = sum(transition_prob[j].values())
        for k in transition_prob:
            transition_prob[j][k] = transition_prob[j][k]/total
    return None

def emission() -> None:
    """Compute the emission probabilities from each POS tag to 
    each observed word and modify <emission_prob>.
    """
    global emission_prob
    for j in emission_prob:
        total = sum(emission_prob[j].values())
        for k in emission_prob[j]:
            emission_prob[j][k] = emission_prob[j][k]/total
    return None

def test(file: List[str]) -> None:
    """To split the sentences in <file>, which will be stored in 
    <test_sentences>.
    """
    f = open(file)
    temp = []
    for line in f:
        word = line[:-1]
        temp.append(word) 
        if word == "." or  word == "?" or word == "!":
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
    prob = {0:{}}
    prev = {0:{}}

    for i in init_prob:
        if E[0] in emission_prob and i in emission_prob[E[0]]:
            prob[0][i] = init_prob[i] * emission_prob[E[0]][i]
        else:
            prob[0][i] = init_prob[i] * 0.0001
        prev[0][i] = None

    for t in range(1, len(E)):
        prob[t] = {}
        prev[t] = {}
        for i in init_prob:
            if E[t] in emission_prob and i in emission_prob[E[t]]:
                x = max(list(prob[t-1].keys()), \
                    key=lambda x: prob[t-1][x]*transition_prob[x][i]*\
                        emission_prob[E[t]][i])
                prob[t][i] = prob[t-1][x] * \
                    transition_prob[x][i] * emission_prob[E[t]][i]
            else:
                x = max(list(prob[t-1].keys()), \
                    key=lambda x: prob[t-1][x]*transition_prob[x][i]*0.0001)
                prob[t][i] = prob[t-1][x] * transition_prob[x][i] * 0.0001
            prev[t][i] = x

    # final = max(prob[len(E)-1])
    final = "PUN"
    j = len(E) - 1
    while j >= 0:
        path.append(final)
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
