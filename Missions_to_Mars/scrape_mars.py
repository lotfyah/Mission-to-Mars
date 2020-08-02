#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup as bs
from selenium import webdriver
from splinter import Browser
import pandas as pd
import requests
import pymongo
import time
import os


client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

# NASA Mars News

# In[ ]:

def init_browser():
    executable_path = {"executable_path":'chromedriver.exe'}


    return Browser('chrome', **executable_path, headless=False)

# In[ ]:
def scrape():

    browser = init_browser()
    mars_facts_data = {}

    nasa = 'https://mars.nasa.gov/news/'
    browser.visit(nasa)
    time.sleep(5)

# In[ ]:
    browser = init_browser()
    html = browser.html
    soup = bs(html, 'html.parser')

# In[ ]:
    
    news_title = soup.find('div', class_='content_title').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = news_paragraph

# JPL Mars Space Images - Featured Image

# In[ ]:
# featured category url
    nasa_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit'
    browser.visit(nasa_image)
    time.sleep(5)

# In[ ]:

    html_image = browser.html
    soup = bs(html_image, "html.parser")
    image_url = soup.find("img", class_="thumb")["src"]
    featured_image_url = 'https://www.jpl.nasa.gov/' + image_url
    print(featured_image_url)

# Mars Weather

# In[ ]:

    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, 'html.parser')
    mars_weather = soup.find(
        'div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text
    mars_facts_data["mars_weather"] = mars_weather


# Mars Facts

# In[ ]:

    url_facts = 'https://space-facts.com/mars/'
    time.sleep(5)
    table = pd.read_html(url_facts)
    table[0]


# In[ ]:

    df_mars_facts = table[0]
    df_mars_facts.columns = ['Parameter', 'Values']
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace('\n', '')
    mars_facts_data['mars_facts_table'] = mars_html_table

# Mars Hemispheres

# In[40]:

    url_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisphere)
    time.sleep(5)



# In[41]:

    html_hemispheres = browser.html

    soup = bs(html_hemispheres, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for i in items:

        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)

        partial_img_html = browser.html

        soup = bs(partial_img_html, 'html.parser')

        img_url = hemispheres_main_url + \
            soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({"title": title, "img_url": img_url})

        mars_facts_data['hemisphere_img_url'] = hemisphere_image_urls

        
        return mars_facts_data
    collection.insert(mars_facts_data)
 

