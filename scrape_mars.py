# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser(): 
# Use splinter to start up a Chrome driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # Call the init_browser function to start the browser
    browser = init_browser()

    # Send the browser to NASA's news page
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # Give the browser 1 second to load the website
    time.sleep(1)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Pull the list of articles
    article_list = soup.find('ul', class_='item_list')

    # Extract the most recent article's title
    news_title = article_list.h3.text

    # Extract the most recent article's description
    news_p = article_list.find('div', class_="rollover_description_inner").text

    # Send the browser to the JPL Featured Space Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Click on FULL IMAGE for the featured image
    browser.click_link_by_partial_text('FULL IMAGE')

    # The browser tried to click too quickly, so add a one second delay
    time.sleep(2)

    # Click on more info to get to the high quality image
    browser.click_link_by_partial_text('more info')

    # create HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract URL from the anchor
    image_url_pre_formatted = soup.article.figure.a['href']
    # Create a full link
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url_pre_formatted

    # Send the browser to the Mars Weather Twitter account
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # create HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Collect all tweets on the timeline in an iterable list
    nearlytimeline = soup.find('div', class_='ProfileTimeline')
    timeline = nearlytimeline.find('ol', class_="stream-items js-navigable-stream")
    tweetsAll = timeline.find_all('li', class_='js-stream-item stream-item stream-item ')

    # Iterate through the list indefinitely until a tweet from Mars Weather twitter account appears
    # This eliminates the problem of retweets
    counter = 0
    name = ''

    while name != '@MarsWxReport':
        tweet = tweetsAll[counter]
        
        mars_weather = tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
        
        tweet_user = tweet.find('span', class_='username u-dir u-textTruncate').text
        
        name = tweet_user
        
        counter += 1

    # Use Pandas to scrape the URL for data formatted as a table
    url = 'http://space-facts.com/mars/'

    mars_data = pd.read_html(url)

    # mars_data returns a list so take the 0th element and create a data frame
    mars_df = mars_data[0]

    mars_df.columns = ['description', 'value']

    mars_df.set_index('description', inplace = True)

    # Convert the data frame to an HTML string
    df_html = mars_df.to_html()

    # Initialize an empty list that will be filled with dictionaries
    # Initialize a list of the hemispheres so we can loop through and do everything in one cell
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
    hemisphere_image_urls = []

    # Send the browser to the USGS Astrogeology site to get high res images of the hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    for hemi in hemispheres:        
        # Do the same as above for Schiaparelli Hemisphere
        browser.click_link_by_partial_text(f'{hemi} Hemisphere Enhanced')

        # create HTML object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Initialize the dict
        hemi_dict = {}

        # Scrape the incomplete URL
        inc_url = soup.find('img', class_='wide-image')['src']

        # Construct the complete URL
        img_url = 'https://astrogeology.usgs.gov' + inc_url

        # Store the data in a dictionary then add that dictionary to the tracking list
        hemi_dict["title"] = f'{hemi} Hemisphere'
        hemi_dict["img_url"] = img_url
        hemisphere_image_urls.append(hemi_dict)

        # Return to the original page
        browser.click_link_by_partial_text('Back')

    mars_facts_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts_table': df_html,
        'hemisphere_imgs': hemisphere_image_urls
    }


    # Return the dictionary
    return mars_facts_dict