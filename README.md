Scrape the web for data for NEC SAP POC.

The data is a json file of FBI data.  I use topten and fugitives to populate.

This is a rough cut as there are a lot of things not done!

This project contains 3 things:
1. a node app for view place of birth info on a map
2. a set of tools to scrape fugitive info from the FBI
3. a set of tools to format the fugitive data for the node app
4. a named entity recognizer
5. data files

#1
app.js = the node driver, web server
index.html = the web page
package.json = the node package file

#2
le.py = longExtract.py - this reads a data file and creates
      a json db with images and details of the fugitives
de.py = compiles a little data on the classifications of crimes
fbiwebscrape.py = the first version of le.py

#3
extract_place.py = reads the fbi_db.json file, writes list.csv
creategeo.py = experiments with geocoding

#4
ensemble.py = experiments in NER

#5
data-1.json = created by artoo (see le for instructions)
fbi_db.json = create by le
list.csv = created by extract_place.py

10/25/2016
