import xml.etree.ElementTree
import collections
import os, sys
from lxml import etree



"""
#############################################
Run inside the folder of TEI Song files.
Finds Chorus of every TEI file recursivly. 
#############################################
"""

def get_tree_stanzas(path):
    try:
        e = xml.etree.ElementTree.parse(path).getroot()[1][0][0]
    except:
        return []
    i=0
    ret=[]
    for x in e.findall('{http://www.tei-c.org/ns/1.0}lg'):
        i=i+1
        ret.append(x)
    return ret

def get_stanza_text(stanzas):
    ret=[]
    for stanza in stanzas:
        string=""
        for line in range(len(stanza)):
            string=string+stanza[line].text.lstrip().rstrip()+'\n'
        ret.append(string)
    return ret

def get_pizmon_stanzas(path):
    ret=[]
    #e = xml.etree.ElementTree.parse(path).getroot()[1][0][0]
    arr=get_stanza_text(get_tree_stanzas(path)) 
    try:
        piz= [item for item, count in collections.Counter(arr).items() if count > 1][0]
    except:
        print 'error'
        return None
    if len(piz.split('\n') )==2:
        return
    for i in enumerate(arr):
        if i[1]==piz:
            ret.append(i[0]+1)
    return ret


def get_pizmon_stanzas2(path):
    ret=[]
    arr=get_stanza_text(get_tree_stanzas(path))
    pizmon_string=""
    for stanza in arr:
        temp=stanza.split('\n')
        if len(temp)==2:
            if temp[0][-3:]=="...":
                pizmon_string= temp[0][:-3]
                

    if len(pizmon_string)==0:
        return
    
    for stanza in enumerate(arr):
        print stanza[1].find(pizmon_string)
        if stanza[1].find(pizmon_string)!=-1:
            ret.append(stanza[0]+1)
    
    print ret
    
    return ret


def find_chorus(path):
    
    print path
    pizmons= get_pizmon_stanzas(path) 
    xml.etree.ElementTree.register_namespace('', "http://www.tei-c.org/ns/1.0")
    tree = xml.etree.ElementTree.parse(path)
    root = tree.getroot()
    try:
        e = root[1][0][0]
    except:
        return
    if pizmons==None :
        pizmons=get_pizmon_stanzas2(path)
        print pizmons
    if pizmons!=None:
        for i,rank in enumerate(e.iter('{http://www.tei-c.org/ns/1.0}lg')):
            if i in pizmons:
                rank.set('Chorus', 'yes')
        tree.write(path,encoding='utf-8')


def add_publishers(subdirectories):

    for artists in subdirectories:
        artist=os.listdir(artists)
        for song in artist:
            if song not in [ u'.DS_Store',u'.settings',u'Chorus.py',u'Chorus.pyc']:
                print song
                xml.etree.ElementTree.register_namespace('', "http://www.tei-c.org/ns/1.0")
                path='./'  + artists +'/'+ song
                tree = xml.etree.ElementTree.parse(path)
                root = tree.getroot()
                publicationStmt = root[0][0][1]
                publisher = xml.etree.ElementTree.SubElement(publicationStmt, u'publisher')
                publisher.text = "Yoav Cohen and Maya Ben Tov, Ben-Gurion University"
                #publicationStmt.append(xml.etree.ElementTree.Element(u'publisher'))
                #publicationStmt[1].text = "Yoav Cohen and Maya Ben Tov, Ben-Gurion University"
                tree.write(path, encoding='utf-8') 
                tree2 = etree.parse(path)
                tree2.write(path, pretty_print=True, encoding='utf-8')
                try:
                    find_chorus(path) 
                except:
                    print "error"
                

subdirectories = [d for d in os.listdir('./') if os.path.isdir(os.path.join('./', d))]
add_publishers(subdirectories)






