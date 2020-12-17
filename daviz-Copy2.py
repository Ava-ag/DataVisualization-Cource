#!/usr/bin/env python
# coding: utf-8

# 
# Title: The Effect of my weekly steps number on my walking pace
# 
# I am interested in analyze how the steps/time that I walk per week improves my walking pace and aerobic fitness over time.
# 
# Data Collection:
# 
# I collected all the data from my fitbit watch except:
# 
# 1- '1 mile test time' because my watch GPS was not as acurate as my cellphone so i record that with my phone via an app named 
# Strava.
# 
# 2- 'Dificulty level' which I insert in manually after each weekly test in my phone.
# I defined 'Dificulty level' a scale  between 1 to 10 from very easy to very hard while doing 1 Mile test.
# 
# *- During the 1 Mile test I walked as fast as I can.
# 
# I export 2 csv files from my account from fitbit website: one for sleep data and another for activity data like steps,calorie burned,distance,etc.
# 
# I joined 2 csv files on Date column. 
# 
# note: my sleep data was not completly recorded because during some nights i had'nt wear my watch! so I decided to fill all Na numbers in sleep data with 400 minutes sleep(a little bit less than 7 hours)!
# 
# *- during the analysis I considered 7  and more hours of night sleep 'enough sleep'.
# 

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


#read the first file,Activity data

data = pd.read_csv('GFG.csv')


# In[4]:


data.head()


# In[5]:


#cleaning the data
data.set_index('Date',inplace=True)


# In[6]:


data=data.drop('Unnamed: 0',axis=1)


# In[7]:


data.head()


# In[8]:


sns.distplot(data['Steps'],color='green')
plt.title('Daily Steps "dist" plot',fontsize=20)
data['Steps'].describe()


# In[9]:


data['Steps'].plot(figsize=(25,7),color='green',kind='bar')
plt.title('Steps/calories burned per day',fontsize=25)
plt.yticks(fontsize=16)
plt.xlabel('Date',fontsize=20)
plt.xticks(fontsize=13)
plt.plot(data['Calories Burned'],color='red',label='calorie burned',linewidth=4.0)
plt.legend(fontsize=15)


# In[14]:


sns.relplot(x='Steps',y='1 MILE TEST',data=data,hue='TIME',style='DIFFICULTY',height=5, aspect=1.6)


# In[15]:


data['day_num'] = np.arange(len(data))


# In[17]:


avg=[]
for i in range(0,len(data),7):
    avg.append(sum(data['Steps'].values[i:i+7]))


# In[ ]:





# In[18]:


#reading second file,sleep data
sleep = pd.read_csv('sleep.csv',parse_dates=True)
sleep.set_index('End Time',inplace=True)


# In[19]:


sleep.head()


# In[79]:


#sleep['Minutes Asleep'].plot(figsize=(25,6))


# In[23]:


#remove rows less than 5 hours sleep(during days sleeps)
sleep=sleep[sleep['Minutes Asleep'] > 300]


# In[25]:


sleep['Minutes Asleep'].plot(figsize=(25,6),linewidth=6)
sleep['Minutes REM Sleep'].plot(linewidth=6)
plt.legend(fontsize=20)


# In[80]:


#parse date from time stamp
sleep['Start Time'] =  pd.to_datetime(sleep['Start Time'])


# In[81]:


sleep['Date']=sleep['Start Time'].dt.date


# In[82]:


sleep['Date']


# In[29]:


#convert it to string
sleep['Date']=sleep['Date'].astype(str)


# In[ ]:





# In[30]:


sleep.head()


# In[32]:


data = pd.read_csv('GFG.csv')
data=data.drop('Unnamed: 0',axis=1)

dff=data.set_index('Date').join(sleep.set_index('Date'))


# In[721]:


dff


# In[33]:


#fill NAs with 400 min
dff['Minutes Asleep']=dff['Minutes Asleep'].fillna(400)


# In[83]:



#dff['Minutes Asleep'].plot(figsize=(25,6),linewidth=6)
#plt.legend(fontsize=20)


# In[57]:


dff.drop_duplicates(subset ='Steps', 
                     keep ='first', inplace = True) 


# In[58]:


table=dff[dff['1 MILE TEST'].notna()]


# In[84]:


table


# In[60]:


import numpy as np
table['Sleep enough'] = np.where(table['Minutes Asleep']>400,'True','False')
table['Sleep enough'] = np.where(table['Sleep enough']=='True','yes','no')


# In[61]:


d={'Weekly Steps':avg,'1 Mile Test':table['1 MILE TEST'],'difficulty':[7,6,7,7,8,8,8,7,7],'time':table['TIME'],'enough Sleep':table['Sleep enough'] }
df=pd.DataFrame(data=d)
df.reset_index(drop=True, inplace=True) 


# In[62]:


df


# In[85]:


sns.relplot(x='Weekly Steps',y='1 Mile Test',data=df,hue='time',size='difficulty',sizes=(40,300),style='enough Sleep',height=5, aspect=1.6)
plt.xlabel('Weekly Steps',fontsize=16)
plt.ylabel('1 Mile Test time',fontsize=16)
sns.regplot(x='Weekly Steps',y='1 Mile Test',data=df,color='orange')


# In[ ]:


#it shows a negative correlation between number of steps taken each week and the 1 tile test time


# In[64]:


sns.relplot(x=list(df.index),y='1 Mile Test',data=df,hue='time',size='difficulty',sizes=(40,300),style='enough Sleep',height=5, aspect=1.6)
plt.xlabel('Week Number',fontsize=16)
plt.ylabel('1 Mile Test Time',fontsize=16)
plt.title('1 Mile Test Time over the weeks',fontsize=16)
sns.regplot(x=list(df.index),y='1 Mile Test',data=df,color='orange',ci=None)


# In[ ]:


#there is also a negative correlation between 1 mile test time and time


# In[78]:


sns.relplot(x='difficulty',y='1 Mile Test',data=df,size='difficulty',sizes=(40,300),hue='time',style='enough Sleep',height=5, aspect=1.6)
plt.xlabel('Difficulty level',fontsize=16)
plt.ylabel('1 Mile Test Time',fontsize=16)
plt.title('Difficulty level Categories',fontsize=16)


# In[ ]:


#is hsowes its more likely if do not have enough sleep,doing the test would be more difficult for me

