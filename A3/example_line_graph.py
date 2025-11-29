#!/usr/bin/env python
# coding: utf-8

# In[16]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[17]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = np.random.randint(5,30,size=10)
series = pd.Series(data)

fig = plt.plot(series)
plt.title("Example Line Graph") # For subplots, you'll need to look at the set_title() method
plt.xlabel("Year")              # See textbook for example
plt.ylabel("Value")


# In[ ]:




