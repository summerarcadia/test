import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
df = pd.read_csv('owid-co2-data.csv')

df_pivoted = df.pivot_table( index = 'year', columns = 'country', values = 'total_ghg') 
print(df_pivoted)

##LINE GRAPH 1

#set up a subplot
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))

#dataframe[condition] = it's like a if statement, give me the rows where condition is true
#it's a series (list of pairs, year + world values)
world_data = df_pivoted['World']
clean_world_data = world_data[(world_data > 0) & (world_data.notna())]
#i don't get the &
#creates a 2x2 axes for plotting, country year combination
axes[0,0].plot(clean_world_data.index, clean_world_data, color = 'black')
axes[0,0].set_xlabel("Year")
axes[0,0].set_ylabel("Emissions (millions of tons")
axes[0,0].set_title("Global GHG Emissions")


##GRAPH 2

df_pivoted_per_capita = df.pivot_table( index = 'year', columns = 'country', values = 'ghg_per_capita') 

#ffill() = fills missing values with the last valid before it, save it back to the same varaible
df_pivoted_per_capita = df_pivoted_per_capita.ffill()

## .loc[2023] locates the row where index = 2023, returns all country values for that year
row_2023 = df_pivoted_per_capita.loc[2023]
sort_2023 = row_2023.sort_values(ascending = False) 
top_five = sort_2023[:5] # gives u a series of top 5 country and their 2023 values 
top_five_countries = top_five.index.tolist() # converts the index (names of countries) => list

#now have top 5 countries, do time series for each 5
for country in top_five_countries:
    axes[0,1].plot(df_pivoted_per_capita.index,  # All years (x-axis)
                   df_pivoted_per_capita[country],
                   label = country)  # That country's values (y-axis)

axes[0,1].set_xlabel("Year")
axes[0,1].set_ylabel("CO2 Emissions (tons per year)")
axes[0,1].set_title("Top Emitters per Capita")
axes[0,1].legend(top_five_countries)


##GRAPH 3
regions = ['Africa','Asia', 'Oceania', 'North America', 'South America']
df_region_filtered = df[(df['year'] == 2023) & (df['country'].isin(regions))]

df_region_filtered['country'] = pd.Categorical(
    df_region_filtered['country'], 
    categories=regions, 
    ordered=True
)

df_region_filtered = df_region_filtered.sort_values('country')

axes[1,0].bar(df_region_filtered['country'], df_region_filtered['co2_per_capita'],
               color = 'black',label = '2023')
axes[1,0].set_xlabel("")
axes[1,0].tick_params(axis='x', rotation=90)
axes[1,0].set_ylabel("CO2 per Capita (tons per year)")
axes[1,0].set_title("2023 Regional CO2 Emissions")
axes[1,0].legend(title = 'year')

##GRAPH 4
# Drop rows without iso_code first (these are regions or aggregates)
df = df.dropna(subset=['iso_code'])
df_co2_per_capita = df.pivot_table(index='year', columns='country', values='co2_per_capita')
df_co2_per_capita = df_co2_per_capita.ffill()
data_2023 = df_co2_per_capita.loc[2023].dropna()

# Bottom-right histogram
axes[1, 1].hist(data_2023, bins=50)

# Labels and title
axes[1, 1].set_xlabel("CO2 Emissions (tons per year per person)")
axes[1, 1].set_ylabel("Number of Countries")
axes[1, 1].set_title("CO2 Emissions per Capita")

# BONUS: Automatically find the first and last years with CO2 reports
years_with_data = df['year'].dropna().unique()
first_year = int(years_with_data.min())
last_year = int(years_with_data.max())

print(f"CO2 data is available from {first_year} to {last_year}.")


plt.tight_layout()
plt.savefig("assignment3.png", dpi=300)
plt.show()

