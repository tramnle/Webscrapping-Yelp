#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 11:10:55 2022

@author: tramle
"""
from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import re
import pymongo
import json

# Question 3 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydb"]

mycol = mydb["sf_donut_shop"]
a = 1
for i in np.arange(1,5,1):
    f = open("sf_donut_shop_search_page" + str(i) + ".htm")
    print('\n Search page inserted to database:', i)
    content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all("div",{'class':'container__09f24__mpR8_ hoverable__09f24__wQ_on margin-t3__09f24__riq4X margin-b3__09f24__l9v5d padding-t3__09f24__TMrIW padding-r3__09f24__eaF7p padding-b3__09f24__S8R2d padding-l3__09f24__IOjKY border--top__09f24__exYYb border--right__09f24__X7Tln border--bottom__09f24___mg5X border--left__09f24__DMOkM border-color--default__09f24__NPAKY'})

    for n in np.arange(2,12,1):
        name = divs[n].h3.span.a.get('name')
        rank = a
        link = str('https://www.yelp.com/') + divs[n].h3.span.a.get('href')
        rating = divs[n].find("span",{'class':'display--inline__09f24__c6N_k border-color--default__09f24__NPAKY'}).div.get('aria-label')
        review = divs[n].find("span",{'class':'reviewCount__09f24__tnBk4 css-1e4fdj9'}).text
        tags = divs[n].find("span",{'class':'css-epvm6 display--inline__09f24__c6N_k border-color--default__09f24__NPAKY'})
        a = a+1
        try:
            order = divs[n].find("span",{'class':'css-1enow5j'}).text
            order_on = "Yes"
            
        except: 
            order_on = None
        try:
            dollar = divs[n].find('span',{'class':'priceRange__09f24__mmOuH css-18qxe2r'}).text
        except: 
            dollar = None
            mydict = {"name":name, "rating": rating,"link": link, "tag":[], "rank":rank, "review": review,"dollar sign": dollar, "delitags":[],"Online order":order_on}
        
        mydict = {"name":name, "rating": rating,"link": link, "tag":[], "rank":rank, "review": review,"dollar sign": dollar,"delitags":[],"Online order":order_on}

        for  tag in tags:
            tag_name = tag.text
            mydict['tag'].append(tag_name)
        
        try:
            delitags = divs[n].find("div",{'data-testid':'TRUSTED_PROPERTY'})
            for delitag in delitags:
                tags_true = delitag.find('span',{'class':'raw__09f24__T4Ezm'}).text
                option = delitag.find('svg',{'class':'icon_svg'}).parent.get('class')            
                if "checkmark" in str(option):
                        deliver_order_option = str(tags_true) + str(": Yes")
                else: 
                        deliver_order_option = str(tags_true) + str(": No")
                
                mydict['delitags'].append(deliver_order_option)
        except:
            deliver_order_option = None
            mydict['delitags'].append(deliver_order_option)
            
        
        mydb.sf_donut_shop.insert_one(mydict)
        
        
        
# Question 4 


docs = list(mycol.find({},{"_id": 0,"link":1}))

i = 1 
for doc in docs:
    url = doc['link']
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    time.sleep(5)
    file= open("sf_donut_shop_" + str(i) + ".htm","w")
    file.write(str(soup))
    file.close()
    i = i + 1