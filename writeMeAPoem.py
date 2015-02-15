import random
import sys
import re
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
import hunspell
import pyphen
from metaphone import doublemetaphone
from pattern.en import sentiment, parsetree
from pattern.web import plaintext
from pattern.web import Twitter, Bing
from pattern.search import search

def get_vocabulary_from_theme(theme):
    vocabulary = []
    twitter = Twitter(language='en')
    metaphor_patterns = ["is like", "feels like","is more important than"]
    for metaphor_source in metaphor_patterns:
        for tweet in twitter.search('"' + theme + " " + metaphor_source + '"', cached=False):
            cleaned_tweet = re.sub("RT", "", plaintext(tweet.text).encode('ascii', 'ignore'))
            cleaned_tweet = re.sub("@\w+", "", cleanedtweet)
            vocabulary.append(cleaned_tweet)

        result = Bing().search(theme + " " + metaphor_source, start=1, count=50)
        for searchresult in result:
            s = searchresult.text.lower()
            s = plaintext(s)
            s = parsetree(s)
            p = '{NP} ' + metaphor_source + '{NP}'
            for m in search(p, s):
                vocabulary.append( m.group(2).string )

    return list(set(vocabulary))
# http://www.clips.ua.ac.be/pages/pattern-search
#get related vocabulary from theme : Pattern

def get_disambiguation(phrase, word):
#word-sense disembiguation in Python
# https://github.com/alvations/pywsd
    disambiguated = lesk(context_sentence=phrase, ambiguous_word=word)
    return disambiguated.definition()

def find_synonyms(word):
    synonyms = []
    for ss in wn.synsets(word):
        synonyms.append( ss.name().split(".")[0].replace('_', ' ') )
        for sim in ss.similar_tos():
            synonyms.append(sim.name().split(".")[0].replace('_', ' '))
    return list(set(synonyms))
# http://stackoverflow.com/questions/5534926/to-find-synonyms-defintions-and-example-sentences-using-wordnet

def count_syllables(phrase):
#could syllables : Pyphen
    dic = pyphen.Pyphen(lang='en_US')
    sentence = dic.inserted(phrase)
    return len(re.findall(r"[\w']+", sentence))
#from nltk_contrib.readability.textanalyzer import syllables_en
#print syllables_en.count("potatoes ")
# http://image.slidesharecdn.com/nltk-110105180423-phpapp02/95/nltk-natural-language-processing-in-python-22-728.jpg?cb=1309726267
# using PyPhen instead

def words_rhymes(word1, word2):
#detect rhymes : Metaphone
    word1_a, word1_b = doublemetaphone(word1)
    word2_a, word2_b = doublemetaphone(word2)
    return word1_a[-1] == word2_a[-1]
    # does not actually use the 2nd value... could use metaphone simple instead?

def syllables_matching_words_from_list(list_of_words,word):
    result = []
    for l in list_of_words:
        if count_syllables(l) == count_syllables(word):
            result.append(l)
    return result

def rhyming_words_from_list(list_of_words, word):
    result = []
    for l in list_of_words:
        if words_rhymes(l, word):
            result.append(l)
    return result

def spellcheck(text):
#spell check : Hunspell
    potential_mistakes = {}
    hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
    for word in re.findall(r"[\w']+", text):
        if not hobj.spell(word):
            potential_mistakes[word] = hobj.suggest(word)
    return potential_mistakes

def estimate_sentiment(text):
#sentiment analysis : Pattern sentiment()
    return sentiment(text)
    #useless so far, just a personal warpper
    # for meaning of values see http://www.clips.ua.ac.be/pages/pattern-en#sentiment

def replace_tag(text, tag, replacement):
    #replace the first found tag
    #print replace_tag("I want to eat an apple.", "NN", "orange")
    tokenized_sent = word_tokenize(text)
    pos_tagged = pos_tag(tokenized_sent)
    for t in pos_tagged:
        # print t
        if tag == t[-1]:
            return re.sub(t[0], replacement, text) 
    return text

def respect_structure(text, structure):
    # text is not a string but a list of verses
    if not len(text) == len(structure):
        print 'failed number of lines'
        return False
    for i,line in enumerate(text):
        if not count_syllables(line) == structure[i][0]:
                    # should be able to handle None too when syllable count does not matter
            print 'failed syllables'
            print i
            return False
        if not structure[i][1] == None:
            if not words_rhymes(line, text[structure[i][1]]):
                                # redundant test at corresponding later line
                print 'failed rhyming'
                print i
                return False
    return True
    # poor return value, unable to tell what failed

