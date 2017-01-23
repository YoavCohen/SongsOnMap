#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Pool, TimeoutError
import xml.etree.ElementTree
import collections
import os, sys
import requests
from bs4 import BeautifulSoup
import lxml
from Chorus import get_stanza_text , get_tree_stanzas
from _collections import defaultdict
from _random import Random
import random
import unicodecsv as csv
import youtube
from youtube import youtube_search

def find_places(text):
    ret=defaultdict(list)
    url='http://yeda.cs.technion.ac.il:8088/MWE/analysis.jsp'
    payload ={'input_text': text}
    print "step in"
    r= requests.post(url,timeout=50,data=payload)
    print "step out"
    content= r.content
    soup = BeautifulSoup(content, "xml")
    for sentence in soup.find_all('sentence'):
        sent=""
        for token in sentence:
            sent=sent+' '+token['surface']
            sent=sent.replace('.' ,'')
        for token in sentence.find_all('token'):
            for analysis in  token.find_all('analysis'):
                if analysis.has_attr('score'):
                    if analysis['score']=='1.0' :##or '0.5':
                        try:
                            type=analysis.find('base').find('properName')['type'] 
                            if type== 'town' or type == 'country' or type=='location':
                                ret[(analysis.find('base')['lexiconItem'])].append(sent) 
                                print analysis.find('base')['lexiconItem']
                        except:
                            pass
                        try:
                            type=analysis.find('base').find('MWE')['type'] 
                            if type == 'town' or type == 'country' or type =='location':
                                print analysis.find('base').find('MWE')['multiWordUndotted']
                                ret[(analysis.find('base').find('MWE')['multiWordUndotted'])].append(sent)
                        except:
                            pass
    return ret

def locate_places_by_bounds(place):
    url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + place
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.content, 'xml')
    try:
        geometry = soup.find('geometry')
        viewport = geometry.find('viewport')
        southwest = viewport.find('southwest')
        sw_lat = float(southwest.find('lat').text)
        sw_lng = float(southwest.find('lng').text)
        northeast = viewport.find('northeast')
        ne_lat = float(northeast.find('lat').text)
        ne_lng = float(northeast.find('lng').text)
        lat= random.uniform(sw_lat,ne_lat)
        lng =random.uniform(sw_lng,ne_lng)
    except:
        return (None,None)
    
    return  (lat,lng)
    



def locate_places(place):
    url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + place
    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.content, 'xml')
    try:
        geometry = soup.find('geometry')
        location = geometry.find('location')
        sw_lat = float(location.find('lat').text)
        sw_lng = float(location.find('lng').text)
        up_or_down=random.uniform(0.0,1.0)
        left_or_right=random.uniform(0.0,1.0)
        if(up_or_down>0.5):
            pass
        
        
        
    except:
        return (None,None)
    
    return  (lat,lng)




with open('test.csv', 'a') as csv_file:
    csvfile = csv.writer(csv_file, quoting=csv.QUOTE_ALL,encoding='utf-8')
    csvfile.writerow([u'אמן', u'שיר',u'מקום',u'משפטים',u'lat',u'lng',u'youtube'])
    subdirectories = [d for d in os.listdir('./') if os.path.isdir(os.path.join('./', d))]

    for artists in subdirectories:
        artist=os.listdir(artists)
        for song in artist:
            print song
            if song!='.DS_Store': 
                if artists != '.settings':
                    path='./'  + artists +'/'+ song
                    print path
                    arr = get_stanza_text(get_tree_stanzas(path))
                    string=""
                    for x in arr:
                        string=string+x
                    dic =find_places(string.replace('\n','.\n'))
                    for place in dic.keys():
                        if place in [u'אספר',u'ראשון',u'שהם',u'שבא',u'אדום',u'בצרה',u'תקוע',u'גן עדן',u'מולדת',u'שבלי',u'מוצא',u'כנף',u'נשר']:
                            continue   
                        lat,lng = locate_places_by_bounds(place)
                        if (lat,lng) !=(None,None):
                            all_sentences=""
                            for sent in dic[place]:
                                all_sentences=all_sentences+'"'+sent+'"'+'\n'
                            youtubeurl= youtube_search(artists+song[:-4])
                            csvfile.writerow([artists,song[:-4],place,all_sentences,lat,lng,youtubeurl])