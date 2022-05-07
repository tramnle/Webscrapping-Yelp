#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 11:16:18 2022

@author: tramle
"""

# Question 5 

from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import re
import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydb"]

mycol = mydb["sf_donut_shop"]

for i in np.arange(1,41,1):
    
    f= open("sf_donut_shop_" + str(i) + ".htm")
    print('\n\nRank:', i)
    content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all("div",{'class':'css-xp8w2v padding-t2__09f24__Y6duA padding-r2__09f24__ByXi4 padding-b2__09f24__F0z5y padding-l2__09f24__kf_t_ border--top__09f24__exYYb border--right__09f24__X7Tln border--bottom__09f24___mg5X border--left__09f24__DMOkM border-radius--regular__09f24__MLlCO background-color--white__09f24__ulvSM'})
    
    for div in divs:
        try:     
            pattern0 = re.compile(r'Get Directions')
            address = div.find("p",text=pattern0).nextSibling
            print("address:", address.text)
        except: 
            address = None
    
        try: 
            pattern = re.compile(r'Business website')
            website = div.find("p",text=pattern).nextSibling
            print("website:", website.text)
            pattern2 = re.compile(r'Phone number')
            phone = div.find("p",text=pattern2).nextSibling
            print("phone:",phone.text)
        except: 
            try:
                pattern2 = re.compile(r'Phone number')
                phone = div.find("p",text=pattern2).nextSibling
                print("phone:",phone.text)
            except: continue
                

    
    
    
# Question 6
for i in np.arange(1,41,1):
    
    f= open("sf_donut_shop_" + str(i) + ".htm")
    content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all("div",{'class':'css-xp8w2v padding-t2__09f24__Y6duA padding-r2__09f24__ByXi4 padding-b2__09f24__F0z5y padding-l2__09f24__kf_t_ border--top__09f24__exYYb border--right__09f24__X7Tln border--bottom__09f24___mg5X border--left__09f24__DMOkM border-radius--regular__09f24__MLlCO background-color--white__09f24__ulvSM'})
    
    
    for div in divs:
        try:
             
            pattern0 = re.compile(r'Get Directions')
            address = div.find("p",text=pattern0).nextSibling.text
            mydb.sf_donut_shop.find_one_and_update({'rank':int(i)}, {"$set":{'address':address}})
        except: address = None
            
        try:
            pattern = re.compile(r'Business website')
            website = div.find("p",text=pattern).nextSibling.text
            mydb.sf_donut_shop.find_one_and_update({'rank':int(i)}, {"$set":{'website':website}})
            pattern2 = re.compile(r'Phone number')
            phone = div.find("p",text=pattern2).nextSibling.text
            mydb.sf_donut_shop.find_one_and_update({'rank':int(i)}, {"$set":{'phone':phone}})
        except: 
            try:
                pattern2 = re.compile(r'Phone number')
                phone = div.find("p",text=pattern2).nextSibling.text
                mydb.sf_donut_shop.find_one_and_update({'rank':int(i)}, {"$set":{'phone':phone}})
            except: continue
            
        try: 
            
            url = 'http://api.positionstack.com/v1/forward?access_key=57f036dcaa50c3c11af21ad179203722&query=' + str(address)
            
            res = requests.get(url)
            doc = BeautifulSoup(res.content, 'html.parser')
            json_object = json.loads(str(doc)) 
        except: continue
    
        longitude = json_object['data'][0]['longitude']
        mydb.sf_donut_shop.find_one_and_update({'rank':int(i)}, {"$set":{'longitiude':longitude}})
        latitude = json_object['data'][0]['latitude']
        mydb.sf_donut_shop.find_one_and_update({'rank':int(i)}, {"$set":{'latitude':latitude}})
    
    
    ## Create index 
mydb.sf_donut_shop.create_index('rank')
if "rank_1" in mydb.sf_donut_shop.index_information():
        print("Rank is now index")
    
            
            
            
            
            
            
            


        

        
