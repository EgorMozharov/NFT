#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
import yfinance as yf
import time
import matplotlib.pyplot as plt
from datetime import datetime


# In[3]:


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

# In[2]:


solana_df = yf.download("SOL-USD", start="2021-01-01", end=datetime.today().strftime('%Y-%m-%d'))
solana_df


# In[3]:


solana_df.plot(y = "Adj Close", use_index=True)


# ## Ethereum 

# In[4]:


Ethereum_df = yf.download("ETH-USD", start="2018-01-01", end=datetime.today().strftime('%Y-%m-%d'))
Ethereum_df


# In[5]:


Ethereum_df.plot(y = "Adj Close", use_index=True)


# ## Rarible

# In[59]:


dict_collections = {}
url_top_100 = 'https://api-mainnet.rarible.com/marketplace/api/v4/collections/top?days=30&size=100'
url_collections = 'https://rarible-cdn.reallm.io/collections/{}/prices?filters=%7B%7D'


def get_collections_id(url):
    json = requests.get(
        url
    ).json()

    df_id = pd.DataFrame.from_dict(json)
    df_id = df_id[['id', 'name']]
    return df_id


def get_collections_data(id):
    df = pd.read_json(url_collections.format(id))
    return df


df_id = get_collections_id(url_top_100)

for index, row in df_id.iterrows():
    dict_collections[row['name']] = get_collections_data(row['id'])

    
print(dict_collections)


# In[ ]:




