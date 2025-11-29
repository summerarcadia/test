import pandas as pd
import pickle 

df = pd.read_csv('who.csv')
df.columns = ['Country', 'Year', 'LE0', 'LE0M', 'LE0F', 'LE60', 'LE60M', 'LE60F', 
              'HALE0', 'HALE0M', 'HALE0F', 'HALE60', 'HALE60M', 'HALE60F']


df = df.drop(0)  # Delete row 0

#Convert to Int for Years
    #direct column access is built-in for pandas
#convert to numbers, make incorrect values NaN, astype 64 can convert to Int. and handle missing value
df['Year'] = pd.to_numeric(df['Year'], errors= 'coerce').astype('int64')

#Convert to Float for data fields
data_columns = ['LE0', 'LE0M', 'LE0F', 'LE60', 'LE60M', 'LE60F', 
                'HALE0', 'HALE0M', 'HALE0F', 'HALE60', 'HALE60M', 'HALE60F']
for col in data_columns:
    df[col] = pd.to_numeric(df[col], errors= 'coerce')


#save df to a pickle file
df.to_pickle("assignment2.pkl")

# new data frame for 'LEO' values. A pivot reshapes data from "long format" to "wide format".
le0_df = df.pivot(index= 'Country', columns= 'Year', values= 'LE0')

# No need to loop through each row, pd can apply operations across rows all tgt.
# Make new columns, axis = 0 (goes DOWN the columns), axis = 1(goes ACROSS columns)
# All automatically ignore missing (NaN) values 
le0_df['Mean'] = le0_df.mean(axis=1)
le0_df['Max'] = le0_df.max(axis=1)
le0_df['Min'] = le0_df.min(axis=1)
le0_df['Std'] = le0_df.std(axis=1)

# Sort by Mean in descending order (it's audo ascending, for descend = ascending = False)
le0_df = le0_df.sort_values(by='Mean', ascending = False)


#save df to a pickle file
le0_df.to_pickle("assignment2-le0.pkl")

# new data frame for 'HALE0' values. A pivot reshapes data from "long format" to "wide format".
hale_df = df.pivot(index= 'Country', columns= 'Year', values= 'HALE0')

hale_df = hale_df.interpolate(axis=1)

# Interpolate across years for each country, e.g estimate 2015 w/ 2014 and 2016 data

hale_df['Mean'] = hale_df.mean(axis=1)
hale_df['Max'] = hale_df.max(axis=1)
hale_df['Min'] = hale_df.min(axis=1)
hale_df['Std'] = hale_df.std(axis=1)
hale_df = hale_df.sort_values(by='Mean', ascending = False)

hale_df.to_pickle("assignment2-hale0.pkl")

print(df.info())
print(hale_df.head())

'''Notes'''
# Coerce:
# Sample messy data : messy_years = ['2020', '2021', 'Unknown', '', '2022', 'N/A']
#     pd.to_numeric(messy_years, errors='raise')   # ERROR - stops at 'Unknown'
#     pd.to_numeric(messy_years, errors='ignore')  # Returns original strings
#     pd.to_numeric(messy_years, errors='coerce')  # [2020, 2021, NaN, NaN, 2022, NaN]


# Astype:
    # Data with NaN
    # data = [2020.0, 2021.0, NaN, 2022.0]

    # data.astype('int')    # ERROR - can't convert NaN to int
    # data.astype('Int64')  # Works! [2020, 2021, <NA>, 2022]