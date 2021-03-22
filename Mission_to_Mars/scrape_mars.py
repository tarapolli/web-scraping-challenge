# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import mars_data


def scrape():
    # initiallize browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    

time.sleep(1)

    # Visit Mars News site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    




    

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

