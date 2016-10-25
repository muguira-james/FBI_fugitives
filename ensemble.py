import sys
import nltk
from polyglot.text import Text
from sets import Set

# first readin the file
if len(sys.argv) <= 0:
    sys.exit()

file = sys.argv[1]

text_raw = open(file, 'rb').read()
text = unicode(text_raw, errors='ignore').encode('UTF-8', 'ignore')

# now setup for parseing
# this creates an array of sentences
sentences = nltk.sent_tokenize(text)

tup = Set()
for sentence in sentences:
    # print nltk.word_tokenize(sentence)
    nz = nltk.ne_chunk(
            nltk.pos_tag(
                nltk.word_tokenize(sentence)), binary=False)


    for el in nz.subtrees(lambda e:
                          e.label() == 'ORGANIZATION' or
                          e.label() == 'PERSON' or
                          e.label() == 'LOCATION' or
                          e.label() == 'QUANTITY' or
                          e.label() == 'DATE' or
                          e.label() == 'TIME' or
                          e.label() == 'MONEY' or
                          e.label() == 'PERCENT' or
                          e.label() == 'GPE'):
        print el
    print '------------------------------------'
    """
    for el in nz.subtrees(lambda e: e.label() == 'NE'):
    """


    pz = Text(sentence).entities
    print pz
    print '================================'
