#!/usr/bin/env python
# coding: utf-8

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # Setup splinter
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # ## NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Retrive all elements that contain information 
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
                             
    # ## JPL Mars Space Images - Featured Image
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Retrive all elements that contain information
    image = soup.find('div', class_='floating_text_area')
    image_url = image.find('a')['href']
    featured_image_url = jpl_url + image_url
    
    # ## Mars Facts

    # Use the read html function in Pandas to automatically scrape any tabular data from the page
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Data', 'Info']
    
    # Generate HTML table from DataFrame
    html_table = df.to_html()
    html_table

    # Strip unwanted newlines to clean up the table
    html_table.replace('\n', '')

    # ## Mars Hemisphere

    # Defining url and link
    astro_url = 'https://marshemispheres.com/'
    browser.visit(astro_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all hemispheres using beautifulsoup
    hemispheres = soup.find_all('div', class_='description')
    hemispheres

    # Creating empty hemisphere link list
    hemisphere_links = []

    # Loop throug hemispheres to append links to list
    for hemisphere in hemispheres:
        link = astro_url + hemisphere.find('a')['href']
        hemisphere_links.append(link)
    
    # Creating empty image url list
    hemisphere_info = []

    # Loop through links to obtain image URL and title
    for link in hemisphere_links:
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        title = soup.find('h2', class_='title').text
    
        image_div = soup.find('div', class_='downloads')
        image_info = image_div.find('ul').find_all('li')[0].find('a')
        image_url = astro_url + image_info['href']
        hemisphere_info.append({"title":title, "img_url":image_url})
    
    # Store in a dictionary
    mars_data = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "html_table":html_table,
        "hemisphere_info":hemisphere_info
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data



