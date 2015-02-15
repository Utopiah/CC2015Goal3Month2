import unittest
from writeMeAPoem import *
import random
# just to test testunit and kickstart it

''' Methodes to test
'''

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.structures = {}
        self.structures['haiku3'] = [(5,None),(7,None),(5,None)]
        self.structures['rhymetest'] = [(2,1),(2,0)]

    def test_rhymes(self):
        self.assertTrue(words_rhymes("potato","potato"))
        self.assertFalse(words_rhymes("train","potato"))

    def test_respect_structure(self):
        myhaikutest = ['a b c d e','a b c d e f g','a b c d e']
        #print 'Testing structure respect'
        #print 'structures:'+ str(structures)
        #print str(myhaikutest) + ' with structure ' + str(structures['haiku'])
        self.assertTrue(respect_structure(myhaikutest,self.structures['haiku3']))
        myrhymetest = ["patato","potato"]
        #print str(myrhymetest) + ' with structure ' + str(structures['rhymetest'])
        self.assertTrue(respect_structure(myrhymetest,self.structures['rhymetest']))

    def test_get_vocabulary_from_theme(self):
        # get_vocabulary_from_theme(w)
        self.assertTrue(False)

    def test_get_disambiguation(self):
        self.assertTrue(False)

    def test_find_synonyms(self):
        # find_synonyms(testwords[0])
        self.assertTrue(False)

    def test_count_syllables(self):
        self.assertTrue(False)

    def test_syllables_matching_words_from_list(self):
        # syllables_matching_words_from_list(synonyms,w)
        self.assertTrue(False)

    def test_rhyming_words_from_list(self):
        # rhyming_words_from_list(synonyms,w)
        self.assertTrue(False)

    def test_spellcheck(self):
        self.assertTrue(False)

    def test_estimate_sentiment(self):
        self.assertTrue(False)

    def test_replace_tag(self):
        self.assertTrue(False)

    def test_respect_grammar(self):
        sentence1 = 'I want to eat fruits.'
        self.assertTrue(respect_grammar(sentence1,['PRP', 'VBP', 'TO', 'VB', 'NNS', '.']))

    def ignoreme(self): 

        #check coherence : word2vec with pretrained data https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing
        #consider instead cheaper generic NLP : NTLK / spaCy
        generated_paragraph = 'I eat tapas in Spain and camembert in France. They were both delicious but especially the cheese.'
        estimated_coherence = 0
        print 'estimated_coherence:' + str(estimated_coherence)
        #import gensim
        #import os
        #model = gensim.models.word2vec.Word2Vec.load_word2vec_format(os.path.join(os.path.dirname(__file__), 'GoogleNews-vectors-negative300.bin'), binary=True)
        #model.most_similar('dog')
        # consider http://stackoverflow.com/questions/8897593/similarity-between-two-text-documents
        # if uses less memory
    
        found_rhyming_words = [] 
        print 'found_rhyming_words' + str(found_rhyming_words)

if __name__ == '__main__':
    unittest.main()
