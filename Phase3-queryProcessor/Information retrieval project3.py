#!/usr/bin/env python
# coding: utf-8

# In[2]:


import xml.etree.ElementTree as ElementTree
import re
from nltk.stem import PorterStemmer
import numpy as np
import os 
import itertools
#from collections import OrderedDict 


# In[20]:




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
 

 #-----------------------------------the function that reads each document file----------------------------------

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
        #-------------------------making dictionary of frequency of each word in doc-----+df----   
            
            if word_id in inverted_index.keys():
                if doc_no in inverted_index[word_id].keys():
                    inverted_index[word_id][int(word_list[doc_no])] += 1
                else: 
                    inverted_index[word_id].update({int(word_list[doc_no]): 1})            
                    df_dict[word_id]=+1
                  
                        
            else:
                inverted_index[word_id] = {} 
                inverted_index[word_id][int(word_list[doc_no])]= 1
                df_dict[word_id]= 1 
            
            if word_id in dictionary.keys(): 
                dictionary[word_id]+= 1
            else: 
               
                dictionary[word_id]= 1 
                
        #------------making dictionary of dictionaries of each doc---------------  
        
        forward_index[doc_no] = dictionary 
        #-------------------------making tf--------------
       
       # for key in forward_index:
        #tf_dict[key]=dictionary[key]/float(len(dictionary)) 
    #-------------now all the documents are processed and forward+ invert+df are complete--------
    for d_num in forward_index.keys():
        tf_idf_dict[word_list[d_num]]={}
        for w_id in forward_index[d_num].keys():
            tf_idf_dict[word_list[d_num]][w_id]=float(round((forward_index[d_num][w_id])*(np.log((doc_count)/df_dict[w_id])),2))
            
    
            
    
        

    


# In[237]:


title=[]
desc=[]
narr=[]


 #-----------------------------------the function that reads each query file----------------------------------

def q_Indexer(filename): 
    with open(filename, 'r') as f:   
        xml = f.read()
   
    result=xml.split("<top>")
    q_count=len(result)
    #--------making a dictionary of query numbers and their ids-----------------------------
    for i in range(1,len(result)):

        _void, str1=result[i].split("<num> Number:")
        q_num, str1=str1.split("<title>")
        q_num=int(q_num.strip())
        q_num_id[q_num]=i  
        q_num_id2[q_num]=i  
        q_num_id3[q_num]=i  
    #------------------------------------------------
    for i in range(1,len(result)):
        
        _void, str1=result[i].split("<num> Number:")
        q_num, str1=str1.split("<title>")
        q_num=int(q_num.strip())
        __title, str1=str1.split(r"<desc> Description:")
        __desc, str1=str1.split("<narr> Narrative: ")
        __narr,__void =str1.split("</top>")
        
        text_string2=__title +__desc
        text_string3=__title + __narr
        
        text_string=__title.lower() 
        text_string2=text_string2.lower() 
        text_string3=text_string3.lower() 
        
        
        text_string= re.findall(r'\w+', text_string) 
        text_string2= re.findall(r'\w+', text_string2) 
        text_string3= re.findall(r'\w+', text_string3) 
        
        text_string = [ele for ele in text_string if ele not in stop_w ]
        text_string2 = [ele for ele in text_string2 if ele not in stop_w ]
        text_string3 = [ele for ele in text_string3 if ele not in stop_w ]
        
        text_string = [ele for ele in text_string if not any(c.isdigit() for c in ele)]
        text_string2 = [ele for ele in text_string2 if not any(c.isdigit() for c in ele)]
        text_string3 = [ele for ele in text_string3 if not any(c.isdigit() for c in ele)]
        
            
