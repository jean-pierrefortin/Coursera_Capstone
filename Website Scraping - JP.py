#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import ssl
import csv
from urllib.request import urlopen #Download all neccessary libraries


# In[8]:


URL = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
page = requests.get(URL).text
soup = BeautifulSoup(page, 'lxml') #naming data crucial for scraping the data on website


# In[9]:


ctx = ssl.create_default_context() 
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE #SSL errors


# In[10]:


data_table = soup.find('table',{'class':'wikitable sortable'})
data_rows = data_table.find_all('tr') # find all table rows on website link


# In[11]:


table = [] 
for row in data_rows:
    table.append([t.text.strip() for t in row.find_all('td')]) #append to table all rows that are scraped from link


# In[27]:


df = pd.DataFrame(table, columns=['PostalCode', 'Borough', 'Neighbourhood'])
df = df[df['PostalCode'].notnull()] #pull all values with not null in columns
df.head() #Display frist 5 rows of data table


# In[29]:


df.drop(df[df['Borough'] == 'Not assigned'].index, axis=0, inplace = True) #drop all True values for Not assigned in Borough


# In[30]:


df.shape #express shape of dataframe


# In[66]:


df2 = df.groupby('PostalCode').agg(lambda x: ','.join(x)) # group ALL with same PostCode name in same Column
df2 #Display data table


# In[67]:


df2.reset_index() #reset index to data table


# In[68]:


df2.loc[df2['Neighbourhood']=="Not assigned",'Neighbourhood']=df2.loc[df2['Neighbourhood']=="Not assigned",'Borough'] 
#locate "Not assigned in Neighborhood col & replace with Borough"
df2 # Display data table


# In[69]:


df2['Borough']= df2['Borough'].str.replace('nan|[{}\s]','').str.split(',').apply(set).str.join(',').str.strip(',').str.replace(",{2,}",",") 
#take out duplicates in "Borough" column


# In[70]:


df_main = df2.reset_index() #reset index after taking out duplicates and creating new dataframe name
df_main.head() #display first 5 rows of new table after reseting index


# In[71]:


df_main.shape #Display shape of dataframe


# In[ ]:





# In[ ]:




