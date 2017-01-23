#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import subprocess
import requests
from bs4 import BeautifulSoup
import cookielib, urllib2, sys
import cookielib
import codecs
import io
import os
import json
from _codecs import encode
from warnings import catch_warnings
reload(sys)
import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from lxml import etree
import time
import pickle
from multiprocessing import Process

class song(object):
    
    def song(self):
        song=[]
    
    def addStanza(self,stanza):
        song.append(stanza)
    
    def getStanza(self,num):
        song.get(num)
    

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring("zz", 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def get_lyrics(url,job):
    
    
    
    #Create the tei structure:

    above = Element(u'TEI', xmlns="http://www.tei-c.org/ns/1.0")

    # <teiHeader>
    tei_header = SubElement(above, u'teiHeader')
    
    # <teiHeader><fileDesc>
    file_desc = SubElement(tei_header, u'fileDesc')
      
    # <teiHeader><fileDesc><titleStmt>
    title_stmt = SubElement(file_desc, u'titleStmt')
        
    # <teiHeader><fileDesc><titleStmt><title>
    title = SubElement(title_stmt, u'title').text=url[url.find('/', 28)+1: ].replace('-',' ').decode('utf-8')
    
    
    # <teiHeader><fileDesc><titleStmt><singer>
    

    if job == u'זמר':
        classification = u'male singer'
    elif job == u'זמרת':
        classification = u'female singer'
    elif job == u'להקה':
        classification = u'band'
    elif job ==u'DJ':
        classification = u'DJ'
    else:
        classification = u'unknown'
    
    singer = SubElement(title_stmt, u'singer', classification=classification).text=url[28:url.find('/', 28)].replace('-',' ').decode('utf-8')
        
    # <teiHeader><fileDesc><titleStmt><writer>
    writer = SubElement(title_stmt, u'writer')

    # <teiHeader><fileDesc><titleStmt><composer>
    composer = SubElement(title_stmt, u'composer')

    # <teiHeader><fileDesc><titleStmt><album>
    album = SubElement(title_stmt, u'album')    
        
    # <teiHeader><fileDesc><publicationStmt>
    publication_stmt = SubElement(file_desc, u'publicationStmt')
        
    # <teiHeader><fileDesc><publicationStmt><date>
    date = SubElement(publication_stmt, u'date').text=u'2016'
        
    # <teiHeader><fileDesc><sourceDesc>
    source_desc = SubElement(file_desc, u'sourceDesc')
        
    # <teiHeader><fileDesc><sourceDesc><p>
    p = SubElement(source_desc, u'p').text=u'The website SongLyrics: http://songlyrics.co.il'
        
    # <teiHeader><profileDesc>
    profile_desc = SubElement(tei_header, u'profileDesc')
        
    # <teiHeader><profileDesc><langUsage>
    lang_usage = SubElement(profile_desc, u'langUsage')
        
    # <teiHeader><profileDesc><langUsage><language>
    language = SubElement(lang_usage, u'language', ident=u'he').text=u'Hebrew'
        
        
    # <text>
    tei_text = SubElement(above, u'text')
        
    # <text><body>
    text_body = SubElement(tei_text, u'body')
        
    # <text><body><lg type="song lyrics">
    type_song = SubElement(text_body, u'lg', type=u'song lyrics')
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #f.write( soup.p.text.replace("                                                ", "").encode('utf8'))
    if len(soup.find_all("p", class_="writerComposer"))>0:
        writer_composer = soup.find_all("p", class_="writerComposer")[0].getText() ##change here
    else:
        writer_composer='missing'
    try:
        artist=soup.findAll('h3')[0].text
        song_name=soup.findAll('h1')[0].text
    except:
        return
    print writer_composer
    print song_name
    # divide to writer and composer by location of comma, if exists
    commaLocation = writer_composer.find(',')
    if commaLocation>0:
        writer.text = writer_composer[ 7:commaLocation].replace('-',' ')
        composer.text = writer_composer[commaLocation+7: ].replace('-',' ')
        if composer.text==u'קיים ביצוע נוסף לשיר זה':
            composer.text="missing"
    else:
        writer.text = writer_composer[7:]
        composer.text = 'missing'
    
    # <text><body><lg type="song lyrics"><head>
    song_head = SubElement(type_song, u'head').text=song_name
    
    h4s= soup.findAll('h4')
    if not h4s: # album name is missing
        album.text = 'missing'
    for h4 in h4s:
        for link in h4.find_all('a'):
            album.text =  link.getText() ##album 
            print album.text
                   
    lyrics= soup.p.text.replace("                                                ", "").replace('\r', '').encode('utf8').split('\n')
    num_of_rows=len(lyrics)
    ##sometimes last lines are blank
    if len(lyrics[num_of_rows-1]) == 0 and len(lyrics[num_of_rows-2]) == 0:
        lyrics=lyrics[:num_of_rows-2]
    i=1
    stanza = SubElement(type_song, u'lg', type=u'stanza', number=str(i))
    #song=""
   # my_song=song()
    for sentence in lyrics[1:]:
        ##last sentence sometimes just spaces
        if sentence.isspace(): 
            continue
        ## insert lines and stanzas to structure
        elif len(sentence) == 0: ## a new stanza
            i=i+1
            stanza = SubElement(type_song, u'lg', type=u'stanza', number=str(i))
        else:
            SubElement(stanza, u'l').text=sentence.decode('utf-8')
        #song=song+'\n'+sentence   
    #save unpreety xml
    import uuid
    id=uuid.uuid1()
    ET.ElementTree(above).write(str(id),encoding="UTF-8",xml_declaration=True)
    tree = etree.parse(str(id))
    subprocess.call(['rm', str(id)])
    subprocess.call(['mkdir','-p', artist])
    tree.write(artist+'/'+song_name.replace('/','-')+".xml", pretty_print=True, encoding='utf-8')
    
    #output_file.close()


def get_artist(url,dic):
    name= url[28:].replace('-',' ')
    try:
        job= dic[name.decode('utf-8')][0]
    except:
        job=None
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for node in soup.findAll(itemprop="url",href=True):
        song_page='http://www.songlyrics.co.il'+node.get('href').encode('utf-8')
        get_lyrics(song_page,job)
    r.close()


def get_letter(url,dic):
    #find how many pages
    startadr= url
    adr=startadr+str(1)
    print adr
    req = urllib2.Request(adr.encode('utf-8'))
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(the_page, 'html.parser')
    list= soup.find_all('ul', {'class': 'clearfix'})
    listli=list[0].find_all('li')
    
    for i in range(1,int(listli[4].text)+1):
        adr=startadr+str(i)
        req = urllib2.Request(adr)
        response = urllib2.urlopen(req)
        the_page = response.read()
        soup = BeautifulSoup(the_page, 'html.parser')
        h3s= soup.findAll('h3')
        for h3 in h3s:
            for link in h3.find_all('a'):
                print "now starting to crawl " +link.get('href').encode('utf-8')
                artist_page='http://www.songlyrics.co.il'+link.get('href').encode('utf-8')
                get_artist(artist_page,dic)
        response.close()

import unicodecsv as csv
def get_place(place,artist,title):
    adr='https://maps.googleapis.com/maps/api/geocode/json?address='+place
    response=requests.get(adr)
    z=json.loads(response.text)
    if len(z['results'])>0:
        print z['results'][0]['address_components'][0]['long_name']
        with open('fusiontable.csv', 'a') as csv_file:
            bale_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL,encoding='utf-8')
            bale_writer.writerow([z['results'][0]['address_components'][0]['long_name'],artist,title])

        
def mooma(adr,dic):
    """get adress of letter in moma and return dic [name : jobs]
    """
    next=None
    response=requests.get(adr, timeout=20)
    response.encoding='cp1255'
    soup = BeautifulSoup(response.text, 'html.parser')
    #f.write( soup.p.text.replace("                                                ", "").encode('utf8'))
    artists = soup.find_all('a')
    for artist in artists:
        href=artist.get('href')
        if href[:6]=="artist":
            try:
                art=requests.get("http://mooma.mako.co.il/"+artist.get('href'), timeout=20)
            except:
                continue
            art.encoding='cp1255'
            soup2 = BeautifulSoup(art.text, 'html.parser')
            name= soup2.find_all("td", class_="TopItemHeaderBlack")[1].text.replace("\n","").replace("\r","").replace("\t","")
            if len(name)==0:
                name= soup2.find_all("td", class_="TopItemHeaderBlack")[0].text.replace("\n","").replace("\r","").replace("\t","")
            if name[len(name)-1]==' ':
                name=name[:len(name)-1]
            print name
            ##print type
            job= soup2.find_all("td", class_="TopItemHeaderGray14")[0].text.replace("\n","").replace("\r","").replace("\t","")
            jobs= job.split(' ,')
            dic[name]=jobs
            for x in jobs:
                print x
            
            #if len(soup2.find_all("td", class_="TopItemSmallText"))>0:
             #   print soup2.find_all("td", class_="TopItemSmallText")[0].text.replace("\n","").replace("\r","").replace("\t","")

            if( soup2.find_all("td", class_="TopItemHeaderGray14")[0].text.replace("\n","").replace("\r","").replace("\t","")==u'זמר'):
                pass
        elif artist.text==u'הבא' and href[:16]=="Moomaindex.asp?p":
            #print href[:16]
            next=href
        
    if next is not None:
        print 'http://mooma.mako.co.il/'+next
        mooma('http://mooma.mako.co.il/'+next , dic)
    return dic
    


def get_mooma_info():
    """return a dic with info from and save it to a file
    """
    letters=['alef','bet','gimel','daled','he','vav','zz','het','tet','yod','kaf','lamed','mem','nun','sameh','eye','pe','zadik','kof','resh','shin','taf']
    dic={}
    for letter in letters:
        dic=mooma("http://mooma.mako.co.il/moomaindex.asp?Letter="+letter, dic)
        dic=mooma("http://mooma.mako.co.il/Moomaindex.asp?Type=2&letter="+letter,dic)
        dic=mooma("http://mooma.mako.co.il/Moomaindex.asp?Type=3&letter="+letter,dic)
    output = open('moomadic.txt', 'ab+')
    pickle.dump(dic, output)
    output.close()
    return dic





#array for all hebrew letters
z=['90','91','92','93','94','95','96','97','98','99','9B','9C','9E','A0','A1','A2','A4','A6','A7','A8','A9','AA']
#z=['91']
url='http://www.songlyrics.co.il/%D7%90%D7%9E%D7%A0%D7%99%D7%9D/%D7%'
dic = pickle.load(open("moomadic.txt", "rb"))


for i in z:
    testurl=url+i+'?page='
    print testurl
    p = Process(target=get_letter, args=(testurl,dic))
    p.start()





