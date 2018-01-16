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
RARE = "_RARE_"
tags_list = [IORG, BPER, BLOC, ILOC, IPER, BORG, IMISC, BMISC, O]

def log2(r):
	return log(r,2)

#now, do everything as in the beginning of hw4_1.py, but using the _RARE_ symbol

counts = open("4_1.txt", "r")
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
	else: # record individual tag counts
		if line[1] == "1-GRAM":
			tag = line[2]
			count = int(line[0])
			tag_counts[tag] = count

counts.close()

def e(x, y): # e(x|y)
	if (x,y) not in word_tag_counts.keys():
		return 0.0
	return float(word_tag_counts[(x,y)])/float(tag_counts[y])

def simple_tagger(x):
	# returns the tag y that gives the greatest e(x|y) for a given x
	if x not in word_counts.keys() or word_counts[x] < 5: # unseen or rare words should be given the _RARE_ tag and probability
		return simple_tagger(RARE)
	best_tag = None
	highest_e = 0.0
	for y in tags_list:
		score = e(x,y)
		if score > highest_e:
			highest_e = score
			best_tag = y
	return best_tag, highest_e

input_file = open("ner_dev.dat", "r")
output_file = open("4_2.txt", "w")



rare_tag = simple_tagger(RARE)


lines = [line.split() for line in input_file.readlines()]
for line in lines:
	if line == []:
		output_file.write("\n")
	else:
		word = line[0]
		tag_answer = simple_tagger(word)
		output_file.write(word+" "+tag_answer[0]+" "+str(log2(tag_answer[1]))+"\n")

input_file.close()
output_file.close()