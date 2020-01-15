import pandas as pd
import numpy as np

# World Bank Data
df_social_progress_index = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx', sheet_name='Social Progress Index')
df_basic_human_needs = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx', sheet_name='Basic Human Needs')
df_foundations_of_wellbeing = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx',
                                            sheet_name='Foundations of Wellbeing')
df_opportunity = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx', sheet_name='Opportunity')

df_final = pd.read_excel('.\\Data\\Final df.xlsx')
df_final.iloc[:, 5] = df_final.iloc[:, 5]*100
data_2016 = pd.read_csv('.\\Data\\cost-of-living-2016.csv')
data_2017 = pd.read_csv('.\\Data\\cost-of-living-2017.csv')
data_2018 = pd.read_csv('.\\Data\\cost-of-living-2018.csv')

# Importing Human Development Index DataFrame
df_hdi = pd.read_csv('.\\Data\\human-development-index.csv', header=0, quotechar="'")

for index, row in df_hdi.iterrows():
    if row['Year'] < 2017:
        df_hdi.drop(index, inplace=True)

df_hdi = df_hdi.drop(['Year'], axis=1).reset_index(drop=True)
df_hdi = df_hdi.rename(columns={" ((0-1; higher values are better))": "2017", 'Entity': 'Country'})

data_2016 = data_2016.loc[:, ['City', 'Country', 'Cost.of.Living.Index', 'Rent.Index', 'Groceries.Index']]
data_2016.rename(columns={'Cost.of.Living.Index': 'CLI_16', 'Rent.Index': 'R_16', 'Groceries.Index': 'G_16'},
                 inplace=True)

data_2017 = data_2017.loc[:, ['City', 'Country', 'CLI', 'Rent Index', 'Groceries Index']]
data_2017.rename(columns={'CLI': 'CLI_17', 'Rent Index': 'R_17', 'Groceries Index': 'G_17'}, inplace=True)

data_2018 = data_2018.loc[:, ['City', 'Cost of Living Index', 'Rent Index', 'Groceries Index']]
data_2018.rename(columns={'Cost of Living Index': 'CLI_18', 'Rent Index': 'R_18', 'Groceries Index': 'G_18'},
                 inplace=True)

city = []
country = []
for value in data_2018.loc[:, 'City']:
    city.append(value.split(',')[0])
    country.append(value.split(',')[-1])

data_2018.insert(1, 'Country', pd.DataFrame(country))
data_2018.loc[:, 'City'] = city

all_data = data_2016.merge(data_2017, how='outer', left_on='City', right_on='City')
all_data = all_data.merge(data_2018, how='outer', left_on='City', right_on='City')

all_data.isna().sum()

temp_data = all_data.loc[:, ['Country_x', 'Country_y', 'Country']]
temp_data.replace(np.nan, 0, inplace=True)
all_data.loc[:, ['Country_x', 'Country_y', 'Country']] = temp_data

countries_complete = []
for i in range(all_data.shape[0]):
    if all_data.loc[i, 'Country'] != 0:
        countries_complete.append(all_data.loc[i, 'Country'])
    elif all_data.loc[i, 'Country_y'] != 0:
        countries_complete.append(all_data.loc[i, 'Country_y'])
    else:
        countries_complete.append(all_data.loc[i, 'Country_x'])

countries_complete = [i.strip() for i in countries_complete]  # eliminates spaces
countries_complete = ['United States' if len(i) == 2 else i for i in countries_complete]

all_data['Country_final'] = pd.DataFrame(countries_complete)
all_data = all_data.drop(columns=['Country_x', 'Country_y', 'Country'])
all_data = all_data.rename(columns={'Country_final': 'Country'})

df_cost_living = all_data.loc[:, ['City', 'Country', 'CLI_16', 'CLI_17', 'CLI_18']]
df_rent = all_data.loc[:, ['City', 'Country', 'R_16', 'R_17', 'R_18']]
df_groceries = all_data.loc[:, ['City', 'Country', 'G_16', 'G_17', 'G_18']]

df_cost_living.drop_duplicates(subset=['City', 'Country'], inplace=True)
df_cost_living.reset_index(drop=True, inplace=True)
df_rent.drop_duplicates(subset=['City', 'Country'], inplace=True)
df_rent.reset_index(drop=True, inplace=True)
df_groceries.drop_duplicates(subset=['City', 'Country'], inplace=True)
df_groceries.reset_index(drop=True, inplace=True)

df_temperature = pd.read_csv('.\\Data\\avg_temperature.csv', header=0, sep=';')
df_temperature['Temperature'] = df_temperature['Temperature'].map(lambda x: str(x.replace(',', '.')))
df_temperature['Temperature'] = pd.to_numeric(df_temperature['Temperature'])

df_precipitation = pd.read_csv('.\\Data\\API_AG.LND.PRCP.MM_DS2_en_csv_v2_620809.csv')

df_data_scientist_salary = pd.read_excel('.\\Data\\Data Scientists GROSS Anual Compensation Around the World.xlsx')
df_wage = pd.read_excel('.\\Data\\wage.xlsx')
df_wage1 = df_wage.melt(id_vars='Country',
                        var_name='Year',
                        value_name='Wage')

df_happiness_score = pd.read_excel('.\\Data\\Hapiness Score.xlsx')


# Joining all dataframes
df_cost_living_mean = df_cost_living.set_index('Country').groupby(level='Country').mean().reset_index()
df_groceries_mean = df_groceries.set_index('Country').groupby(level='Country').mean().reset_index()
df_rent_mean = df_rent.set_index('Country').groupby(level='Country').mean().reset_index()


df_countries = [df_data_scientist_salary, df_foundations_of_wellbeing.loc[:,['Country', 2018]],
                df_hdi, df_opportunity.loc[:,['Country', 2018]],
                df_social_progress_index.loc[:,['Country', 2018]], df_temperature, df_wage.loc[:,['Country', '2017']],
                df_cost_living_mean.loc[:,['Country','CLI_18']], df_groceries_mean.loc[:,['Country','G_18']],
                df_rent_mean.loc[:,['Country','R_18']], df_happiness_score.loc[:,['Country',2018]]]
                # falta precipitation

df = df_basic_human_needs.loc[:,['Country', 2018]]

for dataframe in df_countries:
    cols = dataframe.columns
    if 'Code' in cols:
        dataframe = dataframe.drop(columns='Code')
    if 'Country Name' in cols:
        dataframe = dataframe.rename(columns={'Country Name':'Country'})
    df = pd.merge(df, dataframe, how='outer', on='Country')


df.columns = ['Country', 'Basic Human Needs','Data Scientist Salary', 'Foundations of Wellbeing', 'HDI', 'Opportunity',
               'Social Progress Index', 'Temperature', 'Wage', 'Cost of Living', 'Groceries', 'Rent',
               'Happiness Score']


del all_data, countries_complete, data_2018, data_2017, data_2016, city, country, i, temp_data, value, index, row, dataframe