from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
     # Setup splinter
     executable_path = {'executable_path': ChromeDriverManager().install()}
     browser = Browser('chrome', **executable_path, headless=False)
     return browser

mars_data= {}
def mars_news_scrape():
     browser = init_browser()
    #Visit Nasa News url  using splinter module

     Nasa_url = 'https://mars.nasa.gov/news/'

     browser.visit(Nasa_url)

     html = browser.html

     Nasa_soup = bs(html, 'html.parser')

     first_li = Nasa_soup.find('li', class_='slide')

    # --- save the news title under the <div> tag with a class of 'content_title' ---
     Nasa_news_title = first_li.find('div', class_='content_title').text
     print(Nasa_news_title)

    # Extract title text
     nasa_news_paragraph=Nasa_soup.find('div',class_='article_teaser_body').text
     print(nasa_news_paragraph)

     browser.quit()
     return mars_data
     
def img_scrape():
     browser = init_browser()
     #Visit Nasa's JPL Mars Space url  using splinter module
     jplNasa_url = 'https://spaceimages-mars.com/'

     browser.visit(jplNasa_url)

     browser.links.find_by_partial_text('FULL IMAGE').click()

     html = browser.html
     soup = bs(html, 'html.parser')


     featured_image_url = soup.find('img', class_='fancybox-image')['src']
     featured_image_url = jplNasa_url + featured_image_url
     print(featured_image_url)
    
     browser.quit()
     return mars_data

def mars_facts():
     # Visit the Mars Facts webpage
     mars_facts_url='https://space-facts.com/mars/'
     mars_fact_table=pd.read_html(mars_facts_url)

     #Create Dataframe to store table data
     df = mars_fact_table[0]
     df.columns = ['Description', 'Mars']
     mars_facts = df.to_html()
     mars_data['mars_facts'] = mars_facts
     return mars_data
     


def mars_hem():

     browser = init_browser()
     # Visit the Mars Facts webpage
    # Visit the USGS Astrogeology site
     USGS_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
     short_url="https://astrogeology.usgs.gov"

     browser.visit(USGS_url)
     html = browser.html
     soup = bs(html, 'html.parser')
     main_url = soup.find_all('div', class_='item')
     
     hemisphere_img_urls=[]      
     for x in main_url:
          title = x.find('h3').text
          url = x.find('a')['href']
          hem_img_url= short_url+url
          #print(hem_img_url)
          browser.visit(hem_img_url)
          html = browser.html
          soup = bs(html, 'html.parser')
          hemisphere_img_original= soup.find('div',class_='downloads')
          hemisphere_img_url=hemisphere_img_original.find('a')['href']
          
          print(hemisphere_img_url)
          img_data=dict({'title':title, 'img_url':hemisphere_img_url})
          hemisphere_img_urls.append(img_data)
     mars_data['hemisphere_img_urls']=hemisphere_img_urls

     browser.quit()
     return mars_data