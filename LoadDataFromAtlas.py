import pandas
import numpy as np

file = pandas.ExcelFile('FdaFoodAtlas.xls')

population = pandas.read_excel(file, sheetname='Supplemental Data - County', index_col='FIPS')
population = population['2010 Census Population']

health = pandas.read_excel(file, sheetname='HEALTH', index_col='FIPS')
health = health[['PCT_DIABETES_ADULTS10']]
health = health * .01

access = pandas.read_excel(file, sheetname='ACCESS', index_col='FIPS')
access = access['LACCESS_POP10']

access_pct = pandas.DataFrame()
access_pct['LACCESS_POP10'] = access.div(population, axis='index')
access_pct = access_pct[np.isfinite(access)]

assistance = pandas.read_excel(file, sheetname='ASSISTANCE', index_col='FIPS')
assistance = assistance[['PCT_SNAP14']]
assistance = assistance * .01

# percents, except for med household income that's in dollars
socioeconomic = pandas.read_excel(file, sheetname='SOCIOECONOMIC', index_col='FIPS')
race = socioeconomic[['PCT_NHWHITE10', 'PCT_NHBLACK10', 'PCT_HISP10', 'PCT_NHASIAN10', 'PCT_NHNA10', 'PCT_NHPI10']]
financial = socioeconomic [['MEDHHINC10', 'METRO13']]
race = race * .01

# count of shops
stores = pandas.read_excel(file, sheetname='STORES', index_col='FIPS')
stores = stores[['GROC12', 'SUPERC12', 'CONVS12', 'SPECS12']]

# count of stores
restaurants = pandas.read_excel(file, sheetname='RESTAURANTS', index_col='FIPS')
restaurants = restaurants[['FFR12', 'FSR12']]

# count of farms, counts of acres
local = pandas.read_excel(file, sheetname='LOCAL', index_col='FIPS')
local = local[['FMRKT13', 'VEG_ACRES07', 'ORCHARD_ACRES07', 'BERRY_ACRES07']]
markets = local['FMRKT13'].fillna(0)
veggies = local['VEG_ACRES07'].fillna(0)
orchard = local['ORCHARD_ACRES07'].fillna(0)
berries = local[ 'BERRY_ACRES07'].fillna(0)

local['TOTAL_FARM_ACRES07'] = veggies + orchard + berries

local = local[ 'TOTAL_FARM_ACRES07']


full_atlas_set = pandas.concat([population, health, access_pct, assistance, race, financial, stores, restaurants, markets, local], axis=1, join='inner')

full_atlas_set.to_pickle('full_merged_atlas.p')
population.to_pickle('full_zipcode_set.p')
