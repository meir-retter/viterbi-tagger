Meir Retter
smr2215


README



Note: count_freqs.py and eval_ne_tagger.py should be run using Python 2, while all other .py files should be run with Python 3.



-----QUESTION 4_1-----

Enter into the terminal: 

python3 HW4_1.py

This creates ner_train.dat.rare_processed, takes < 1 sec to run. Then enter

python count_freqs.py ner_train.dat.rare_processed > 4_1.txt

This creates 4_1.txt, which could also be called "ner.counts.rare_processed".



-----QUESTION 4_2-----
Once 4_1.txt is created, enter into the terminal:

python3 HW4_2.py

This creates 4_2.txt directly.

Here are the somewhat decent results that the simple entity tagger gave:


Found 14043 NEs. Expected 5931 NEs; Correct: 3117.

	     precision 	recall 		F1-Score
Total:	 0.221961	0.525544	0.312106
PER:	 0.435451	0.231230	0.302061
ORG:	 0.475936	0.399103	0.434146
LOC:	 0.147750	0.870229	0.252612
MISC:	 0.491689	0.610206	0.544574



-----QUESTION 5_1-----

This one was very straightforward. Have trigrams.txt available (an example is provided) and enter into the terminal:

python3 HW5_1.py

This does not create a file, but prints output.

As expected, it gives appropriate log probabilities for trigrams, giving negative infinity to some infeasible ones.



-----QUESTION 5_2-----
The Viterbi tagger. Enter into the terminal

python3 HW5_2.py

This creates 5_2.txt. Here are the results that the evaluator showed for 5_2.txt:

Found 4704 NEs. Expected 5931 NEs; Correct: 3648.

	 precision 	recall 		F1-Score
Total:	 0.775510	0.615073	0.686037
PER:	 0.763231	0.596300	0.669517
ORG:	 0.611855	0.478326	0.536913
LOC:	 0.876458	0.696292	0.776056
MISC:	 0.830065	0.689468	0.753262

Observe that it is better than the baseline tagger, getting 3648 correct instead of only 3117.



-----QUESTION 6-----
For Question 6, I have HW6_1.py which is similar to HW4_1.py, in that it creates a training file. HW4_1.py creates a training file with a single class of rare words (ner_train.dat.rare_processed), while HW6_1.py creates one with multiple classes of rare words (ner_train.dat.rare_processed_advanced). 

Then, counts_freq.py should be run on ner_train.dat.rare_processed_advanced to create ner.counts.rare_processed_advanced.

Finally, there is HW6.py, which is similar to HW5_2.py, but it uses the advanced multi-rare-class counts. 

Results for Question 6:

I used the classes given in the homework document with one change: capitalization is not special if it's the first word in the sentence.

_RARE1_ --> capitalized words that are not the first words in their sentence.
_RARE2_ --> words that contain only capital letters and dots
_RARE3_ --> words that consist of only numerals, and
_RARE4_ --> all others.

Doing this increased the performance of the Viterbi tagger, giving 4161 correct instead of 3648 correct:

Found 5331 NEs. Expected 5931 NEs; Correct: 4161.

	 precision 	recall 		F1-Score
Total:	 0.780529	0.701568	0.738945
PER:	 0.799417	0.745919	0.771742
ORG:	 0.637634	0.579970	0.607436
LOC:	 0.843712	0.753544	0.796083
MISC:	 0.830486	0.686211	0.751486



