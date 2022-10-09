import string
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pprint, time
import random

#Read dataset
with open('Brown_train.txt') as fp:
    data=fp.read()
raw_data=data.split('\n')
split_data=[]

'''split each sentence on space  and then again each spliited word_tag pair on / and create tuple with (word,pos_tag) add it to list
do it for each sentence in dataset'''
for sentence in raw_data:
    words_poss=[]
    for word_pos in sentence.split(" "):
        if "/" in word_pos:
            words_pos=word_pos.split("/")
            #for i in range(len(word_pos)-1):
            #    words_poss.append((word_pos[i],word_pos[i+1]))
            #words.extend(words_pos[:-1])
            for i in range(len(words_pos[:-1])):
                words_poss.append((words_pos[i],words_pos[-1]))
    split_data.append(words_poss)

#remove the punctutaion words and corresponding pos tag
for words_poss in split_data:
    for word_pos in words_poss:
        if word_pos[0] in string.punctuation:
            words_poss.remove(word_pos)

#split dataset
train_set,test_set =train_test_split(split_data,train_size=0.80,test_size=0.20,random_state = 101)

# create list of train and test tagged words
train_tagged_words=[ tup for sent in train_set for tup in sent ]
test_tagged_words=[ tup for sent in test_set for tup in sent ]

#use set datatype to check how many unique tags are present in training data
tags = {tag for word,tag in train_tagged_words}
print(len(tags))
print(tags) 

# check total words in vocabulary
vocab = {word for word,tag in train_tagged_words}

# compute Emission Probability
def word_given_tag(word, tag, train_bag = train_tagged_words):
    tag_list = [pair for pair in train_bag if pair[1]==tag]
    count_tag = len(tag_list)#total number of times the passed tag occurred in train_bag
    w_given_tag_list = [pair[0] for pair in tag_list if pair[0]==word]
    #now calculate the total number of times the passed word occurred as the passed tag.
    count_w_given_tag = len(w_given_tag_list)
    return (count_w_given_tag, count_tag)

# compute  Transition Probability
def t2_given_t1(t2, t1, train_bag = train_tagged_words):
    tags = [pair[1] for pair in train_bag]
    count_t1 = len([t for t in tags if t==t1])
    count_t2_t1 = 0
    for index in range(len(tags)-1):
        if tags[index]==t1 and tags[index+1] == t2:
            count_t2_t1 += 1
    return (count_t2_t1, count_t1)

# creating t x t transition matrix of tags, t= no of tags
# Matrix(i, j) represents P(jth tag after the ith tag)
tags_matrix = np.zeros((len(tags), len(tags)), dtype='float32')
for i, t1 in enumerate(list(tags)):
    for j, t2 in enumerate(list(tags)):
        tags_matrix[i, j] = t2_given_t1(t2, t1)[0]/t2_given_t1(t2, t1)[1]
#print(tags_matrix)

# convert the matrix to a df for better readability
#the table is same as the transition table shown in section 3 of article
tags_df = pd.DataFrame(tags_matrix, columns = list(tags), index=list(tags))

#viterbi
def Viterbi(words, train_bag = train_tagged_words):
    state = []
    T = list(set([pair[1] for pair in train_bag]))
    for key, word in enumerate(words):
        #initialise list of probability column for a given observation
        p = []
        for tag in T:
            if key == 0:
                transition_p = tags_df.loc['.', tag]
            else:
                transition_p = tags_df.loc[state[-1], tag]
            # compute emission and state probabilities
            emission_p = word_given_tag(words[key], tag)[0]/word_given_tag(words[key], tag)[1]
            state_probability = emission_p * transition_p
            p.append(state_probability)
        pmax = max(p)
        # getting state for which probability is maximum
        state_max = T[p.index(pmax)]
        state.append(state_max)
    return list(zip(words, state))

# Let's test our Viterbi algorithm on a few sample sentences of test dataset
random.seed(1234)      #define a random seed to get same sentences when run multiple times

# choose random 10 numbers
rndom = [random.randint(1,len(test_set)) for x in range(10)]

# list of 10 sents on which we test the model
test_run = [test_set[i] for i in rndom]

# list of tagged words
test_run_base = [tup for sent in test_run for tup in sent]

# list of untagged words
test_tagged_words = [tup[0] for sent in test_run for tup in sent]


#Here We will only test 10 sentences to check the accuracy
#as testing the whole training set takes huge amount of time
start = time.time()
tagged_seq = Viterbi(test_tagged_words)
end = time.time()
difference = end-start
print("Time taken in seconds: ", difference)
# accuracy
check = [i for i, j in zip(tagged_seq, test_run_base) if i == j]
accuracy = len(check)/len(tagged_seq)
print('Algorithm Accuracy: ',accuracy*100)

'''
#Code to test all the test sentences
#(takes alot of time to run s0 we wont run it here)
# tagging the test sentences()
test_tagged_words = [tup for sent in test_set for tup in sent]
test_untagged_words = [tup[0] for sent in test_set for tup in sent]
test_untagged_words

start = time.time()
tagged_seq = Viterbi(test_untagged_words)
end = time.time()
difference = end-start

print("Time taken in seconds: ", difference)

# accuracy
check = [i for i, j in zip(test_tagged_words, test_untagged_words) if i == j]

accuracy = len(check)/len(tagged_seq)
print('Viterbi Algorithm Accuracy: ',accuracy*100)


'''

'''
new_corpus=[]
new_pos=[]
for i in range(len(corpus)):
    words=[]
    poss=[]
    for j in range(len(corpus[i])):
        if corpus[i][j] not in string.punctuation:
            words.append(corpus[i][j])
            poss.append(pos[i][j])
    new_corpus.append(words)
    new_pos.append(poss)
split_train_percent=80
split=round(len(corpus)*(split_train_percent/100))
train_corpus,train_pos=new_corpus[:split],new_pos[:split]
test_corpus,test_pos=new_corpus[split:],new_pos[split:]
pos_tag=set()
for sentence in train_pos:
    for pos in sentence:
        pos_tag.add(pos)
pos_tag=list(pos_tag)
'''
