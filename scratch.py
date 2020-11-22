import pandas as pd
import requests
import io

url = "https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv?_ga=2.202367956.492409862.1605773777-1333374011.1605773777"
s=requests.get(url).content
f=pd.read_csv(io.StringIO(s.decode('utf-8')))
pd.DataFrame.from_records(f).to_csv("covidcasesbycounty.csv")

states = f['State'].unique()
print(min(f['11/19/20']))
dict = {}

fips = f['countyFIPS'].unique()

print(fips)

for fip in fips:
    dict[fip] = pd.DataFrame(f.loc[f['countyFIPS'] == fip])


print(dict[1003]['11/19/20'])
