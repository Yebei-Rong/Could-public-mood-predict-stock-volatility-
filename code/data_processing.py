#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pymysql
from datetime import datetime
from snownlp import SnowNLP


# In[2]:


# DB Connection


# In[3]:


conn = pymysql.connect(host='localhost', port=3306, user='root', password='password', db='stock')
cursor = conn.cursor()


# In[4]:


# Get raw data


# In[5]:


query_sql = "select stock_id, review, review_date from guba;"
cursor.execute(query_sql)
results = cursor.fetchall()
data = pd.DataFrame(data=list(results), index=None, columns=['stock_id', 'review', 'review_date'])


# In[46]:


data.shape[0]


# In[7]:





# In[8]:





# In[9]:


data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d', errors='coerce')


# In[10]:


data.index


# In[14]:


data.is_copy = False


# In[15]:


data = data.drop(data['review'] == '')


# In[17]:


data.index


# In[18]:


judge_df = pd.notnull(data)


# In[21]:


cnt = 0


# In[22]:


# Get sentiments
for i in range(2, 3019357):
    review = data.loc[i, 'review']
    if review != '' and judge_df.loc[i,'review']:
        nlp = SnowNLP(review)
        data.loc[i,'sentiment'] = nlp.sentiments
        cnt += 1
        
        if cnt % 10000 == 0:
            print(cnt)


# In[24]:


grouped = data[['sentiment', 'date']].groupby(data['date'])
mean = grouped.mean()


# In[25]:


mean


# In[47]:


data.head()


# In[ ]:


data = data


# In[66]:


## Preprocessing
# Convert review_date (str -> Date)
def get_year(s):
    '''
    >>> get_year('06-03')
    >>> '2018-06-03'
    '''
    
    month, day = s.split('-')
    
    if int(month) > 3:
        return '2018-' + s
    elif int(month) == 1:
        return '2019-' + s
    else:
        return ''
    
def parse_ymd(s):
    if s != '':
        year_s, mon_s, day_s = s.split('-')
        return datetime(int(year_s), int(mon_s), int(day_s))
    else:
        return ''


# In[50]:


data['date1'] = data['review_date'].apply(lambda x: parse_ymd(get_year(x)))


# In[52]:


grouped1 = data[['sentiment', 'date1']].groupby(data['date1'])
mean1 = grouped1.mean()


# In[55]:


mean1.to_excel('sentiment1.xlsx', encoding='utf-8')


# In[60]:


data.shape[0]


# In[67]:


data['date2'] = data['review_date'].apply(lambda x: parse_ymd(get_year(x)))


# In[68]:


grouped2 = data[['sentiment', 'date2']].groupby(data['date2'])
mean2 = grouped2.mean()


# In[70]:


mean2.to_excel('sentiment2.xlsx', encoding='utf-8')


# In[71]:


cursor.close()
conn.close()


# In[ ]:




