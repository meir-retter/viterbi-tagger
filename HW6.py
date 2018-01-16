from math import log

IORG = "I-ORG"
BLOC = "B-LOC"
ILOC = "I-LOC"
IPER = "I-PER"
BPER = "B-PER"
BORG = "B-ORG"
IMISC = "I-MISC"
BMISC = "B-MISC"
O = "O"
STAR = "*"
STOP = "STOP"

tags_list = (BLOC, BPER, ILOC, IPER, BORG, IMISC, IORG, BMISC, O)

B = float("inf")

def log2(r):
	if r == 0:
		return -B
	else:
		return log(r,2)

#now, do everything as in the beginning of hw4_1.py, but using the _RARE_ symbol

counts = open("ner.counts.rare_processed_advanced", "r")
lines = [line.split() for line in counts.readlines()]

word_tag_counts = {}
tag_counts = {}
word_counts = {}
for line in lines: # record number of times a word gets a tag
	if line[1] == "WORDTAG":
		count = int(line[0])
		label = line[2]
		word = line[3]
		word_tag_counts[(word, label)] = count
		if word not in word_counts.keys():
			word_counts[word] = 0
		word_counts[word] += count
	else: # record unigram tag counts
		if line[1] == "1-GRAM":
			tag = line[2]
			count = int(line[0])
			tag_counts[tag] = count

counts.close()

def rare_word_classifier(word, is_first_in_sentence):
	if all([letter in "1234567890" for letter in word]):
		return "_RARE3_"
	if all([letter in "QWERTYUIOPASDFGHJKLZXCVBNM." for letter in word]):
		return "_RARE2_"
	if word[0] in "QWERTYUIOPASDFGHJKLZXCVBNM" and not is_first_in_sentence:
		return "_RARE1_"
	return "_RARE4_"

def e(x, y, is_first_in_sentence): # e(x|y)
	if x not in word_counts.keys():
		return e(rare_word_classifier(x, is_first_in_sentence), y, is_first_in_sentence)
	if (x,y) not in word_tag_counts.keys() or y not in tag_counts.keys():
		return 0
	return float(word_tag_counts[(x,y)])/float(tag_counts[y])

def T(x):
	pass


counts = open("ner.counts", "r")
lines = [line.split() for line in counts.readlines()]

bigram_tag_counts = {}
trigram_tag_counts = {}

for line in lines:
	if line[1] == "2-GRAM":
		first = line[2]
		second = line[3]
		count = line[0]
		bigram_tag_counts[(first, second)] = count
	elif line[1] == "3-GRAM":
		first = line[2]
		second = line[3]
		third = line[4]
		count = line[0]
		trigram_tag_counts[(first, second, third)] = count
counts.close()

def q(yi, yi_2, yi_1):
	# q(yi | yi-2, yi-1)
	if (yi_2, yi_1) not in bigram_tag_counts.keys() or (yi_2, yi_1, yi) not in trigram_tag_counts.keys():
		return 0
	else:
		return float(trigram_tag_counts[(yi_2, yi_1, yi)])/(float(bigram_tag_counts[(yi_2, yi_1)]))


def K(i):
	if i in (0,-1):
		return (STAR,)
	else:
		return tags_list



def viterbi(x_seq):
	# x_seq is a list of words
	# returns the list of tags y_seq that maximizes p(x_seq, y_seq)
	# even though Python uses 0-based indexing, here the input will be consistent with
	  #the indexing used in the class's written version of the algorithm
	# so, xk is found using x_seq[k-1]
	PI = {} # holds log probabilities, not probabilities
	PI[(0, "*", "*")] = 0.0
	bp = {} # backpointer dictionary
	N = len(x_seq)
	for k in range(1,N+1):
		for v in K(k):
			for u in K(k-1):
				# this part finds the best w
				best_w = None#K(k-2,x_seq)[0]
				highest_PI = -B
				for w in K(k-2):
					if k == 1:
						is_first = True
					else:
						is_first = False
					current_PI = PI[(k-1, w, u)] + log2(q(v,w,u)) + log2(e(x_seq[k-1],v, is_first))
					if current_PI > highest_PI:
						highest_PI = current_PI
						best_w = w
				PI[(k,u,v)] = highest_PI
				bp[(k,u,v)] = best_w
	best_ending_y_pair = None, None # the best (yn-1, yn) pair of tags to finish off the sentence
	highest_ending_PI = -B
	for v in K(N):
		for u in K(N-1):
			current_ending_PI = PI[(N,u,v)] + log2(q(STOP, u,v))
			if current_ending_PI > highest_ending_PI:
				highest_ending_PI = current_ending_PI
				best_ending_y_pair = (u,v)
	y_seq = [None for i in range(N)] # access yk by y_seq[k-1]
	y_seq[N-2] = best_ending_y_pair[0] # yn-1
	y_seq[N-1] = best_ending_y_pair[1] # yn
	for k in range(N-2, 0, -1):
		y_seq[k-1] = bp[(k+2, y_seq[k], y_seq[k+1])]
	# here we find the up-til log probabilities
	# this is just using the PI values
	log_probs_up_to_words = [None for i in range(N)]
	log_probs_up_to_words[0] = PI[(1,STAR,y_seq[0])]
	for k in range(2, N+1):
		log_probs_up_to_words[k-1] = PI[(k,y_seq[k-2],y_seq[k-1])]
	return y_seq, log_probs_up_to_words



input_file = open("ner_dev.dat", "r")
output_file = open("6.txt", "w")

lines = [line[:-1] for line in input_file.readlines()]

def first_sentence(lines):
	# returns the first sentence, and the remaining portion of `lines`
	if '' not in lines:
		return lines, []
	i = lines.index('')
	if i == 0:
		return first_sentence(lines[1:])
	if i == len(lines)-1:
		return lines[:-1], []
	return lines[:i], lines[i+1:]

while lines:
	s, lines = first_sentence(lines)
	V = viterbi(s)
	tags = V[0]
	probs = V[1]
	for i in range(len(s)):
		output_file.write(s[i]+' '+tags[i]+' '+str(probs[i])+'\n')
	output_file.write('\n')





















input_file.close()
output_file.close()





