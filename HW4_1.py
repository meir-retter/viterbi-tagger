IORG = "I-ORG"
BLOC = "B-LOC"
ILOC = "I-LOC"
IPER = "I-PER"
BPER = "B-PER"
BORG = "B-ORG"
IMISC = "I-MISC"
BMISC = "B-MISC"
O = "O"
tags_list = [IORG, BPER, BLOC, ILOC, IPER, BORG, IMISC, BMISC, O]


orig_counts = open("ner.counts", "r")
lines = [line.split() for line in orig_counts.readlines()]

orig_word_tag_counts = {}
orig_tag_counts = {}
orig_word_counts = {} # without _RARE_ involved
for line in lines: # record number of times a word gets a tag
	if line[1] == "WORDTAG":
		count = int(line[0])
		label = line[2]
		word = line[3]
		orig_word_tag_counts[(word, label)] = count
		if word not in orig_word_counts.keys():
			orig_word_counts[word] = 0
		orig_word_counts[word] += count
	else: # record individual tag counts
		if line[1] == "1-GRAM":
			tag = line[2]
			count = int(line[0])
			orig_tag_counts[tag] = count
orig_counts.close()

def e(x, y): # e(x|y)
	if (x,y) not in orig_word_tag_counts.keys():
		return 0.0
	return float(orig_word_tag_counts[(x,y)])/float(orig_tag_counts[y])

orig_training_data = open("ner_train.dat", "r")
training_data_with_rare = open("ner_train.dat.rare_processed", "w")
lines = [line.split() for line in orig_training_data.readlines()]
for line in lines:
	if line == []:
		training_data_with_rare.write("\n")
	else:
		word = line[0]
		label = line[1]
		if orig_word_counts[word] < 5:
			word = "_RARE_"
		training_data_with_rare.write(word+" "+label+"\n")
orig_training_data.close()
training_data_with_rare.close()

# Now, we can run "python count_freqs.py ner_train_with_rare.dat > ner_with_rare.counts" on the terminal to create new counts
