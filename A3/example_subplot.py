#!/usr/bin/env python
# coding: utf-8

# In[6]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[8]:


import matplotlib.pyplot as plt
import pandas as pd

# Create the figure/subfigure
fig = plt.figure()
sub = fig.add_subplot(2,2,1)

# Create a DataFrame and Plot it
df = pd.util.testing.makeDataFrame()
df.plot.bar(ax=sub,color="black")   ## Note here the ax= to set proper subplot
sub.set_title("Random Bar Graph")


# In[ ]:





# In[ ]:




