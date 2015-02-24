""" Testing the WriteMeAPoem module """
import unittest
from WriteMeAPoem import *

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_rhymes(self):
        self.assertTrue(words_rhymes("potato", "potato"))
        self.assertFalse(words_rhymes("train", "potato"))

    def test_respect_structure(self):
        self.structures = {'haiku3': [(5, None), (7, None), (5, None)],
                            'rhymetest' : [(2, 1), (2, 0)]}
        myhaikutest = ['a b c d e', 'a b c d e f g', 'a b c d e']
        self.assertTrue(respect_structure(myhaikutest, self.structures['haiku3']))
        myrhymetest = ["patato", "potato"]
        self.assertTrue(respect_structure(myrhymetest, self.structures['rhymetest']))

    def test_get_vocabulary_from_theme(self):
        vocabulary = get_vocabulary_from_theme("potato")
        self.assertTrue(len(vocabulary) > 0)

    def test_get_disambiguation(self):
        foodrelated = get_disambiguation("I eat on a table.", "table")
        programming_related = get_disambiguation("I program software on a table.", "table")
        self.assertTrue(len(foodrelated) > 0)
        self.assertTrue(len(programming_related) > 0)
        #self.assertTrue(len(get_disambiguation("I like to drink punch.","punch"))>0)
        #print get_disambiguation("he is playing the bass guitar nicely","bass")
        #print get_disambiguation("I fish sea bass","bass")
        #self.assertTrue(foodrelated != programming_related)

    def test_find_synonyms(self):
        self.assertTrue("nice" in find_synonyms("good"))
        self.assertFalse("potato" in find_synonyms("car"))

    def test_count_syllables(self):
        self.assertTrue(count_syllables("table") == 2)
        self.assertFalse(count_syllables("") > 0)

    def test_syllables_matching_words_from_list(self):
        self.assertTrue(len(syllables_matching_words_from_list(["healthy", "nice"], "very")) == 2)
        self.assertTrue(len(syllables_matching_words_from_list(["healthy", "nice"], "potatoes")) == 0)
        self.assertFalse(len(syllables_matching_words_from_list([], "potatoes")) > 0)

    def test_rhyming_words_from_list(self):
        self.assertTrue(len(rhyming_words_from_list(["chorizo", "tomato"], "potato")) == 1)
        self.assertTrue(len(rhyming_words_from_list(["chorizo", "tomato"], "chair")) == 0)
        self.assertFalse(len(rhyming_words_from_list([], "potatoes")) > 0)

    def test_spellcheck(self):
        self.assertTrue(len(spellcheck("This sentence is correct.")) == 0)
        self.assertTrue(len(spellcheck("This sentence is incorrtect.")) > 0)

    def test_estimate_sentiment(self):
        [polarity, subjectivity] = estimate_sentiment("I am very happy and this is true.")
        self.assertTrue(polarity != 0 and subjectivity != 0)

    def test_replace_tag(self):
        sentence1 = 'I want to eat fruits.'
        self.assertTrue(replace_tag(sentence1, 'NNS', 'vegetables') == 'I want to eat vegetables.')
        self.assertTrue(replace_tag(sentence1, 'NN', 'vegetables') == 'I want to eat fruits.')

    def test_respect_grammar(self):
        sentence1 = 'I want to eat fruits.'
        self.assertTrue(respect_grammar(sentence1, ['PRP', 'VBP', 'TO', 'VB', 'NNS', '.']))

    def test_estimated_coherence(self):
        #check coherence : word2vec with pretrained data
        #consider instead cheaper generic NLP : NTLK / spaCy
        generated_paragraph = 'I eat tapas in Spain and camembert in France.'
        generated_paragraph += 'They were both delicious but especially the cheese.'
        estimated_coherence = 0
        print 'estimated_coherence:' + str(estimated_coherence)
        raise NotImplementedError
        #import gensim
        #import os
        #model = gensim.models.word2vec.Word2Vec.load_word2vec_format(os.path.join(os.path.dirname(__file__), 'GoogleNews-vectors-negative300.bin'), binary=True)
        #model.most_similar('dog')
        # consider http://stackoverflow.com/questions/8897593/similarity-between-two-text-documents
        # if uses less memory

if __name__ == '__main__':
    unittest.main()