#------------------------------counting occurance of each word in each query----------   
        
        dictionary = {}
        #-------------------------porter stemmer to stem and remove duplicates----------
        for elements in text_string: 
            ps = PorterStemmer() 
            elements=ps.stem(elements)
            if elements in word_list:
                         word_id=int(word_list[elements])
        #-------------------------making dictionary of frequency of each word in doc-----+df----   
            
            if word_id in q_inverted_index.keys():
                if q_num in q_inverted_index[word_id].keys():
                    q_inverted_index[word_id][int(q_num_id[q_num])] += 1
                else: 
                    q_inverted_index[word_id].update({int(q_num_id[q_num]): 1})            
                    q_df_dict[word_id]=+1
                  
                        
            else:
                q_inverted_index[word_id] = {} 
                q_inverted_index[word_id][int(q_num_id[q_num])]= 1
                q_df_dict[word_id]= 1 
            
            if word_id in dictionary.keys(): 
                dictionary[word_id]+= 1
            else: 
               
                dictionary[word_id]= 1 
                
        #------------making dictionary of dictionaries of each query---------------  
        
        q_forward_index[q_num] = dictionary 
        
        #------------------------------option 2----------------
        dictionary2 = {}
        for elements in text_string2: 
            ps = PorterStemmer() 
            elements=ps.stem(elements)
            if elements in word_list:
                         word_id=int(word_list[elements])
        #-------------------------making dictionary of frequency of each word in doc-----+df----   
            
            if word_id in q_inverted_index2.keys():
                if q_num in q_inverted_index2[word_id].keys():
                    q_inverted_index2[word_id][int(q_num_id2[q_num])] += 1
                else: 
                    q_inverted_index2[word_id].update({int(q_num_id2[q_num]): 1})            
                    q_df_dict2[word_id]=+1
                  
                        
            else:
                q_inverted_index2[word_id] = {} 
                q_inverted_index2[word_id][int(q_num_id2[q_num])]= 1
                q_df_dict2[word_id]= 1 
            
            if word_id in dictionary2.keys(): 
                dictionary2[word_id]+= 1
            else: 
               
                dictionary2[word_id]= 1 
                
        #------------making dictionary of dictionaries of each query---------------  
        
        q_forward_index2[q_num] = dictionary2
        
        #------------------------------option 3----------------
        dictionary3 = {}
        for elements in text_string3: 
            ps = PorterStemmer() 
            elements=ps.stem(elements)
            if elements in word_list:
                         word_id=int(word_list[elements])
        #-------------------------making dictionary of frequency of each word in doc-----+df----   
            
            if word_id in q_inverted_index3.keys():
                if q_num in q_inverted_index3[word_id].keys():
                    q_inverted_index3[word_id][int(q_num_id3[q_num])] += 1
                else: 
                    q_inverted_index3[word_id].update({int(q_num_id3[q_num]): 1})            
                    q_df_dict3[word_id]=+1
                  
                        
            else:
                q_inverted_index3[word_id] = {} 
                q_inverted_index3[word_id][int(q_num_id3[q_num])]= 1
                q_df_dict3[word_id]= 1 
            
            if word_id in dictionary3.keys(): 
                dictionary3[word_id]+= 1
            else: 
               
                dictionary3[word_id]= 1 
                
        #------------making dictionary of dictionaries of each query---------------  
        
        q_forward_index3[q_num] = dictionary3
        
        
    #-------------now all the documents are processed and forward+ invert+df are complete--------
    for q_num in q_forward_index.keys():
        q_tf_idf_dict[q_num_id[q_num]]={}
        for w_id in q_forward_index[q_num].keys():
            q_tf_idf_dict[q_num_id[q_num]][w_id]=float(round((q_forward_index[q_num][w_id])*(np.log((q_count)/q_df_dict[w_id])),2))
            
   #-------------now all the documents are processed and forward+ invert+df are complete--------
    for q_num in q_forward_index2.keys():
        q_tf_idf_dict2[q_num_id2[q_num]]={}
        for w_id in q_forward_index2[q_num].keys():
            q_tf_idf_dict2[q_num_id2[q_num]][w_id]=float(round((q_forward_index2[q_num][w_id])*(np.log((q_count)/q_df_dict2[w_id])),2))
            
     
  #-------------now all the documents are processed and forward+ invert+df are complete--------
    for q_num in q_forward_index3.keys():
        q_tf_idf_dict3[q_num_id3[q_num]]={}
        for w_id in q_forward_index3[q_num].keys():
            q_tf_idf_dict3[q_num_id3[q_num]][w_id]=float(round((q_forward_index3[q_num][w_id])*(np.log((q_count)/q_df_dict3[w_id])),2))
                       
    
        

    


# In[238]:


#---------------reading, processing and calculating the query tf_idf-----------------------
Q_DIR = './Query-Documents/'

q_forward_index ={}
q_forward_index2 ={}
q_forward_index3 ={}

