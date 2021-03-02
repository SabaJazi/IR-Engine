#!/usr/bin/env python
# coding: utf-8

# In[7]:


import xml.etree.ElementTree as ElementTree
import re
from nltk.stem import PorterStemmer
import numpy as np
import os 


# In[8]:




word_unique = []
docno_dicts = {} 
#-----------reading parser output-------------------
word_list={}

with open('parser_output.txt', 'r') as f:   
    for line in f:
        (key, val) = line.split()
        word_list[key] = val

#-----------------------------------reading stop word file to a list----------------------------------

stop_w=[]

with open('stopwordlist.txt', 'r') as f:
    stop_w = f.read().split()
 

 #-----------------------------------the function that reads each file----------------------------------

def Indexer(filename): 
    with open(filename, 'r') as f:   
        xml = f.read()
        
    xml = '<ROOT>' + xml + '</ROOT>'   # adding a root tag
    root = ElementTree.fromstring(xml)
    
 #------------------------------counting number of documents-----------------------------------------    
    doc_count=0
    
    for doc in root:
        doc_no=doc.find('DOCNO').text.strip()
        doc_count=doc_count+1   
        
        
    
#------------------------------counting occurance of each word in each document----------   
    
    for doc in root:
          
        doc_no=doc.find('DOCNO').text.strip()
        
        text_string=doc.find('TEXT').text.strip()
        text_string=text_string.lower() 
        text_string= re.findall(r'\w+', text_string) 
        text_string = [ele for ele in text_string if ele not in stop_w ]
        text_string = [ele for ele in text_string if not any(c.isdigit() for c in ele)]
        
        dictionary = {}
        #-------------------------porter stemmer to stem and remove duplicates----------
        for elements in text_string: 
            ps = PorterStemmer() 
            elements=ps.stem(elements)
            if elements in word_list:
                         word_id=int(word_list[elements])
        #-------------------------making dictionary of frequency of each word in doc---------   
            
            if word_id in inverted_index.keys():
                if doc_no in inverted_index[word_id].keys():
                    inverted_index[word_id][int(word_list[doc_no])] += 1
                else: 
                    inverted_index[word_id].update({int(word_list[doc_no]): 1})
            else:
                inverted_index[word_id] = {} 
                inverted_index[word_id][int(word_list[doc_no])]= 1
            
            if word_id in dictionary.keys(): 
                dictionary[word_id]+= 1
            else: 
               
                dictionary[word_id]= 1 
                
        #------------making dictionary of dictionaries of each doc---------------        
        forward_index[doc_no] = dictionary 
        
        

    


# In[3]:


#-----------------------------------making forward and inverted index----------------------------

DOC_DIR = './IR-Documents/'

forward_index ={}
inverted_index={}
for file_name in os.listdir(DOC_DIR):
    Indexer(DOC_DIR + file_name)
    
    
with open('forward_index.txt', 'w') as f:    
    for key, value in forward_index.items():
        print(word_list[key],'\t',str(value)[1:-1] ,'\n',   file=f) 
        
with open('inverted_index.txt', 'w') as f:    
    for key, value in inverted_index.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)
       


# In[11]:


#------------------------------------------search function---------------------------------------

                    #------------preprocessing the search string---------------
def search_word(search_string):
    search_term=search_string
    search_term=search_term.lower()        
    search_term= re.findall(r'\w+', search_term)        
    search_term = [ele for ele in search_term if not any(c.isdigit() for c in ele)]

#-------------stemming the search term---------------
    u_search_term=[]
    for word in search_term:
        ps = PorterStemmer() 
        stemmed_w=ps.stem(word)
        u_search_term.append(stemmed_w)
    w_str=""
 
    for ele in u_search_term: 
         w_str += ele  
 
    
    if w_str in stop_w:
        print("the word :"+ w_str+ "is in stop word list.")
    else:
        
        search_id=0 
        FW_INDX_DIR = './IR-FW/'
        INV_INDX_DIR='./IR-INV/'


        #-----------reading parser output-------------------
    
        with open('parser_output.txt', 'r') as f: 
            for line in f:
                if w_str in line:
                    (key, val) = line.split()
                    if key == w_str:
                        search_id=val                                         

        output=""
        with open("./IR-INV/inverted_index.txt", "r") as f:
            for line in f:
                if search_id in line:
                    output=line
                
        if output!="":
            print("\nThe result from inverted index is :\n")
            word_id,index_list =output.split("\t")
            print("word id is: "+ word_id+"\n")
            print("index information : "+ index_list)
        else:
            print("this word was not found.")


# In[13]:


#--------------------searching interface---------------------------------

search_term = input ("Please enter your search term :\n") 
search_word(search_term)


# In[ ]:




