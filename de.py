import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from StringIO import StringIO
from PIL import Image
from sets import Set

fileName = 'data-1.json'
with open(fileName) as dat:
    js = json.load(dat)

aSet = Set()
for el in js:
    #
    # only want lines with a name on the end
    #
    element = el['url']
    fq = element.rpartition('/')[0]
    if fq.rpartition('/')[-1] == 'wanted':
        continue
    aSet.add(element)


classSet = {}
for el in aSet:
    classification = el.rpartition('/')[0].rpartition('/')[-1]
    if classification in classSet:
        classSet[classification] = classSet[classification] + 1
    else:
        classSet[classification] = 1


for el in classSet:
    print '{:25}:\t{}'.format(el, classSet[el])
