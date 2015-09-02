#!/usr/bin/env python


from lxml import etree


tree = etree.parse(open('Data/bookstore.xml'))
#root = tree.getroot()

r = tree.xpath("//book[@category='WEB']")
print len(r)

for i in r:
    title = i.xpath('title')[0]
    author = i.xpath('author')
    print "TAG: {0}\nAUTHOR: {1}\n".format(title.text, author[0].text)
