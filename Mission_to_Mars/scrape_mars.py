#!/usr/bin/env python
# coding: utf-8


# Dependencies for all four sections 
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import time

def init_browser():  # Setup splinter
    # @NOTE: Replace the path with your actual path to the chromedriver
    # eexecutable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)
  
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)

# Set up Splinter - AskBCS
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

# In[2]:
      # connect to url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)
    
      # In[4]:
      # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html             
    soup = BeautifulSoup(html, 'html.parser')

      # Search for the latest news title; assign to a variable.
    title_results = soup.find_all('div', class_='content_title')

      # Extract first title; assign new variable, then print
    news_title = title_results[1].text
    print(news_title)

      # Search for the latest news paragraph rollover text; assign to a variable.
    p_results = soup.find_all('div', class_='article_teaser_body')

      # Extract first paragraph; assign new variable, then print            
    news_p = p_results[0].text
    print(news_p)


      # Part II: JPL Mars Space Images

      # setup splinter
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)

      # connect to urls
    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html' 
    browser.visit(url2)

    base_url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'


      # click full image button, then inspect
    image_button = browser.find_by_css("button.btn.btn-outline-light")
    image_button.click()

      # Create HTML and BeautifulSoup objects; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

      # create relative image path
    featured_image = soup.select_one("div.fancybox-inner img").get("src")
    featured_image

      # save a complete url string for this image
    featured_image_url = base_url2 + featured_image
    print(featured_image_url)


      # Part III:  Mars Facts

      # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. (Day2#3)
    import pandas as pd

    url3 = "https://space-facts.com/mars/"


    tables = pd.read_html(url3)
    tables[0]

      # use first of 3 tables on website; this one contains Mars' facts
    facts_df = tables[0]

      # convert data to a HTML table string
    mars_facts = facts_df.to_html()
    mars_facts


      # Part IV:  Mars Hemispheres

      # dependency
    # from webdriver_manager.chrome import ChromeDriverManager
    # from splinter import Browser
    # from bs4 import BeautifulSoup as bs
    # from bs4 import BeautifulSoup

    #   # Setup splinter
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)


      # connect to url
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

      # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html             
    soup = BeautifulSoup(html, 'html.parser')


      # search for hemispheres; assign to a variable.
    items = soup.find_all('div', class_='item')

      # empty list to add urls
    hemisphere_image_urls = []
      
    base_url4 = 'https://astrogeology.usgs.gov'

      # Loop through the items previously stored
    for x in items: 
          # obtain hemispher title
        title = x.find('h3').text
          
          # variable for link to link with full resoltuion image
        hemi_url = x.find('a', class_='itemLink product-item')['href']
          
          # visit link to full resolutin image 
        browser.visit(base_url4 + hemi_url)
          
          # HTML Object of individual hemisphere information website 
        hemi_html = browser.html
          
          # Parse hemisphere HTML using Beautiful Soup 
        soup = BeautifulSoup(hemi_html, 'html.parser')
          
          # variable for high resolution image
        img_url = base_url4 + soup.find('img', class_='wide-image')['src']
          
          # Append hemisphere and and image to list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
          
      # print list of dictionaries 
    hemisphere_image_urls

      # %%
        ## Close the test browser
    # browser.quit()
        

      # Step 2 - MongoDB & FLASK APPLICATION

    mars_data = {"news_title": news_title, 
                  "news_p": news_p,
                  "featured_image_url": featured_image_url,
                  "mars_facts": mars_facts,
                  "hemisphere_image_urls": hemisphere_image_urls}

      ## Close the test browser
    browser.quit()

    return mars_data

  