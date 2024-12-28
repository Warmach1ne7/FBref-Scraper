import pandas as pd
import os
season = ['2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019', '2017-2018', '2016-2017', '2015-2016', '2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011', '2009-2010']
leaguelink = "https://fbref.com/en/comps/10/"
leagueurls = []
for year in season: 
    leagueurls.append(leaguelink + year + "/"+year+"-Championship-Stats")
# Convert list to DataFrame
urls_joined = ", ".join(leagueurls)
# Convert the string into a DataFrame with one row and one column
for url in leagueurls:
    print(url,",")
