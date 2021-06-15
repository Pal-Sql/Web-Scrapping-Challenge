from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
def scrape():
    browser = init_browser()
    mars_data = {}
    #NASA MARS NEWS
    # ------------------------------------------
    url = "https://redplanetscience.com/"
    #Use requests module to retrieve the webpage
    response = requests.get(url)
    #Create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    #Retrieve article title and preview paragraph
    news_title = soup.find('div', class_="content_title").find('a').text
    news_p = soup.find('div', class_="rollover_description_inner").text
    #Add items into the mars_data dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p
    #JPL MARS SPACE IMAGES - FEATURED IMAGE
    # ------------------------------------------
    #Open webpage using splinter
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    #HTML object
    html = browser.html
    #Parse HTML object with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    #Extract base url from website url
    base_url = (url.split('/spaceimages'))[0]
    #Retrieve route to detailed image description webpage
    description_page = soup.find_all('a', class_='button fancybox')[0]['data-link']
    #Concatenate route and base url
    description_url = base_url + description_page
    #Open new url using splinter
    browser.visit(description_url)
    #Create HTML object
    image = browser.html
    #Parse HTML object with BeautifulSoup
    soup = BeautifulSoup(image, 'html.parser')
    #Retrieve route to full-size image 
    img = soup.find('img', class_="main_image")['src']
    #Concatenate route with base url
    featured_image_url = base_url + img
    #Add item to mars_data dictionary
    mars_data['featured_image_url'] = featured_image_url
    # MARS HEMISPHERES
    # ------------------------------------------
    url = "https://marshemispheres.com/"
    #Open webpage using splinter
    browser.visit(url)
    #HTML object
    html = browser.html
    #Parse HTML object with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    #Create list for image urls
    hemisphere_image_urls = []
    #Extract base url from webpage url
    base_url= (url.split('/search'))[0]
    #Retrieve all items with hemisphere info
    hemispheres = soup.find_all('div', class_='description')
    for hemisphere in hemispheres:
        #Create an empty dictionary
        hemisphere_info = {}
        #Retrieve hemisphere title
        hem_title = hemisphere.find('h3').text
        #Add only hemisphere title into dictionary by splitting text 
        hemisphere_info['title'] = hem_title.split(' Enhanced')[0]
        #Retrieve route to detailed hemisphere webpage
        hem_route = hemisphere.find('a', class_='itemLink product-item')['href']
        #Concatenate base url with route
        hemisphere_link = base_url + hem_route
        #Open new url with splinter
        browser.visit(hemisphere_link)
        #HTML object
        html = browser.html
        #Parse HTML object with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        #Retrieve route to full resolution image
        image_url = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        #Add image url into dictionary
        hemisphere_info['img_url'] = image_url
        #Append dictionary to list
        hemisphere_image_urls.append(hemisphere_info)
        #Add item into the mars_data dictionary
        mars_data["image_urls"] = hemisphere_image_urls
    #MARS FACTS
    # ------------------------------------------
    url = "https://galaxyfacts-mars.com/"
    #Scrape table data from Mars webpage
    tables = pd.read_html(url)
    #Index the first dataframe object
    df = tables[0]
    #Set column names
    df.columns = ['Description','Value']
    #Set Description column as the index
    df.set_index('Description', inplace=True)
    #Convert table into HTML table
    html_table = df.to_html()
    #Remove unwanted new lines
    html_table.replace('\n', '')
    #Add item to mars_data dictionary
    mars_data['html_table'] = html_table
    browser.quit()
    return mars_data