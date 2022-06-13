#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import datetime as dt
import pandas as pd

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    image_dicts = mars_hemis(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "image_dicts": image_dicts
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Replacing 'dataframe' with 'table table-striped' is a Bootstrap 3 table class which looks nicer
    return df.to_html().replace('dataframe','table table-striped')

def mars_hemis(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    hemi_elem = hemi_soup.find_all('div', class_='item')

    for hemi in hemi_elem:
        hemi_data = {}
        
        # Find URL to hemisphere page
        hemi_url_rel = hemi.find('a').get('href')
        
        # Navigate to Hemisphere page, set up new Soup
        browser.visit(f"{url}{hemi_url_rel}")
        hemi_html = browser.html
        hemi_image_soup = soup(hemi_html, 'html.parser')
        
        # Isolate <div> tag for box with download information
        hemi_image_box = hemi_image_soup.find('div', class_='downloads')
        
        # Find URL to first link, which is the full "Sample" link and assign to dictionary
        hemi_image_url_rel = hemi_image_box.find('a', target='_blank').get('href')
        hemi_data['img_url'] = f"{url}{hemi_image_url_rel}"
        
        # Find title, assign to dictionary
        hemi_title = hemi_image_soup.find('h2', class_='title').get_text()
        hemi_data['title'] = hemi_title
        
        # Append data to list of dictionaries and browser back
        hemisphere_image_urls.append(hemi_data)
        browser.back()
    
    return hemisphere_image_urls