#should become a grammar respecting function
def respect_grammar(text, grammar):
#for grammatical rules
    tokenized_sent = word_tokenize(text)
    pos_tagged = pos_tag(tokenized_sent)
    testinggrammar = []
    for t in pos_tagged:
        testinggrammar.append(t[-1]) 
    return testinggrammar == grammar
    # http://image.slidesharecdn.com/nltk-110105180423-phpapp02/95/nltk-natural-language-processing-in-python-22-728.jpg?cb=1309726267

if __name__ == '__main__' :
    testwords = []
    for arg in sys.argv[1:]:
        testwords.append(arg)

    themes = ['Valentines', 'Relationship']
    nicknames = ['gingersnap', 'Beau bear']
    names = ['Alison', 'Beau']
    themes += ['Thirteenth']

    themes = ['bed', 'under', 'quest']
    names = ['Fabien']
    nicknames = ['Miss Moles']
    
    # include nicknames as potential synonym for each name
    print 'generating for :'
    print 'themes' + str(themes)
    print 'names' + str(names) + ' aka ' + str(nicknames)
    print '-------------------------------------------------'
    
    print "test words from the command line:"

    structures = {}
    structures['haiku3'] = [(5, None), (7, None), (5, None)]
    #structures['rhymetest'] = [(2,1),(2,0)]
                                # redundant test
    # structures have :
    #   metres or syllables
    #   stanza or lines or verses
    #   rhyme_form (e.g. current line rhymes with line 3)
    #               Python indexing, line 1 is in fact index 0
    # WARNING : better overdefine multiples versions of one structure than handle strange open cases!
    #           no free poetry but N different lines with N different rhymes
    #           kaiku3 haiku5 haiku7 for the different number of verses
    #           etc


    vocabulary_from_theme = {}
    for theme in themes:
        vocabulary_from_theme[theme] = get_vocabulary_from_theme(theme)
    #print 'vocabulary_from_theme' + str(vocabulary_from_theme)
    
    poems = []
    for structure in structures:
        poem = []
        pickedthemes = []
        print structure
        print "theoretical number of lines = " + str(len(structures[structure]))

        syllables = 0
        for line in structures[structure] : 
            syllables += line[0]
        print "theoretical number of syllables = " + str(syllables)

        # looping to adjust until
            # change to synonyms, names and nicknames
            # rhymes work
            # syllable count work
            # splitting in appropriate lines 
        for i in range(1, 30):
            picked_text = random.choice(vocabulary_from_theme[random.choice(themes)])
            picked_text = replace_tag(picked_text, "NNS", random.choice(names))
            picked_text = replace_tag(picked_text, "NN", random.choice(nicknames))
            if count_syllables(picked_text) < syllables :
                if count_syllables(picked_text) < syllables + 3 :
                    picked_text += random.choice(vocabulary_from_theme[random.choice(themes)])
                    picked_text = replace_tag(picked_text, "NNS", random.choice(names))
                else :
                    print "not such a big difference, should get a synonym for a name or adjective (JJ,JJS,JJR) but not implemented yet"
                    exit()

            # cut in 5 7 5
            #print picked_text
            dic = pyphen.Pyphen(lang='en_US')
            sentence = dic.inserted(picked_text)
            #print sentence
            allsyllables = re.findall(r"[\w']+", sentence)
            #print allsyllables
            #exit()
            
            poem_by_line = []
            for line in structures[structure] : 
                syllables_added = 0
                newline = ""
                while syllables_added <= line[0] and len(allsyllables) > 0:
                    #print allsyllables
                    ending_syllable = allsyllables.pop(0)
                    newline += ending_syllable  + " "
                    syllables_added += 1
                poem_cut = re.sub(ending_syllable+"?", ending_syllable+"\n", picked_text)
                poem_by_line.append( newline )
            #print picked_text
            print poem_by_line
            #print poem_cut 
            #not working well so far
        exit()

        for line_number in range(0, len(structures[structure])):
            #should pop themes to insure diversity
            picked_text = random.choice(vocabulary_from_theme[random.choice(themes)])
            if line_number > 0:
                if not structures[structure][line_number][-1] == None:
                    print "should check if it rhymes"
            #should pop names and nicknames to insure diversity
            picked_text = replace_tag(picked_text, "NNS", random.choice(names))
            if not structures[structure][line_number][0] == None:
                print "syllables ok: " + str( count_syllables(picked_text) == structures[structure][line_number][0] )
            poem.append(picked_text)
        for line in poem:
            print line

    #https://github.com/lekhakpadmanabh/Summarizer
    #summarize a text that is too long
    
    #Named Entity Recognition (NEs) in http://www.nltk.org/book/ch07.html
