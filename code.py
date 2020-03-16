# --------------
import pandas as pd 

# Read the data using pandas module.
import pandas as pd
import numpy as np
df_ipl = pd.read_csv(path)
df_ipl.shape

# Find the list of unique cities where matches were played
print('\nVenues Played At:',df_ipl['city'].unique())     

# Find the columns which contains null values if any ?
df_ipl.isnull().sum()

# List down top 5 most played venues
venues = df_ipl.groupby('venue')['match_code'].nunique().sort_values(ascending=False)
print('Top 5 favoured grounds are : \n',venues[0:5])

# Make a runs count frequency table
runs_counts = df_ipl['runs'].value_counts()
print('Runs count frequency table:\n',runs_counts)

# How many seasons were played and in which year they were played 
df_ipl['year'] = df_ipl['date'].apply(lambda x : x[:4])

print('The no. of seasons that were played are :', len(df_ipl['year'].unique()))
print('Seasons played were in :', df_ipl['year'].unique())

# No. of matches played per season
matches_per_season = df_ipl.groupby('year')['match_code'].nunique()
print('Matches held per season are :\n', matches_per_season)

# Total runs across the seasons
runs_per_season = df_ipl.groupby('year')['total'].sum()
print('total runs scored per season are: \n', runs_per_season)

# Teams who have scored more than 200+ runs. Show the top 10 results
high_scores=df_ipl.groupby(['match_code', 'inning','team1','team2'])['total'].sum().reset_index() 
high_scores = high_scores[high_scores['total'] >= 200]
high_scores.nlargest(10, 'total')

# What are the chances of chasing 200+ target
high_scores1 = high_scores[high_scores['inning']==1]
high_scores2 = high_scores[high_scores['inning']==2]
high_scores1=high_scores1.merge(high_scores2[['match_code','inning', 'total']], on='match_code')
high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_x':'inning1_runs','total_y':'inning2_runs'},inplace=True)
high_scores1=high_scores1[high_scores1['inning1_runs']>=200]
high_scores1['is_score_chased']=1
high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs']<=high_scores1['inning2_runs'], 
                                           'yes', 'no')
chances = high_scores1['is_score_chased'].value_counts()
print('The chances of chasing a target of 200+ in 1st innings are : \n' , chances[1]/14*100)

# Which team has the highest win count in their respective seasons ?
match_wise_data = df_ipl.drop_duplicates(subset = 'match_code', keep='first').reset_index(drop=True)
match_wise_data.groupby('year')['winner'].value_counts(ascending=False)


