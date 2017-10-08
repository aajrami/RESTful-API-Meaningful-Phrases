## @uthor Ahmed Alajrami
##

import nltk
from nltk.collocations import *
from nltk import ngrams
from bs4 import BeautifulSoup
import glob
import os.path

class Model():
    def buildModel(self):
        ## check if the training data files have been pre-processed before
        if not os.path.isfile('training-data.txt'):
            ## extract text from the HTML text files and save it in training-data.txt
            traingin_data = open('training-data.txt', 'w')
            files = glob.glob('data/training/*')
            ## iterate over the list getting each file
            for file in files:
                # open the file and then call .read() to get the text
                with open(file) as f:
                    text = f.read()
                    soup = BeautifulSoup(text, 'html.parser')
                    traingin_data.write(soup.get_text())
            traingin_data.close()

            bigram_measures = nltk.collocations.BigramAssocMeasures()
            trigram_measures = nltk.collocations.TrigramAssocMeasures()

            ## read text from the training-data file and do tokenization
            data_file = open('training-data.txt')
            tokens = nltk.tokenize.word_tokenize(data_file.read())

            ## ****** find bigram collocations ******
            finder = BigramCollocationFinder.from_words(tokens)
            ## ignore  all bigrams which occur less than 100 times in the training data
            finder.apply_freq_filter(100)
            ## ignore high-frequency words like the, to,  also, etc.
            ignored_words = nltk.corpus.stopwords.words('english')
            finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
            finder.apply_word_filter(lambda w: w.islower())
            ## save the bigram collocations in a file
            bigram_output = open('bigrams.txt', 'w')
            ## the 500 2-grams with the highest pointwise mutual information
            for p in finder.nbest(bigram_measures.pmi, 500):
                bigram_output.write(' '.join(p).lower() + '\n')

            bigram_output.close()

            ## ****** find trigram collocations ******
            finder = TrigramCollocationFinder.from_words(tokens)
            ## ignore  all trigrams which occur less than 20 times in the training data
            finder.apply_freq_filter(20)
            ## ignore high-frequency words like the, to,  also, etc.
            ignored_words = nltk.corpus.stopwords.words('english')
            finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
            finder.apply_word_filter(lambda w: w.islower())
            ## save the bigram collocations in a file
            trigram_output = open('trigrams.txt', 'w')
            ## the 500 3-grams with the highest pointwise mutual information
            for p in finder.nbest(trigram_measures.pmi, 500):
                trigram_output.write(' '.join(p).lower() + '\n')

            trigram_output.close()

    ## process the text posted using POST
    def postedText(self, text):
        ## tokenization
        tokens = nltk.tokenize.word_tokenize(text)
        ## getting the bigrams
        string_bigrams = ngrams(tokens,2)
        script_dir = os.path.dirname(__file__)  ## absolute dir the script is in
        bigrams_file = "bigrams.txt"
        bigrams_file_path = os.path.join(script_dir, bigrams_file)
        trigrams_file = "trigrams.txt"
        trigrams_file_path = os.path.join(script_dir, trigrams_file)
        ## extracted phrases
        phrases = []
        for grams in string_bigrams:
            ## check if the bigram is seen before in the top bigrams list
            if ' '.join(grams).lower() in open(bigrams_file_path).read():
                phrases.append(' '.join(grams))
        ## getting the trigrams
        string_trigrams = ngrams(tokens, 3)
        for grams in string_trigrams:
            ## check if the trigram is seen before in the top trigrams list
            if ' '.join(grams).lower() in open(trigrams_file_path).read():
                phrases.append(' '.join(grams))
        ## return the list of extracted phrases from the posted text
        return phrases
