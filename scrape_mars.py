#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    # URLs
    nasa_url = '''https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%
    2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'''
    jpl_url = '''https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'''
    marsweather_url = '''https://twitter.com/marswxreport?lang=en'''
    marsfacts_url = '''https://space-facts.com/mars/'''
    hemispheres_url = '''https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'''

    ## NASA WebPage ## ------------------------------------------------------------------------------------
    # Retrieve page with splinter
    url = nasa_url
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the parent li's for all articles
    results = soup.find_all('li', class_='slide')

    #Write News Title and Paragraph
    news_title = results[0].find('h3').text
    news_p = results[0].find('div', class_='article_teaser_body').text

    ## Featured Image from JPL ## ------------------------------------------------------------------------------------
    #Retrieve page with splinter
    url = jpl_url
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Retrieve parent 
    results = soup.find('a', class_='button fancybox')

    #Write Featured Image URL
    featured_image_url = f"https://www.jpl.nasa.gov{results['data-fancybox-href']}"


    ## Mars Weather ------------------------------------------------------------------------------------------------
    #Retrieve page with splinter
    url = marsweather_url
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = list(results.children)[0]

    ## Mars Facts ------------------------------------------------------------------------------------------------
    #Retrieve page with splinter
    url = marsfacts_url
    df = pd.read_html(url)

    marsfacts = df[0].rename(columns = {0:'Description',1:'Values'})

    facts_html = marsfacts.to_html()
    facts_html = facts_html.replace('\n','')

    ## Mars Hemispheres ------------------------------------------------------------------------------------------------
    url = hemispheres_url
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Find all image titles and store in list
    results = soup.find_all('div', class_='description')
    title_list = []
    for result in results:
        title_list.append(result.find('h3').text)

    #Find all image URLs
    list_img_url = []
    xpath = '//div[@class="description"]/a/h3'
    clickables = browser.find_by_xpath(xpath)

    for i in range(len(clickables)):
        clickables[i].click()

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        list_img_url.append(list(list(list(soup.find('div',class_='downloads').children)[5].children)[1].children)[0]['href'])

        browser.back()

        clickables = browser.find_by_xpath(xpath)

    #Save list of URLs
    hemisphere_image_urls = []
    for i in range(len(title_list)):
        hemisphere_image_urls.append({"title":title_list[i],"img_url":list_img_url[i]})

    browser.close()

    ## Insert Items into Mongo ---------------------------------------------------------------------------------------------
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.mars_db
    collection = db.marsinfo

    # Dictionary to be inserted into MongoDB
    post = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts':facts_html,
        'hemispheres': hemisphere_image_urls
    }

    # Insert dictionary into MongoDB as a document
    collection.insert_one(post)
    browser.quit()
    return post