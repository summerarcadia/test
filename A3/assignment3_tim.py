import pandas as pd
import matplotlib.pyplot as plt

#load the dataset
data = pd.read_csv('owid-co2-data.csv')

#drop countries that do not belong to a region using dropna()
data = data.dropna(subset=['iso_code'])

#ffill() missing values with NA
data = data.fillna(method='ffill')

#create the figure with 4 subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# 1. Global Greenhouse Gas Emissions (Top Left)

#pivot the data so that 'year' is the index and each column represents a different metric
pivoted_data = data.pivot(index='year', columns='country', values='total_ghg')

#plot the data for 'World' starting from 1990
world_data = pivoted_data['World'][(pivoted_data.index >= 1990)]
axs[0, 0].plot(world_data.index, world_data.values, color='black') #color is black
axs[0, 0].set_title('Global GHG Emissions')
axs[0, 0].set_xlabel('Year')
axs[0, 0].set_ylabel('Emissions (millions of tons)')

# 2. Top Emitters Per Capita (Top Right)

#filter the data to only include years from 1990 onward
data_recent = data[data['year'] >= 1990]

#pivot the data
pivoted_data = data_recent.pivot(index='year', columns='country', values='ghg_per_capita')

#find the top 5 emitters in 2018
top_emitters = pivoted_data.loc[2018].nlargest(5)

#plot the data for the top emitters
for country in top_emitters.index:
    axs[0, 1].plot(pivoted_data.index, pivoted_data[country], label=country)

axs[0, 1].set_title('Top Emitters per Capita')
axs[0, 1].set_xlabel('Year')
axs[0, 1].set_ylabel('GHG Emissions (tons per year)')
axs[0, 1].legend()


# 3. Regional CO2 Emissions for 2018 (Bottom Left)

#use dictionary to put countries under their respective continents
regions = {
    'Africa': ['Algeria', 'Nigeria', 'South Africa', 'Egypt'],  
    'Asia': ['China', 'India', 'Japan', 'South Korea'],
    'Oceania': ['Australia', 'New Zealand'],
    'North America': ['United States', 'Canada', 'Mexico'],
    'South America': ['Brazil', 'Argentina', 'Colombia', 'Chile']
}

#aggregate the CO2 per capita data for the specified regions
region_means = {}
for region, countries in regions.items():
    regional_data = data[(data['year'] == 2018) & (data['country'].isin(countries))]
    if not regional_data.empty:
        region_means[region] = regional_data['co2_per_capita'].mean()

#plot the bar graph
axs[1, 0].bar(region_means.keys(), region_means.values(), label='2018', color='black')
axs[1, 0].set_title('2018 Regional CO2 Emissions')
axs[1, 0].set_xlabel('')
axs[1, 0].set_ylabel('CO2 Per Capita (tons per year)')
axs[1, 0].legend(title='Year', loc='upper left') #put legend 

# 4. Histogram of CO2 Emissions Per Capita (Bottom Right)
world_data = data[data['country'] != 'World']
axs[1, 1].hist(world_data[world_data['year'] == 2018]['co2_per_capita'].dropna(), bins=50)
axs[1, 1].set_title('CO2 Emissions per Capita')
axs[1, 1].set_xlabel('CO2 Emissions (tons per year per person)')
axs[1, 1].set_ylabel('Number of Countries')

#save the figure
plt.tight_layout()
plt.savefig('assignment3.png', dpi=300)
plt.show()
