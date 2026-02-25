import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("C:/ipl_data.csv")
print(data.head())
print(data.shape)
print(data.columns.tolist())
print(data.info())
print(data.isnull().sum())
data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')
data['season'] = data['date'].dt.year

'''DATA CLEANING 
1- MISSING VALUES KO HANDLE KRNA 
2- COLUMN NAMES STANDARDIZE KRNA 
3- AGR DATE HAI, USKO DATE FORMAT ME CONVERT KRNA
'''
data["runs"] = data["runs"].fillna(0)
data["wickets"] = data["wickets"].fillna(0)

conn = sqlite3.connect("ipl_database.data")
cursor = conn.cursor()

data.to_sql("ipl_matches",conn,if_exists='replace',index=False)
conn.close()


conn = sqlite3.connect('ipl_database.data')
print("\n2.TOP 10 BATSMAN LIST")


top_batsmen = data.groupby('batsman')['runs'].sum().sort_values(ascending=False).head(10)
print("top 10 batsman list :\n", top_batsmen)


top_bowlers = data.groupby('bowler')['wickets'].sum().sort_values(ascending=False).head(10)
print("\ntop 10 bowler:\n", top_bowlers)

runs_per_season = data.groupby('season')['runs'].sum()
print("\ntotal runs per season\n", runs_per_season)

top_batting_team = data.groupby('bat_team')['runs'].sum().sort_values(ascending=False)
print("\ntotal runs scored by the team:\n", top_batting_team)

data['wickets'] = pd.to_numeric(data['wickets'], errors='coerce')

# visualization 
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 1. TOP 10 BATSMAN BAR CHART
plt.subplot(2, 2, 1)
top_batsmen.plot(kind='bar', color='skyblue')
plt.title('top 10 batsman (total runs)')
plt.xlabel('batsman')
plt.ylabel('total runs')
plt.xticks(rotation=45)

# 2. top 10 bowler bar chart
plt.subplot(2, 2, 2)
top_bowlers.plot(kind='bar', color='lightcoral')
plt.title('top bowler (total wicket)')
plt.xlabel('bowling')
plt.ylabel('total wicket')
plt.xticks(rotation=45)

# 3.total runs per season(line chrt)
plt.subplot(2, 2, 3)
runs_per_season.plot(kind='line', marker='o', color='green')
plt.title('season runs')
plt.xlabel('season')
plt.ylabel('total runs')
plt.grid(True)

# 4. total runs scored by the team ( bar chart)
plt.subplot(2, 2, 4)
top_batting_team.head(5).plot(kind='bar', color='gold')
plt.title('total runs scored by the team (top 5)')
plt.xlabel('team')
plt.ylabel('total runs')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()