q_inverted_index={}
q_inverted_index2={}
q_inverted_index3={}

q_num_id={}
q_num_id2={}
q_num_id3={}

q_df_dict={}
q_df_dict2={}
q_df_dict3={}

q_tf_idf_dict={}
q_tf_idf_dict2={}
q_tf_idf_dict3={}

for file_name in os.listdir(Q_DIR):
    q_Indexer(Q_DIR + file_name)
    
with open('q_forward_index.txt', 'w') as f:    
    for key, value in q_forward_index.items():
        print(q_num_id[key],'\t',str(value)[1:-1] ,'\n',   file=f) 
        
with open('q_forward_index2.txt', 'w') as f:    
    for key, value in q_forward_index2.items():
        print(q_num_id2[key],'\t',str(value)[1:-1] ,'\n',   file=f) 
        
with open('q_forward_index3.txt', 'w') as f:    
    for key, value in q_forward_index3.items():
        print(q_num_id3[key],'\t',str(value)[1:-1] ,'\n',   file=f) 
        
        
        
with open('q_inverted_index.txt', 'w') as f:    
    for key, value in q_inverted_index.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)

with open('q_inverted_index2.txt', 'w') as f:    
    for key, value in q_inverted_index2.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)
        
with open('q_inverted_index3.txt', 'w') as f:    
    for key, value in q_inverted_index3.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)
 

with open('q_tf_idf_index.txt', 'w') as f:  
    for key, value in q_tf_idf_dict.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)
        
with open('q_tf_idf_index2.txt', 'w') as f:  
    for key, value in q_tf_idf_dict2.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)
        
with open('q_tf_idf_index3.txt', 'w') as f:  
    for key, value in q_tf_idf_dict3.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)


# In[21]:


#-----------------------------------making forward and inverted index of documents----------------------------

DOC_DIR = './IR-Documents/'

forward_index ={}
inverted_index={}

df_dict={}
tf_idf_dict={}
for file_name in os.listdir(DOC_DIR):
    Indexer(DOC_DIR + file_name)
    
with open('forward_index.txt', 'w') as f:    
    for key, value in forward_index.items():
        print(word_list[key],'\t',str(value)[1:-1] ,'\n',   file=f) 
        
with open('inverted_index.txt', 'w') as f:    
    for key, value in inverted_index.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)
 

with open('tf_idf_index.txt', 'w') as f:  
    for key, value in tf_idf_dict.items():
        print(key,'\t',str(value)[1:-1] ,'\n',   file=f)
       


# In[105]:


#---------------------making the vector for all of the words of all of the documents---------------------------
#N is number of total number of documents
#N=len(forward_index)
N=376
# total_vocab_size is lenght inverted_index

#total_vocab_size=len(inverted_index)

total_vocab_size=33183


D = np.zeros((N, total_vocab_size))
D = D.astype(object)

for doc_id in tf_idf_dict:
    
    for key,value in tf_idf_dict[doc_id].items():
        #print(key)
        D[int(doc_id)][int(key)] = float(value)
        
        


# In[271]:


def gen_vector(query_dict):
   # print(query_dict)

    Q = np.zeros(total_vocab_size)
    Q=Q.astype(object)
    
    words_count = len(q_tf_idf_dict)
    
    for key,value in query_dict.items():
        #print(key)
        Q[int(key)] = float(value)
    return Q

def gen_vector2(query_dict2):
   # print(query_dict2)

    Q1 = np.zeros(total_vocab_size)
    Q1=Q1.astype(object)
    
    words_count = len(q_tf_idf_dict2)
    
    for key,value in query_dict2.items():
        #print(key)
        Q1[int(key)] = float(value)
    return Q1

def gen_vector3(query_dict3):

    Q2 = np.zeros(total_vocab_size)
    Q2=Q2.astype(object)
    
    words_count = len(q_tf_idf_dict3)
    
    for key,value in query_dict3.items():
        #print(key)
        Q2[int(key)] = float(value)
        
    return Q2


# In[405]:




#------------------------------------------------
def cosine_sim(a, b):
    chek=(np.linalg.norm(a)*np.linalg.norm(b))
    if chek!=0.0:
        cos_sim =round( np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b)),5)
    else:
        cos_sim=0
        
    return cos_sim

