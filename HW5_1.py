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
STAR = "*"
STOP = "STOP"

B = 10**8

tags_list = [IORG, BPER, BLOC, ILOC, IPER, BORG, IMISC, BMISC, O]

def log2(r):
	return log(r,2)

#does not matter whether we use the with-rare version or without-rare version right now
#only dealing with tags

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


trigrams = open("trigrams.txt", "r")
lines = [line.split() for line in trigrams.readlines()]
for line in lines:
	first = line[0]
	second = line[1]
	third = line[2]
	prob = q(third, first, second)
	if prob == 0:
		log_prob = -B
	else:
		log_prob = log2(prob)

	print(first+" "+second+" "+third+" "+str(log_prob))
trigrams.close()



