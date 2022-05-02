#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import yfinance as yf
import time
import matplotlib.pyplot as plt
from datetime import datetime


# In[2]:


import requests
import sys
import traceback
from getpass import getpass
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC


# # Get Data

# ## Solana

# In[3]:


solana_df = yf.download("SOL-USD", start="2021-01-01", end=datetime.today().strftime('%Y-%m-%d'))
solana_df


# In[4]:


solana_df.plot(y = "Adj Close", use_index=True)


# ## Ethereum 

# In[5]:


Ethereum_df = yf.download("ETH-USD", start="2018-01-01", end=datetime.today().strftime('%Y-%m-%d'))
Ethereum_df


# In[6]:


Ethereum_df.plot(y = "Adj Close", use_index=True)


# ## Rarible

# In[ ]:


dict_collections = {}
list_broken_urls = []
url_top_100 = 'https://api-mainnet.rarible.com/marketplace/api/v4/collections/top?days=30&size=100'
url_collections = 'https://rarible-cdn.reallm.io/collections/{}/{}?filters=%7B%7D'
broken_collection_url = 'https://rarible.com/collection/{}/stats?range=-Number.MAX_SAFE_INTEGER'
list_features = ['prices', 'marketcap', 'lowwatermark', 'transactions', 'owners', 'sellers', 'buyers']

def get_collections_id(url):
    json = requests.get(
        url
    ).json()

    df_id = pd.DataFrame.from_dict(json)
    df_id = df_id[['id', 'name']]
    return df_id


def change_collection_data(df, feature):
    if feature == 'prices':
        df.rename(columns = {'dates': 'date'}, inplace = True)
    elif feature == 'marketcap':
        df.rename(columns = {'graph_dates': 'date'}, inplace = True)
        df.rename(columns = {'graph_values': 'marketcap'}, inplace = True)
        df = df[['date', 'marketcap']]
    elif feature == 'lowwatermark':
        df.rename(columns = {'graph_dates': 'date'}, inplace = True)
        df.rename(columns = {'graph_values': 'lowwatermark'}, inplace = True)
        df = df[['date', 'lowwatermark']]
    elif feature == 'transactions':
        df.rename(columns = {'graph_dates': 'date'}, inplace = True)
        df.rename(columns = {'graph_values': 'amount_transactions'}, inplace = True)
        df = df[['date', 'amount_transactions']]
    elif feature == 'owners':
        df.rename(columns = {'graph_dates': 'date'}, inplace = True)
        df.rename(columns = {'graph_values': 'amount_owners'}, inplace = True)
        df = df[['date', 'amount_owners']]
    elif feature == 'sellers':
        df.rename(columns = {'graph_dates': 'date'}, inplace = True)
        df.rename(columns = {'graph_values': 'amount_sellers'}, inplace = True)
        df = df[['date', 'amount_sellers']]
    elif feature == 'buyers':
        df.rename(columns = {'graph_dates': 'date'}, inplace = True)
        df.rename(columns = {'graph_values': 'amount_buyers'}, inplace = True)
        df = df[['date', 'amount_buyers']]
    
    return df


def get_collection_data(id, features):
    df = pd.DataFrame()
    flag = True
    for feature in features:
        tmp = pd.read_json(url_collections.format(id, feature))
        df = pd.merge(df, change_collection_data(tmp, feature), how='left')
    
    return df


df_id = get_collections_id(url_top_100)

for index, row in df_id.iterrows():
    try:
        dict_collections[row['name']] = get_collection_data(row['id'], list_features)
    except:
        print("collection:", row['name'], "has not got dataset")
        print("url:", broken_collection_url.format(row['id']))
        list_broken_urls.append(broken_collection_url.format(row['id']))
        pass


# In[9]:


dict_collections['Moonbirds']


# In[ ]:




