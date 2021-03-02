#!/usr/bin/env python
# coding: utf-8

# In[5]:


import xml.etree.ElementTree as ElementTree
import re
from nltk.stem import PorterStemmer


# In[6]:


word_unique = []
docno_dicts = {}    
#-----------------------------------reading stop word file to a list----------------------------------

stop_w=[]

with open('stopwordlist.txt', 'r') as f:   # Reading file
    stop_w.append( f.read().split())
    
#-----------------------------------the function that reads each file----------------------------------

def file_parser(filename): 
    with open(filename, 'r') as f:   
        xml = f.read()
        
    xml = '<ROOT>' + xml + '</ROOT>'   # adding a root tag
    root = ElementTree.fromstring(xml)
    #------------------------------counting number of documents-----------------------------------------
    
    doc_count=0
    
    for doc in root:
        doc_no=doc.find('DOCNO').text.strip()
        doc_count=doc_count+1
        
    #-----------------------------making a dictionary from numbers and names of document-----------------  
   
    keys = range(doc_count)
    i=len(docno_dicts)+1
    
    for doc in root:
            docno_dicts[i] = doc.find('DOCNO').text.strip()  
            i=i+1

    #-------------------------------reading all the text into 1 string------------------------------------
    
    text=""
    for doc in root:
        singl_text=doc.find('TEXT').text.strip()
        
     #------------------------------lowercasing every word-----------------------------------------------
    
        singl_text=singl_text.lower()        
        text+=singl_text
        
     #------------------------------spliting on every non-alphanumerical---------------------------------
     
    text= re.findall(r'\w+', text)   
   
    text = [''.join(x for x in i if x.isalpha()) for i in text]
    
    #----------------------------------removing stop words-----------------------------------------------

    text = [ele for ele in text if ele not in stop_w ]
    
    #----------------------------------removing empty spaces---------------------------------------------
    
    text = [ele for ele in text if ele != "" ]
   
    #--------------------------removing duplicates by making a new list using Potter Stemmer--------
   
    for j in text: 
        ps = PorterStemmer() 
        j=ps.stem(j)
        if j not in word_unique: 
            word_unique.append(j)         
   
 #-----------------------------reading and parsing each file--------------------------------
    
file_parser('ft911_1')
file_parser('ft911_2')
file_parser('ft911_3')
file_parser('ft911_4')
file_parser('ft911_5')
file_parser('ft911_6')
file_parser('ft911_7')
file_parser('ft911_8')
file_parser('ft911_9')
file_parser('ft911_10')
file_parser('ft911_11')
file_parser('ft911_12')
file_parser('ft911_13')
file_parser('ft911_14')
file_parser('ft911_15')

#---------------------making dictionary of words----------------------------------
word_dict={}
i=0
word_unique.sort()

for w in word_unique:
    word_dict[i] = w
    i=i+1
#--------------------writing the dictionaries to the file-------------------------    
with open('parser_output.txt', 'w') as f:    
    for key, value in word_dict.items():
        print(value,'\t', key,   file=f)
        
with open('parser_output.txt', 'a') as f:    
    for key, value in docno_dicts.items():
        print(value,'\t', key,   file=f)