#----------------------------------by default calculates the title cosin similarity----------------------
def cosine_similarity(n):
    d_cosines = []
    d_cosin_dict={}
    for key, value in q_tf_idf_dict.items(): 
        cosin_sorted[key]={}
        #print(value)
        query_vector = gen_vector(value)   
        i=1
        for d_id in D:
            cosin_=cosine_sim(query_vector, d_id)
            d_cosines.append(cosin_)
            if cosin_!=0.0:
                cosin_sorted[key][i]=cosin_
            i+=1
        out = np.array(d_cosines).argsort()[-n:][::-1]
        
        return(out)
    
def cosine_similarity2(n):
    d_cosines2 = []
    d_cosin_dict2={}
    for key, value in q_tf_idf_dict2.items():
        cosin_sorted2[key]={}
        #print(value)
        query_vector2 = gen_vector2(value)   
        i=1
        for d_id in D:
            cosin2_=cosine_sim(query_vector2, d_id)
            d_cosines2.append(cosin2_)
            if cosin2_!=0.0 :
                cosin_sorted2[key][i]=cosin2_
            i+=1
        out2 = np.array(d_cosines2).argsort()[-n:][::-1]

        return(out2)

    
def cosine_similarity3(n):
    d_cosines3 = []
    d_cosin_dict3={}
    for key, value in q_tf_idf_dict3.items(): 
        cosin_sorted3[key]={}
        #print(value)
        query_vector3 = gen_vector3(value)   
        i=1
        for d_id in D:
            cosin3_=cosine_sim(query_vector3, d_id)
            d_cosines3.append(cosin3_)
            if cosin3_!=0.0:
                cosin_sorted3[key][i]=cosin3_
            i+=1
        out3 = np.array(d_cosines3).argsort()[-n:][::-1]

        return(out3)


# In[406]:


#--------------------cosin similarity running---------------------------------

cosin_sorted={}
cosin_sorted2={}
cosin_sorted3={}

Q = cosine_similarity(5) 
#print(Q)
Q2 = cosine_similarity2(5) 
Q3 = cosine_similarity3(5) 


# In[409]:



#cosin_sorted={k: v for k, v in sorted(cosin_sorted.items(), key=lambda item: item[1],reverse=True)}
#print((cosin_sorted))

q_num_dict={1:352, 2:353, 3:354, 4:359}
#x = itertools.islice(cosin_sorted.items, 0, 5)

with open('title_output.txt', 'w') as f:  
    for q_n, value in cosin_sorted.items():
       
        value={k: v for k, v in sorted(value.items(), key=lambda item: item[1],reverse=True)}
        for key, val in value.items():
            print(q_num_dict[q_n],'\t',"FTP911-"+str(key),'\t',str(val) ,'\n',   file=f)
             #print(q_num_id2[key],'\t',str(value)[1:-1] ,'\n',   file=f) 
            
          #  print(q_num_dict[q_n],'\t',"FTP911-"+str(key),'\t',"0"+str(value) ,'\n',   file=f)

 #--------------------------------------------------------------       
#x = itertools.islice(cosin_sorted.items, 0, 5)

with open('title&description _output.txt', 'w') as f:  
    for q_n, value in cosin_sorted2.items():
        value={k: v for k, v in sorted(value.items(), key=lambda item: item[1],reverse=True)}
        for key, val in value.items():
            print(q_num_dict[q_n],'\t',"FTP911-"+str(key),'\t',str(val) ,'\n',   file=f)
             #print(q_num_id2[key],'\t',str(value)[1:-1] ,'\n',   file=f) 

          #  print(q_num_dict[q_n],'\t',"FTP911-"+str(key),'\t',"0"+str(value) ,'\n',   file=f)
        
        
        
with open('title&narrative _output.txt', 'w') as f:  
    for q_n, value in cosin_sorted3.items():
        value={k: v for k, v in sorted(value.items(), key=lambda item: item[1],reverse=True)}
        for key, val in value.items():
            print(q_num_dict[q_n],'\t',"FTP911-"+str(key),'\t',str(val) ,'\n',   file=f)
             #print(q_num_id2[key],'\t',str(value)[1:-1] ,'\n',   file=f) 

          #  print(q_num_dict[q_n],'\t',"FTP911-"+str(key),'\t',"0"+str(value) ,'\n',   file=f)


# In[ ]:




