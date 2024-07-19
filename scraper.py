from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import requests
import json
from apify_client import ApifyClient

def get_price_from_gordon(item):
    # Define the search URL
    url = f"https://gfsstore.com/?ps={item}"
    
    # Send a GET request to fetch the page content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        logging.error(f"Failed to fetch data: Status code {response.status_code}")
        return []

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the product elements on the page
    product_boxes = soup.find_all('div', class_='product-box')
    print(f"Found {len(product_boxes)} products")
    
    result = []
    for product_box in product_boxes:
        try:
            # Extract the title
            title = product_box.find('p').text.strip()
            
            # Extract the price
            price_element = product_box.find('div', class_='product-box-price-reader')
            price = price_element.text.strip().replace('Price: ', '') if price_element else 'No Price'
            
            result.append({'title': title, 'price': price, 'store': 'Gordon'})
        except AttributeError as e:
            logging.error(f"Error processing product: {e}")
    
    return result

def get_price_from_target(item):
    params = {
        'api_key': '502991854DC34FE5A7B6D376183863BC',
        'search_term': item,
        'category_id': '5xt1a',
        'type': 'search'
    }

    api_result = requests.get('https://api.redcircleapi.com/request', params)
    data = api_result.json()

    result = []
    if 'search_results' in data:
        product = data['search_results']
        product_info = product[0].get('product', {})
        offers = product[0].get('offers', {}).get('primary', {})
        
        title = product_info.get('title')
        price = offers.get('price')

        if title and price is not None:
            result.append({'title': title, 'price': price, 'store': 'Target'})
    
    return result

def get_price_from_aldi(item):
    # Define the search URL
    url = f"https://new.aldi.us/results?q={item}"
    
    # Send a GET request to fetch the page content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        logging.error(f"Failed to fetch data: Status code {response.status_code}")
        return []

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the product elements on the page
    product_boxes = soup.find_all('div', class_='product-teaser-item product-grid__item')
    print(f"Found {len(product_boxes)} products")
    
    result = []
    for product_box in product_boxes:
        try:
            # Extract the title
            title_element = product_box.find('div', class_='product-tile')
            title = title_element.get('title') if title_element else 'N/A'
            
            # Extract the price
            price_element = product_box.find('span', class_='base-price__regular')
            price = price_element.get_text(strip=True) if price_element else 'N/A'
            
            result.append({'title': title, 'price': price, 'store': 'Aldi'})
        except AttributeError as e:
            logging.error(f"Error processing product: {e}")
    
    return result

def collect_data(item):
    # Initialize an empty list to collect results from different sources
    all_results = []

    target_prices = get_price_from_target(item)
    gfs_prices = get_price_from_gordon(item)
    aldi_prices = get_price_from_aldi(item)
    all_results.extend(aldi_prices)
    all_results.extend(gfs_prices)
    all_results.extend(target_prices)
    
    return all_results