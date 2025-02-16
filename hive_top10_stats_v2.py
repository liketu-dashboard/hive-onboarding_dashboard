import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter
import pyodbc
import plotly.express as px

def hive_top10_stats(rewards_period, account):

    TOP = 10

    st.header(f"Onboarded by {account}")


    st.markdown(
    """
    The following apps names are grouped together:
    - All apps with a slash ('/'), e.g. 'peakd/1.0', 'peakd/2.0', 'peakd/3.0' grouped together with 'peakd'
    - All app names starting with 'liketu', e.g. 'liketu', 'liketu-mobile-xxx'
    - All app names starting with '3speak'
    - Small and capital letters: '3SpeakComment' grouped together with '3speak'
    """
    )

    now = datetime.datetime.utcnow()
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=vip.hivesql.io;'
                            'Database=DBHive;'
                            f'uid={st.secrets["DB_USERNAME"]};pwd={st.secrets["DB_PASSWORD"]}')
    SQLCommand = f"""
        SELECT 
            JSON_VALUE(Comments.json_metadata, '$.app') AS appname,
            Comments.author,
            Comments.depth,
            Comments.category,            
            Comments.last_payout,
            Comments.pending_payout_value,
            Comments.created
        FROM 
            Comments
        INNER JOIN 
            TxAccountCreates 
        ON 
            Comments.author = TxAccountCreates.new_account_name
        WHERE 
            TxAccountCreates.creator = '{account}' AND
            ISJSON(Comments.json_metadata) > 0 AND
            Comments.created >= '{(now-timedelta(rewards_period+1)).strftime('%Y-%m-%d %H:%M:%S')}'    """

    df = pd.read_sql(SQLCommand, connection)

    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=vip.hivesql.io;'
                            'Database=DBHive;'
                            f'uid={st.secrets["DB_USERNAME"]};pwd={st.secrets["DB_PASSWORD"]}')
    SQLCommand = """
    SELECT
        Communities.name,
        Communities.title
    FROM
        Communities
    """

    df_communities = pd.read_sql(SQLCommand, connection).drop_duplicates()
    connection.close()
    # pending rewards have date 12/31/1969

    df_pending_rewards = df[df['last_payout'].dt.year < 2000].fillna('')
    
    # Turn all letters small
    df_pending_rewards['app'] = df_pending_rewards['appname'].str.lower()
    # Only take left part before slash if any
    df_pending_rewards.loc[:, 'app'] = df_pending_rewards.loc[:, 'app'].str.split('/').str[0]

    # If 'appname' starts with 'liketu', then 'app' value should be 'liketu'
    # Same with '3speak'
    df_pending_rewards.loc[df_pending_rewards['app'].fillna('').str.lower().str.startswith('liketu'), 'app'] = 'liketu'
    df_pending_rewards.loc[df_pending_rewards['app'].fillna('').str.lower().str.startswith('3speak'), 'app'] = '3speak'
    df_pending_rewards = df_pending_rewards[df_pending_rewards['app'] != '']

    df_pending_rewards_grouped_app = df_pending_rewards.groupby('app').agg(
        num_interactions=('app', 'size'),
        unique_authors=('author', 'nunique'),
        total_pending_rewards=('pending_payout_value', 'sum')
    ).reset_index()

    for stats in df_pending_rewards_grouped_app.columns[1:]:
        df_pending_rewards_grouped_app[f'rank {stats}'] = df_pending_rewards_grouped_app[stats].rank(method='min', ascending=False).astype(int)
    df_pending_rewards_grouped_app['percentage_total_pending_rewards'] = df_pending_rewards_grouped_app['total_pending_rewards']/df_pending_rewards_grouped_app['total_pending_rewards'].sum()    

    df_pending_rewards_grouped_app_sorted_by_num_interactions =  df_pending_rewards_grouped_app.sort_values(by = "num_interactions", ascending = False).head(TOP).reset_index(drop = True)
    if not 'liketu' in df_pending_rewards_grouped_app_sorted_by_num_interactions['app'].to_list():
        df_pending_rewards_grouped_app_sorted_by_num_interactions = pd.concat([df_pending_rewards_grouped_app_sorted_by_num_interactions, df_pending_rewards_grouped_app.loc[df_pending_rewards_grouped_app['app'] == 'liketu']])
        df_pending_rewards_grouped_app_sorted_by_num_interactions['app'] = df_pending_rewards_grouped_app_sorted_by_num_interactions['app'].replace("liketu", f"liketu (rank {df_pending_rewards_grouped_app_sorted_by_num_interactions[df_pending_rewards_grouped_app_sorted_by_num_interactions['app'] == 'liketu']['rank num_interactions'].squeeze()})")
    df_pending_rewards_grouped_app_sorted_by_num_interactions['color'] = df_pending_rewards_grouped_app_sorted_by_num_interactions['app'].apply(lambda x: 'blue' if x.startswith('liketu') else 'red')    

    df_pending_rewards_grouped_app_sorted_by_unique_authors =  df_pending_rewards_grouped_app.sort_values(by = "unique_authors", ascending = False).head(TOP).reset_index(drop = True)
    if not 'liketu' in df_pending_rewards_grouped_app_sorted_by_unique_authors['app'].to_list():
        df_pending_rewards_grouped_app_sorted_by_unique_authors = pd.concat([df_pending_rewards_grouped_app_sorted_by_unique_authors, df_pending_rewards_grouped_app.loc[df_pending_rewards_grouped_app['app'] == 'liketu']])
        df_pending_rewards_grouped_app_sorted_by_unique_authors['app'] = df_pending_rewards_grouped_app_sorted_by_unique_authors['app'].replace("liketu", f"liketu (rank {df_pending_rewards_grouped_app_sorted_by_unique_authors[df_pending_rewards_grouped_app_sorted_by_unique_authors['app'] == 'liketu']['rank unique_authors'].squeeze()})")
    df_pending_rewards_grouped_app_sorted_by_unique_authors['color'] = df_pending_rewards_grouped_app_sorted_by_unique_authors['app'].apply(lambda x: 'blue' if x.startswith('liketu') else 'red')    

    df_pending_rewards_grouped_app_sorted_by_total_pending_rewards =  df_pending_rewards_grouped_app.sort_values(by = "total_pending_rewards", ascending = False).head(TOP).reset_index(drop = True)
    if not 'liketu' in df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['app'].to_list():
        df_pending_rewards_grouped_app_sorted_by_total_pending_rewards = pd.concat([df_pending_rewards_grouped_app_sorted_by_total_pending_rewards, df_pending_rewards_grouped_app.loc[df_pending_rewards_grouped_app['app'] == 'liketu']])
        df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['app'] = df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['app'].replace("liketu", f"liketu (rank {df_pending_rewards_grouped_app_sorted_by_total_pending_rewards[df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['app'] == 'liketu']['rank total_pending_rewards'].squeeze()})")
    df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['color'] = df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['app'].apply(lambda x: 'blue' if x.startswith('liketu') else 'red')    

    st.subheader('HIVE Top 10 DApps')
    col1, col2, col3 = st.columns(3)

    fig = px.bar(df_pending_rewards_grouped_app_sorted_by_num_interactions[::-1], x="num_interactions", y="app", orientation='h', height = 100 + 30* TOP,
             title=f"Top{TOP} apps on Hive, by number of interactions<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_app_sorted_by_num_interactions[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Number of interactions', range = [0, 1.2* df_pending_rewards_grouped_app_sorted_by_num_interactions['num_interactions'].max()])
    col1.write('Top 10 HIVE DApps, by number of interactions')
    col1.plotly_chart(fig,use_container_width=True)

    fig = px.bar(df_pending_rewards_grouped_app_sorted_by_unique_authors[::-1], x="unique_authors", y="app", orientation='h', height = 100 + 30* TOP,
             title=f"Top{TOP} apps on Hive, by number of users who post/comment<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_app_sorted_by_unique_authors[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Number of users who post/comment', range = [0, 1.2* df_pending_rewards_grouped_app_sorted_by_unique_authors['unique_authors'].max()])
    col2.write('Top 10 HIVE DApps, by number of users who posted and commented')    
    col2.plotly_chart(fig,use_container_width=True)

    fig = px.bar(df_pending_rewards_grouped_app_sorted_by_total_pending_rewards[::-1], x="total_pending_rewards", y="app", orientation='h', height = 100 + 30* TOP,
             title=f"Top{TOP} apps on Hive, by HIVE pending rewards<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_app_sorted_by_total_pending_rewards[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Pending HIVE rewards', range = [0, 1.2* df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['total_pending_rewards'].max()])
    col3.write('Top 10 HIVE Apps, by HIVE pending rewards')
    col3.plotly_chart(fig,use_container_width=True)

    col1, col2, col3 = st.columns(3)
    fig = px.bar(df_pending_rewards_grouped_app_sorted_by_total_pending_rewards[::-1], x="percentage_total_pending_rewards", y="app", orientation='h', height = 100 + 30* TOP,
                title=f"Top{TOP} apps on Hive, by HIVE pending rewards (in percentage)<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_app_sorted_by_total_pending_rewards[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Pending HIVE pending rewards (in percentage)', tickformat = '.2%', range = [0, 1.2* df_pending_rewards_grouped_app_sorted_by_total_pending_rewards['percentage_total_pending_rewards'].max()])
    col1.write('Top 10 HIVE Apps, by pending rewards (in percentage)')
    col1.plotly_chart(fig,use_container_width=True)

    top10_apps = ['liketu']
    for stats in ['num_interactions', 'unique_authors', 'total_pending_rewards']:
        top10_apps += df_pending_rewards_grouped_app.sort_values(by = stats, ascending = False).head(TOP)['app'].to_list()
    top10_apps = list(set(top10_apps))
    df_pending_rewards_grouped_app_top10 = df_pending_rewards_grouped_app[df_pending_rewards_grouped_app['app'].isin(top10_apps)]
    df_pending_rewards_grouped_app_top10['color'] = list(np.where(df_pending_rewards_grouped_app_top10['app'] == 'liketu', 'blue', 'red'))

    df_pending_rewards_grouped_app_top10['average_pending_rewards_per_active_user'] = df_pending_rewards_grouped_app_top10['total_pending_rewards']/df_pending_rewards_grouped_app_top10['unique_authors']
    df_pending_rewards_grouped_app_top10['average_pending_rewards_per_interaction'] = df_pending_rewards_grouped_app_top10['total_pending_rewards'] / df_pending_rewards_grouped_app_top10['num_interactions']
    df_pending_rewards_grouped_app_top10['average_interactions_per_active_user'] = df_pending_rewards_grouped_app_top10['num_interactions'] / df_pending_rewards_grouped_app_top10['unique_authors']
    df_pending_rewards_grouped_app_top10['color'] = list(np.where(df_pending_rewards_grouped_app_top10['app'] == 'liketu', 'blue', 'red'))

    col1, col2, col3 = st.columns(3)    

    fig = px.bar(df_pending_rewards_grouped_app_top10.sort_values(by='average_interactions_per_active_user', ascending = False)[::-1], 
             x="average_interactions_per_active_user", 
             y="app", 
             orientation='h', 
             height = 100 + 30* len(top10_apps),
             title=f"Top{TOP} apps on Hive, Average interactions per active user<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", 
             text_auto=True,
             hover_data=['app', 'average_interactions_per_active_user', 'num_interactions', 'unique_authors'])

    fig.update_traces(marker_color=df_pending_rewards_grouped_app_top10.sort_values(by='average_interactions_per_active_user', ascending = False)[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Average interactions per active user', range = [0, 1.2* df_pending_rewards_grouped_app_top10['average_interactions_per_active_user'].max()])
    col1.write('Average interactions per active user')
    col1.plotly_chart(fig,use_container_width=True)


    fig = px.bar(df_pending_rewards_grouped_app_top10.sort_values(by='average_pending_rewards_per_active_user', ascending = False)[::-1], 
                x="average_pending_rewards_per_active_user", 
                y="app", 
                orientation='h', 
                height = 100 + 30* len(top10_apps),
                title=f"Top{TOP} apps on Hive, Average pending rewards per active user<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", 
                text_auto=True,
                hover_data=['app', 'average_pending_rewards_per_active_user', 'total_pending_rewards', 'unique_authors'])

    fig.update_traces(marker_color=df_pending_rewards_grouped_app_top10.sort_values(by='average_pending_rewards_per_active_user', ascending = False)[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Average pending rewards per active user', range = [0, 1.2* df_pending_rewards_grouped_app_top10['average_pending_rewards_per_active_user'].max()])
    col2.write('Average pending rewards per active user')
    col2.plotly_chart(fig,use_container_width=True)

    fig = px.bar(df_pending_rewards_grouped_app_top10.sort_values(by='average_pending_rewards_per_interaction', ascending = False)[::-1], 
                x="average_pending_rewards_per_interaction", 
                y="app", 
                orientation='h', 
                height = 100 + 30* len(top10_apps),
                title=f"Top{TOP} apps on Hive, Average pending rewards per interaction<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", 
                text_auto=True,
                hover_data=['app', 'average_pending_rewards_per_active_user', 'total_pending_rewards', 'num_interactions'])

    fig.update_traces(marker_color=df_pending_rewards_grouped_app_top10.sort_values(by='average_pending_rewards_per_interaction', ascending = False)[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Average pending rewards per interaction', range = [0, 1.2* df_pending_rewards_grouped_app_top10['average_pending_rewards_per_interaction'].max()])
    col3.write('Average pending rewards per interaction')
    col3.plotly_chart(fig,use_container_width=True)

    st.subheader('HIVE Top 10 Communities')

    col1, col2, col3 = st.columns(3)

    df_pending_rewards = df_pending_rewards.merge(df_communities, left_on = 'category', right_on = 'name', how='inner')
    df_pending_rewards_grouped_community = df_pending_rewards.groupby('title').agg(
        num_interactions=('title', 'size'),
        unique_authors=('author', 'nunique'),
        total_pending_rewards=('pending_payout_value', 'sum')
    ).reset_index()

    for stats in df_pending_rewards_grouped_community.columns[1:]:
        df_pending_rewards_grouped_community[f'rank {stats}'] = df_pending_rewards_grouped_community[stats].rank(method='min', ascending=False).astype(int)
    df_pending_rewards_grouped_community['percentage_total_pending_rewards'] = df_pending_rewards_grouped_community['total_pending_rewards']/df_pending_rewards_grouped_community['total_pending_rewards'].sum()    

    df_pending_rewards_grouped_community_sorted_by_num_interactions =  df_pending_rewards_grouped_community.sort_values(by = "num_interactions", ascending = False).head(TOP).reset_index(drop = True)
    if not 'Liketu' in df_pending_rewards_grouped_community_sorted_by_num_interactions['title'].to_list():
        df_pending_rewards_grouped_community_sorted_by_num_interactions = pd.concat([df_pending_rewards_grouped_community_sorted_by_num_interactions, df_pending_rewards_grouped_community.loc[df_pending_rewards_grouped_community['title'] == 'Liketu']])
        df_pending_rewards_grouped_community_sorted_by_num_interactions['title'] = df_pending_rewards_grouped_community_sorted_by_num_interactions['title'].replace("Liketu", f"Liketu (rank {df_pending_rewards_grouped_community[df_pending_rewards_grouped_community['title'] == 'Liketu']['rank num_interactions'].squeeze()})")
    df_pending_rewards_grouped_community_sorted_by_num_interactions['color'] = df_pending_rewards_grouped_community_sorted_by_num_interactions['title'].apply(lambda x: 'blue' if x.startswith('Liketu') else 'red')    

    fig = px.bar(df_pending_rewards_grouped_community_sorted_by_num_interactions[::-1], x="num_interactions", y="title", orientation='h', height = 100 + 30* TOP,
             title=f"Top{TOP} communities on Hive, by number of interactions<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_community_sorted_by_num_interactions[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Number of interactions', range = [0, 1.2 * df_pending_rewards_grouped_community_sorted_by_num_interactions["num_interactions"].max()])
    fig.update_yaxes(title_text='Community')
    col1.write('Top 10 HIVE Communities, by number of interactions')
    col1.plotly_chart(fig,use_container_width=True)

    df_pending_rewards_grouped_community_sorted_by_unique_authors =  df_pending_rewards_grouped_community.sort_values(by = "unique_authors", ascending = False).head(TOP).reset_index(drop = True)
    if not 'Liketu' in df_pending_rewards_grouped_community_sorted_by_unique_authors['title'].to_list():
        df_pending_rewards_grouped_community_sorted_by_unique_authors = pd.concat([df_pending_rewards_grouped_community_sorted_by_unique_authors, df_pending_rewards_grouped_community.loc[df_pending_rewards_grouped_community['title'] == 'Liketu']])
        df_pending_rewards_grouped_community_sorted_by_unique_authors['title'] = df_pending_rewards_grouped_community_sorted_by_unique_authors['title'].replace("Liketu", f"Liketu (rank {df_pending_rewards_grouped_community[df_pending_rewards_grouped_community['title'] == 'Liketu']['rank unique_authors'].squeeze()})")
    df_pending_rewards_grouped_community_sorted_by_unique_authors['color'] = df_pending_rewards_grouped_community_sorted_by_unique_authors['title'].apply(lambda x: 'blue' if x.startswith('Liketu') else 'red')    

    fig = px.bar(df_pending_rewards_grouped_community_sorted_by_unique_authors[::-1], x="unique_authors", y="title", orientation='h', height = 100 + 30* TOP,
             title=f"Top{TOP} communities on Hive, by number of users who post/comment<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_community_sorted_by_unique_authors[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Number of users who post/comment', range = [0, 1.2*df_pending_rewards_grouped_community_sorted_by_unique_authors['unique_authors'].max()])
    col2.write('Top 10 HIVE Communities, by number of users who posted and commented')
    col2.plotly_chart(fig,use_container_width=True)

    df_pending_rewards_grouped_community_sorted_by_total_pending_rewards =  df_pending_rewards_grouped_community.sort_values(by = "total_pending_rewards", ascending = False).head(TOP).reset_index(drop = True)
    if not 'Liketu' in df_pending_rewards_grouped_community_sorted_by_total_pending_rewards['title'].to_list():
        df_pending_rewards_grouped_community_sorted_by_total_pending_rewards = pd.concat([df_pending_rewards_grouped_community_sorted_by_total_pending_rewards, df_pending_rewards_grouped_community.loc[df_pending_rewards_grouped_community['title'] == 'Liketu']])
        df_pending_rewards_grouped_community_sorted_by_total_pending_rewards['title'] = df_pending_rewards_grouped_community_sorted_by_total_pending_rewards['title'].replace("Liketu", f"Liketu (rank {df_pending_rewards_grouped_community[df_pending_rewards_grouped_community['title'] == 'Liketu']['rank total_pending_rewards'].squeeze()})")
    df_pending_rewards_grouped_community_sorted_by_total_pending_rewards['color'] = df_pending_rewards_grouped_community_sorted_by_total_pending_rewards['title'].apply(lambda x: 'blue' if x.startswith('Liketu') else 'red')    

    fig = px.bar(df_pending_rewards_grouped_community_sorted_by_total_pending_rewards[::-1], x="total_pending_rewards", y="title", orientation='h', height = 100 + 30* TOP,
                title=f"Top{TOP} communities on Hive, by HIVE pending rewards<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_community_sorted_by_total_pending_rewards[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Pending HIVE rewards', range = [0, 1.2*df_pending_rewards_grouped_community_sorted_by_total_pending_rewards['total_pending_rewards'].max()])
    col3.write('Top 10 HIVE Communities, by HIVE pending rewards')
    col3.plotly_chart(fig,use_container_width=True)

    col1, col2, col3 = st.columns(3)

    fig = px.bar(df_pending_rewards_grouped_community_sorted_by_total_pending_rewards[::-1], x="percentage_total_pending_rewards", y="title", orientation='h', height = 100 + 30* TOP,
             title=f"Top{TOP} communities on Hive, by HIVE pending rewards<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", text_auto=True)

    fig.update_traces(marker_color=df_pending_rewards_grouped_community_sorted_by_total_pending_rewards[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Pending HIVE rewards (in percentage)', tickformat = '.2%', range = [0, 1.2*df_pending_rewards_grouped_community_sorted_by_total_pending_rewards['percentage_total_pending_rewards'].max()])
    col1.write('Top 10 HIVE Communities, by pending rewards (in percentage)')
    col1.plotly_chart(fig,use_container_width=True)

    col1, col2, col3 = st.columns(3)

    top10_communities = ['Liketu']
    for stats in ['num_interactions', 'unique_authors', 'total_pending_rewards']:
        top10_communities += df_pending_rewards_grouped_community.sort_values(by = stats, ascending = False).head(TOP)['title'].to_list()
    top10_communities = list(set(top10_communities))
    df_pending_rewards_grouped_community_top10 = df_pending_rewards_grouped_community[df_pending_rewards_grouped_community['title'].isin(top10_communities)]
    df_pending_rewards_grouped_community_top10['color'] = list(np.where(df_pending_rewards_grouped_community_top10['title'] == 'Liketu', 'blue', 'red'))

    df_pending_rewards_grouped_community_top10['average_pending_rewards_per_active_user'] = df_pending_rewards_grouped_community_top10['total_pending_rewards']/df_pending_rewards_grouped_community_top10['unique_authors']
    df_pending_rewards_grouped_community_top10['average_pending_rewards_per_interaction'] = df_pending_rewards_grouped_community_top10['total_pending_rewards'] / df_pending_rewards_grouped_community_top10['num_interactions']
    df_pending_rewards_grouped_community_top10['average_interactions_per_active_user'] = df_pending_rewards_grouped_community_top10['num_interactions'] / df_pending_rewards_grouped_community_top10['unique_authors']
    df_pending_rewards_grouped_community_top10['color'] = list(np.where(df_pending_rewards_grouped_community_top10['title'] == 'Liketu', 'blue', 'red'))

    fig = px.bar(df_pending_rewards_grouped_community_top10.sort_values(by='average_interactions_per_active_user', ascending = False)[::-1], 
                x="average_interactions_per_active_user", 
                y="title", 
                orientation='h', 
                height = 100 + 30* len(top10_communities),
                title=f"Top{TOP} communities on Hive, Average interactions per active user<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", 
                text_auto=True,
                hover_data=['title', 'average_interactions_per_active_user', 'num_interactions', 'unique_authors'])

    fig.update_traces(marker_color=df_pending_rewards_grouped_community_top10.sort_values(by='average_interactions_per_active_user', ascending = False)[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Average interactions per active user', range = [0, 1.2*df_pending_rewards_grouped_community_top10['average_interactions_per_active_user'].max()])
    col1.write('Average interactions per active user,\n comparison with Top 10 HIVE communities')    
    col1.plotly_chart(fig,use_container_width=True)

    fig = px.bar(df_pending_rewards_grouped_community_top10.sort_values(by='average_pending_rewards_per_active_user', ascending = False)[::-1], 
             x="average_pending_rewards_per_active_user", 
             y="title", 
             orientation='h', 
             height = 100 + 30* len(top10_communities),
             title=f"Top{TOP} communities on Hive, Average pending rewards per active user<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", 
             text_auto=True,
             hover_data=['title', 'average_pending_rewards_per_active_user', 'total_pending_rewards', 'unique_authors'])

    fig.update_traces(marker_color=df_pending_rewards_grouped_community_top10.sort_values(by='average_pending_rewards_per_active_user', ascending = False)[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Average pending rewards per active user', range = [0, df_pending_rewards_grouped_community_top10['average_pending_rewards_per_active_user'].max()])
    col2.write('Average pending rewards per active user,\n comparison with Top 10 HIVE communities')            
    col2.plotly_chart(fig,use_container_width=True)

    fig = px.bar(df_pending_rewards_grouped_community_top10.sort_values(by='average_pending_rewards_per_interaction', ascending = False)[::-1], 
             x="average_pending_rewards_per_interaction", 
             y="title", 
             orientation='h', 
             height = 100 + 30* len(top10_communities),
             title=f"Top{TOP} communities on Hive, Average pending rewards per interaction<br>Past 7 days<br>Snapshot: {df_pending_rewards['created'].max()} (UTC)", 
             text_auto=True,
             hover_data=['title', 'average_pending_rewards_per_active_user', 'total_pending_rewards', 'num_interactions'])

    fig.update_traces(marker_color=df_pending_rewards_grouped_community_top10.sort_values(by='average_pending_rewards_per_interaction', ascending = False)[::-1]['color'].to_list(),
                    textposition='outside')
    fig.update_xaxes(title_text='Average pending rewards per interaction', range = [0, df_pending_rewards_grouped_community_top10['average_pending_rewards_per_interaction'].max() ])
    col3.write('Average pending rewards per interaction,\n comparison with Top 10 HIVE communities')
    col3.plotly_chart(fig,use_container_width=True)




