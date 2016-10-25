"""
LongExtract

Process the output from artoo scraper and create a json file

This will process a small json file of urls from the FBI wanted list.

The output is a json file with about 250 people listed. Info about them like
name, hair color, place of birth and image are captured.

 use artoo with this command
 var tab = artoo.scrape('.wanted-feature-grid a',
  {url: "href", title: "text"});
 artoo.savePrettyJson(tab)

This file currently reads from data-1.json and writes 'fbi_db.json'

This file also gathers image data. This data is stored in 'fbi_db.json'
and in a directory named: 'images2/'
"""

import requests
import sys
from bs4 import BeautifulSoup
import json

from StringIO import StringIO
from PIL import Image
from sets import Set
import base64


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

outf = open('fbi_db.json', 'wb')

badguyDetail = {}  # init a dictionary
i = 0
for el in aSet:
    print el  # debug info
    try:
        #
        # get the badguy's name
        #
        badguyName = el.rpartition('/')[-1]
        badguyDetail['name'] = badguyName
        #
        # get the image for the badguy
        #
        badguyPic = requests.get(el + '/@@images/image/preview')
        img = Image.open(StringIO(badguyPic.content))
        imgFileName = './images2/' + badguyName + '.jpg'
        img.save(imgFileName)
        #
        # render the image into a string
        #  and put that in the db
        #
        imgString = base64.b64encode(badguyPic.content)
        badguyDetail['image'] = imgString
        #
        # now process the detail table
        #
        detail = requests.get(el)
        soup = BeautifulSoup(detail.text)
        #
        # extract the alias info
        #
        aliasS = soup.select('.wanted-person-aliases')
        if aliasS:
            alias = str(aliasS)[str(aliasS).index('<p>') + 3:
                                str(aliasS).index('</p>')]
            badguyDetail['alias'] = alias
        #
        # go find the table with the detailed data about the person
        #
        tab = soup.select('tbody')
        els = str(tab).split('<td>')
        lst = []
        """ loop over each table entry
              extract the date of birth, place of Birth, Hair, eyes, ...
        """
        for it in els:
            if '</td>' in it:
                lst.append(it[0:it.index('</td>')])

        for jj in range(0, len(lst), 2):
            badguyDetail[lst[jj]] = lst[jj+1]
        """
        Gather the remarks for this entity
        """
        remarks = soup.select('.wanted-person-remarks')
        if remarks:
            remarks_text = str(remarks)[str(remarks).index('<p>') + 3:
                                        str(remarks).index('</p>')]
            badguyDetail['remarks'] = remarks_text
        """
        gather the cautionary info on this entity
        """
        caution = soup.select('.wanted-person-caution')
        if caution:
            caution_text = str(caution)[str(caution).index('<p>') + 3:
                                        str(caution).index('</p>')]
            badguyDetail['caution'] = caution_text
        #
        # write that record out to the file
        #
        strg = json.dumps(badguyDetail) + '\n'
        outf.write(strg)
        badguyDetail.clear()
    except:
        e = sys.exc_info()[0]
        print 'err: {}::{}\n'.format(e, el)
outf.close()
