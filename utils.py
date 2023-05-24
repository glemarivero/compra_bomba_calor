import yaml
import streamlit as st
from bs4 import BeautifulSoup
import requests

def get_costo_hora(hora):
    config = get_config()['costo_horarios']
    if 0 <= hora < 7:
        return config['valle']
    elif 7 <= hora < 18 or 22 <= hora < 24:
        return config['llano']
    else:
        return config['punta']

@st.cache_data
def get_precio_fuel_oil():
    url = 'https://www.ancap.com.uy/1665/1/fueloil-medio.html'

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the desired field based on its HTML element and attributes
        # For example, let's extract the title of the webpage assuming it is enclosed in an <h1> tag
        prices = soup.find_all(id='envaseprecio', class_='price-box-price')
        for price in prices:
            if '0.0' in price.text:
                continue
            price_text = price.text
            print(f"Precio: {price_text}")
            break
        else:
            print("Title element not found.")
    else:
        print("Failed to retrieve the webpage.")
        return 0
    return float(price_text[1:])


@st.cache_data
def get_config():
    with open('config.yaml') as fid:
        config = yaml.safe_load(fid)
    return config

@st.cache_data
def get_usd_uyu_conversion():
    # URL of the API endpoint
    url = 'https://api.apilayer.com/exchangerates_data/convert?to=UYU&from=USD&amount=1'

    headers = {'apikey': 'FY7COUOWP57FLlkpfDEcMCBJxGWj4dkx'}
    # Send a GET request to the API
    response = requests.get(url,
                            headers=headers)
    conversion_rate = 1
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the conversion rate from the response JSON
        data = response.json()
        if 'result' in data:
            conversion_rate = data['result']
            print(f"USD to UYU Conversion Rate: {conversion_rate}")
        else:
            print("Conversion rate not found in the API response.")
    else:
        print("Failed to retrieve the conversion rate.")
    return conversion_rate
