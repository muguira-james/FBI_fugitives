import requests
from bs4 import BeautifulSoup
import json
from StringIO import StringIO
from PIL import Image

"""
  Use this code to get the raw html from the FBI
"""
fbiFugitives = requests.get("https://www.fbi.gov/wanted/fugitives")

file = open('fbi_wanted.html', 'wb')
for chunk in fbiFugitives.iter_content(100000):
    file.write(chunk)

file.close()
soup = BeautifulSoup(fbiFugitives.text)
"""
  Use this code if you read it from a file

fbiFugitives = open('fbi_wanted.html', 'rb').read()
soup = BeautifulSoup(fbiFugitives)
"""

data = soup.select('.focuspoint')
print len(data)
#
# the json dictionary
#
detailsD = {}
#
# loop over the data
#
for item in data:
    badguyDetail = {}
    #
    # split off the detail url and the image info
    #
    faq, image = item['data-base-url'].split('@@')
    #
    # build the image file name from the data
    #
    badguy = requests.get(item['data-base-url'])
    img = Image.open(StringIO(badguy.content))
    fileName = './images/' + faq.rpartition('/')[0].rpartition('/')[2] + '.jpg'
    img.save(fileName)
    badguyDetail['imageFile'] = fileName
    #
    print faq
    detail = requests.get(faq)
    soup2 = BeautifulSoup(detail.text)
    #
    # extract the alias info
    #
    aliasS = soup2.select('.wanted-person-aliases')
    if aliasS:
        alias = str(aliasS)[str(aliasS).index('<p>') + 3:
                            str(aliasS).index('</p>')]
        #
        badguyDetail['alias'] = alias
    #
    # go find the table with the detailed data about the person
    #
    tab = soup2.select('tbody')
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
    remarks = soup2.select('.wanted-person-remarks')
    if remarks:
        remarks_text = str(remarks)[str(remarks).index('<p>') + 3:
                                    str(remarks).index('</p>')]
        badguyDetail['remarks'] = remarks_text
    """
    gather the cautionary info on this entity
    """
    caution = soup2.select('.wanted-person-caution')
    if caution:
        caution_text = str(caution)[str(caution).index('<p>') + 3:
                                    str(caution).index('</p>')]
        badguyDetail['caution'] = caution_text
    """
    Print out the dictionary for debug testing
    """
    detailsD[faq.rpartition('/')[0].rpartition('/')[2]] = badguyDetail

outf = open('fbi_db.json', 'wb')
outf.write(json.dumps(detailsD))
outf.close()
