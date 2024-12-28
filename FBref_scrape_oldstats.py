#scrape FBRef.com for team and player data
# Based upon: https://medium.com/@smehta/scrape-and-create-your-own-beautiful-dataset-from-sports-reference-com-using-beautifulsoup-python-c26d6920684e
# and usefull input from: https://github.com/BenKite/baseball_data/blob/master/baseballReferenceScrape.py

#TO DO: get table column names from html

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys, getopt
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup  # Assuming you're using BeautifulSoup for HTML parsing

import pandas as pd

def add_data_to_dataframe(table):
    # Parse team_table
    df_stats = {}
    
    rows_squad = table.find_all('tr')
    for row in rows_squad:
        # Get the team name (if it exists) and initialize 'squad' column
        th_element = row.find('th')
        if th_element:
            name = th_element.get("data-stat")
            value = th_element.text.strip().encode().decode("utf-8")
            if name in df_stats:
                df_stats[name].append(value)
            else:
                df_stats[name] = [value]
        
            # Loop through all 'td' elements in the row
            for cell in row.find_all("td"):
                column_name = cell.get("data-stat")  # Get the column name from 'data-stat'
                cell_text = cell.text.strip().encode().decode("utf-8") if cell.text else None

                # Append data to corresponding list in df_stats dictionary
                if column_name in df_stats:
                    df_stats[column_name].append(cell_text)
                else:
                    df_stats[column_name] = [cell_text]
        else:
            print(f"Warning: Missing 'squad' column in row {row}")

    # Find the maximum length of the lists
    max_len = max(len(lst) for lst in df_stats.values())

    # Pad each list to ensure consistent length
    for key in df_stats:
        if len(df_stats[key]) < max_len:
            df_stats[key].extend([None] * (max_len - len(df_stats[key])))
    
    # Create DataFrame from the dictionary
    df = pd.DataFrame.from_dict(df_stats)
    return df

# Example usage
# Define the columns you want across all tables
# Assuming `team_stats_table` is an HTML table element obtained from BeautifulSoup
# df_squad = add_data_to_dataframe(team_stats_table, features_wanted_squad)
def safe_assign_data(table, processing_function):  
    if table:
        return processing_function(table)
    else:
        return None  # Assign None if the table is empty or does not exist
def scrapeURL(url):
    df1 = None
    df_squad = None
    df_vs_squad = None
    df_goalkeeping = None
    df_squad_shooting = None
    df_vs_squad_shooting = None
    df_passing = None
    df_vs_passing = None
    df_goal_shot = None
    df_vs_goal_shot = None
    df_defence = None
    df_possession = None
    res = requests.get(url)
    if(res.status_code==200):
        print("successfull")
    else:
        print("unsuccessfull ",res.status_code)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    #player_stat = all_tables[2]
    #df_player_stat = add_data_to_dataframe(player_stat)
    df1 = add_data_to_dataframe(all_tables[0])
    df_squad = add_data_to_dataframe(all_tables[2])
    df_vs_squad = add_data_to_dataframe(all_tables[3])
    df_goalkeeping = add_data_to_dataframe(all_tables[4])
    df_squad_shooting = add_data_to_dataframe(all_tables[6])
    df_vs_squad_shooting = add_data_to_dataframe(all_tables[7])
    return df1,df_squad,df_vs_squad,df_goalkeeping,df_squad_shooting,df_vs_squad_shooting
    
def main(argv):
    urls = pd.DataFrame()
    
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print('FBref_scrape.py -f <url_csv_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('FBref_scrape.py -f <url_csv_file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            urls = pd.read_csv(arg,delimiter=',')

            
    
    for url in urls:
        print("from url: ",url)
        df1, df_squad, df_vs_squad, df_goalkeeping, df_squad_shooting, df_vs_squad_shooting = scrapeURL(url)
        #df = scrapeURL(url)
        #print(df.head())
        k = url.rfind("/")
        output_name = url[k+1:]
        """output_file = str(output_name) + 'players.xlsx'
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Standings", index=False)
        """
        output_file = str(output_name) + '.xlsx'
        # Dynamically write dataframes to Excel sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
      # Replace `output_file` with your actual file path
            if df1 is not None and not df1.empty:
                df1.to_excel(writer, sheet_name='Standings', index=False)
            if df_squad is not None and not df_squad.empty:
                df_squad.to_excel(writer, sheet_name='Squad', index=False)
            if df_vs_squad is not None and not df_vs_squad.empty:
                df_vs_squad.to_excel(writer, sheet_name='Vs Squad', index=False)
            if df_goalkeeping is not None and not df_goalkeeping.empty:
                df_goalkeeping.to_excel(writer, sheet_name='Goalkeeping', index=False)
            if df_squad_shooting is not None and not df_squad_shooting.empty:
                df_squad_shooting.to_excel(writer, sheet_name='Squad Shooting', index=False)
            if df_vs_squad_shooting is not None and not df_vs_squad_shooting.empty:
                df_vs_squad_shooting.to_excel(writer, sheet_name='Vs Squad Shooting', index=False)
        
        time.sleep(5)
    


if __name__ == "__main__":
   main(sys.argv[1:])
   