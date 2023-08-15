#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
#     </a>
# </p>
# 
# <h1 align=center><font size = 5>Assignment: SQL Notebook for Peer Assignment</font></h1>
# 
# Estimated time needed: **60** minutes.
# 
# ## Introduction
# Using this Python notebook you will:
# 
# 1.  Understand the Spacex DataSet
# 2.  Load the dataset  into the corresponding table in a Db2 database
# 3.  Execute SQL queries to answer assignment questions 
# 

# ## Overview of the DataSet
# 
# SpaceX has gained worldwide attention for a series of historic milestones. 
# 
# It is the only private company ever to return a spacecraft from low-earth orbit, which it first accomplished in December 2010.
# SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars wheras other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. 
# 
# 
# Therefore if we can determine if the first stage will land, we can determine the cost of a launch. 
# 
# This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.
# 
# This dataset includes a record for each payload carried during a SpaceX mission into outer space.
# 

# ### Download the datasets
# 
# This assignment requires you to load the spacex dataset.
# 
# In many cases the dataset to be analyzed is available as a .CSV (comma separated values) file, perhaps on the internet. Click on the link below to download and save the dataset (.CSV file):
# 
#  <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv" target="_blank">Spacex DataSet</a>
# 
# 

# In[6]:


get_ipython().system('pip install --force-reinstall ibm_db==3.1.0 ibm_db_sa==0.3.3')

get_ipython().system('pip install sqlalchemy==1.3.24')

get_ipython().system('pip uninstall ipython-sql -y')

get_ipython().system('pip install ipython-sql==0.4.1')


# ### Connect to the database
# 
# Let us first load the SQL extension and establish a connection with the database
# 

# In[8]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[11]:


import csv, sqlite3

con = sqlite3.connect("my_data1.db")
cur = con.cursor()


# In[10]:


get_ipython().system('pip install -q pandas==1.1.5')


# In[12]:


get_ipython().run_line_magic('sql', 'sqlite:///my_data1.db')


# In[13]:


import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")


# **Note:This below code is added to remove blank rows from table**
# 

# In[14]:


get_ipython().run_line_magic('sql', 'create table SPACEXTABLE as select * from SPACEXTBL where Date is not null')


# ## Tasks
# 
# Now write and execute SQL queries to solve the assignment tasks.
# 
# **Note: If the column names are in mixed case enclose it in double quotes
#    For Example "Landing_Outcome"**
# 
# ### Task 1
# 
# 
# 
# 
# ##### Display the names of the unique launch sites  in the space mission
# 

# In[16]:


get_ipython().run_line_magic('sql', 'select DISTINCT ("Launch_Site") from SPACEXTABLE')


# 
# ### Task 2
# 
# 
# #####  Display 5 records where launch sites begin with the string 'CCA' 
# 

# In[24]:


get_ipython().run_line_magic('sql', 'Select * from SPACEXTABLE where "Launch_Site" like "%CCA%" limit 5;')


# ### Task 3
# 
# 
# 
# 
# ##### Display the total payload mass carried by boosters launched by NASA (CRS)
# 

# In[38]:


get_ipython().run_line_magic('sql', 'Select SUM("PAYLOAD_MASS__KG_") from SPACEXTABLE where "Customer"="NASA (CRS)";')


# ### Task 4
# 
# 
# 
# 
# ##### Display average payload mass carried by booster version F9 v1.1
# 

# In[39]:


get_ipython().run_line_magic('sql', 'select AVG ("PAYLOAD_MASS__KG_") from SPACEXTABLE where "Booster_Version"="F9 v1.1"')


# ### Task 5
# 
# ##### List the date when the first succesful landing outcome in ground pad was acheived.
# 
# 
# _Hint:Use min function_ 
# 

# In[50]:


get_ipython().run_line_magic('sql', 'Select * from SPACEXTABLE where "Landing_Outcome" like "%success%" order by Date asc limit 1')


# ### Task 6
# 
# ##### List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000
# 

# In[51]:


get_ipython().run_line_magic('sql', 'Select Distinct ("Booster_Version") from SPACEXTABLE where "Landing_Outcome"="Success (drone ship)" AND "PAYLOAD_MASS__KG_" between 4000 and 6000')


# ### Task 7
# 
# 
# 
# 
# ##### List the total number of successful and failure mission outcomes
# 

# In[52]:


get_ipython().run_line_magic('sql', 'Select "Mission_Outcome", Count("Mission_Outcome") from SPACEXTABLE group by "Mission_Outcome"')


# ### Task 8
# 
# 
# 
# ##### List the   names of the booster_versions which have carried the maximum payload mass. Use a subquery
# 

# In[63]:


get_ipython().run_line_magic('sql', 'Select DISTINCT "Booster_Version","PAYLOAD_MASS__KG_" from SPACEXTABLE where "PAYLOAD_MASS__KG_" = (Select MAX("PAYLOAD_MASS__KG_") from SPACEXTABLE)')


# ### Task 9
# 
# 
# ##### List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
# 
# **Note: SQLLite does not support monthnames. So you need to use  substr(Date, 4, 2) as month to get the months and substr(Date,7,4)='2015' for year.**
# 

# In[72]:


get_ipython().run_line_magic('sql', 'Select "Booster_Version", "Launch_Site" FROM SPACEXTABLE where "Landing_Outcome" = "Failure (drone ship)" AND substr(Date,1,4) = \'2015\'')


# ### Task 10
# 
# 
# 
# 
# ##### Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.
# 

# In[65]:


get_ipython().run_line_magic('sql', 'Select "Landing_Outcome", count(*) from SPACEXTABLE where Date between \'2011-06-04\' and \'2017-03-20\' group by "Landing_Outcome" order by 2 desc')


# ### Reference Links
# 
# * <a href ="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20String%20Patterns%20-%20Sorting%20-%20Grouping/instructional-labs.md.html?origin=www.coursera.org">Hands-on Lab : String Patterns, Sorting and Grouping</a>  
# 
# *  <a  href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Built-in%20functions%20/Hands-on_Lab__Built-in_Functions.md.html?origin=www.coursera.org">Hands-on Lab: Built-in functions</a>
# 
# *  <a  href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Sub-queries%20and%20Nested%20SELECTs%20/instructional-labs.md.html?origin=www.coursera.org">Hands-on Lab : Sub-queries and Nested SELECT Statements</a>
# 
# *   <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-3-SQLmagic.ipynb">Hands-on Tutorial: Accessing Databases with SQL magic</a>
# 
# *  <a href= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-4-Analyzing.ipynb">Hands-on Lab: Analyzing a real World Data Set</a>
# 
# 
# 

# ## Author(s)
# 
# <h4> Lakshmi Holla </h4>
# 

# ## Other Contributors
# 
# <h4> Rav Ahuja </h4>
# 

# ## Change log
# | Date | Version | Changed by | Change Description |
# |------|--------|--------|---------|
# | 2021-07-09 | 0.2 |Lakshmi Holla | Changes made in magic sql|
# | 2021-05-20 | 0.1 |Lakshmi Holla | Created Initial Version |
# 

# ## <h3 align="center"> © IBM Corporation 2021. All rights reserved. <h3/>
# 
