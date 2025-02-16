import streamlit as st
st.set_page_config(page_title="Hive Onboarders Dashboard", layout="wide")
import pandas as pd
import datetime
from datetime import timedelta
from datetime import date
from all_hive_onboarders import generate_all_hive_onboarders
from MAU import get_hive_onboarder_MAU
#import pyodbc
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mtick
# from matplotlib.ticker import FuncFormatter
# from hive_top10_stats_v2 import hive_top10_stats_ratios
# from hive_top15_apps_historical_data_users import hive_top15_apps_historical_data_users
# #from hive_top15_apps_historical_data_users_onboarded_by_liketu import hive_top15_apps_historical_data_users_onboarded_by
# from liketu_engagement_league import generate_liketu_engagement_league_table_app, generate_liketu_engagement_league_table_community
# from hive_liketu_weekly_stats import generate_weekly_hive_liketu_stats
# from liketu_daily_stats_v2 import generate_daily_liketu_stats, generate_daily_liketu_moments_stats
# #from liketu_daily_stats import generate_daily_liketu_stats_app, generate_daily_liketu_stats_community
# from liketu_categories_stats import generate_top10_liketu_categories_stats, generate_top10_liketu_categories_stats_past_hours
# from wordclouds import generate_posts_wordcloud, generate_posts_wordcloud_past_hours
# from follower_graph import generate_follower_graph_stats
# from voting_graph import generate_voting_graph
# from hive_brain_energy_value import generate_hive_brain_energy_value
# from hive_trending_ranking import hive_trending_ranking
# from liketu_trending_ranking import liketu_trending_ranking
# from liketu_voting_stats import generate_liketu_voting
# from liketu_user_retention import generate_liketu_user_retention
# from liketu_author_vests_stakes import generate_liketu_author_vests_stakes
# from liketu_cost_projection import generate_liketu_cost_projection
# from geolocation_stats import generate_geolocation_liketu_stats_app, generate_geolocation_hive_stats
# from farcaster_dashboard import get_farcaster_network_dashboard
# from hive_curator import get_hive_curator_stats
# from liketu_onboarded_users import generate_onboarded_users_stats
# #from leo_onboarded_users import generate_onboarded_users_stats_leo
# from challenge_21_days import generate_challenge_21_days, get_list_of_runners_21_days
# from challenge_21_days_summary import generate_challenge_21_days_summary

# CONST_REWARDS_PERIOD = 7
 

st.title('Hive onboarders Dashboard')

st.sidebar.title("Options")

option = st.sidebar.selectbox(
     'Which dashboard?',
     ('All HIVE onboarders', 'MAU'))
st.header(option)
#st.sidebar.write('You selected:', option)

if option == 'All HIVE onboarders':
    with st.form("all_hive_onboarders"):
        with st.sidebar:

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                pass   
            
    if submitted:
        generate_all_hive_onboarders()

elif option == 'MAU':    
   
    with st.form("hive_curator"):

        with st.sidebar:

            onboarder = st.text_input(label='Enter HIVE onboarder')
            submitted = st.form_submit_button("Submit")

            if submitted:
                pass

    if submitted:
        get_hive_onboarder_MAU(onboarder)
        


# if option == 'Liketu daily/weekly/monthly stats':
#     if 'dashboard' in st.session_state.keys():
#         del st.session_state['dashboard']    
#     with st.form("liketu_daily_stats"):
#         with st.sidebar:
#             option_stats_liketu_daily_stats = st.selectbox(
#                 'Liketu daily stats based on:',
#                 ('Liketu App', 'Liketu Community', 'Liketu Moments'))     

#             option_set_of_users = st.selectbox(
#                 'Set of users:',
#                 ('Hive global', 'Onboarded by liketu', 'Onboarded by leo.voter'))                    

#             option_start_date= st.date_input(
#             "Choose start date", date(2021, 12, 19))

#             option_end_date= st.date_input(
#             "Choose end date", date.today() - timedelta(1)   )

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass            
    
#     if submitted:
#         st.subheader(option_stats_liketu_daily_stats)    
#         if option_stats_liketu_daily_stats in ['Liketu App', 'Liketu Community']:
#             generate_daily_liketu_stats(option_start_date, option_end_date, option_stats_liketu_daily_stats, option_set_of_users)            
#         elif option_stats_liketu_daily_stats == 'Liketu Moments':
#             generate_daily_liketu_moments_stats(option_start_date, option_end_date, option_set_of_users)            

            
# elif option == 'Liketu categories stats':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']         
#     with st.sidebar:
#         option_stats_app_community = st.selectbox(
#                 'Liketu categories based on:',
#                 ('Liketu App', 'Liketu Community'))        

#         option_dates_past_hours = st.radio(
#             "Input start/end dates or past X hours",
#             ('Start/End date', 'Past X hours')
#         )
#         with st.form("liketu_categories_stats"):
#             if option_dates_past_hours == 'Start/End date':
#                 option_start_date= st.date_input(
#                 "Choose start date", datetime.datetime(2021, 12, 19))

#                 option_end_date= st.date_input(
#                 "Choose end date", date.today() - timedelta(1)   )
                
#                 # Every form must have a submit button.
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     pass
#             elif option_dates_past_hours == 'Past X hours':
#                 option_hours= st.number_input(
#                 "Choose number of hours",value = 24)
                
#                 # Every form must have a submit button.
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     pass                    

#     if submitted:
#         st.subheader(option_stats_app_community)
#         if option_dates_past_hours == 'Start/End date':
#             st.write('Start date:', option_start_date)
#             st.write('End date:', option_end_date)
#             generate_top10_liketu_categories_stats(option_start_date, option_end_date, option_stats_app_community)
#         else:
#             st.write('Past', option_hours, "hours")
#             generate_top10_liketu_categories_stats_past_hours(option_hours, option_stats_app_community)

# elif option == 'Wordcloud':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.sidebar:
#         option_stats_app_community = st.selectbox(
#                 'Liketu wordcloud based on posts in:',
#                 ('Liketu App', 'Liketu Community'))        

#         option_dates_past_hours = st.radio(
#             "Input start/end dates or past X hours",
#             ('Start/End date', 'Past X hours')
#         )
#         with st.form("liketu_wordcloud"):
#             if option_dates_past_hours == 'Start/End date':
#                 option_start_date= st.date_input(
#                 "Choose start date", datetime.datetime(2021, 12, 19))

#                 option_end_date= st.date_input(
#                 "Choose end date", date.today() - timedelta(1)   )
                
#                 # Every form must have a submit button.
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     pass
#             elif option_dates_past_hours == 'Past X hours':
#                 option_hours= st.number_input(
#                 "Choose number of hours",value = 24)
                
#                 # Every form must have a submit button.
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     pass                    

#     if submitted:
#         st.subheader(option_stats_app_community)
#         if option_dates_past_hours == 'Start/End date':
#             st.write('Start date:', option_start_date)
#             st.write('End date:', option_end_date)
#             generate_posts_wordcloud(option_start_date, option_end_date, option_stats_app_community)
#         else:
#             st.write('Past', option_hours, "hours")
#             generate_posts_wordcloud_past_hours(option_hours, option_stats_app_community)




# elif option == 'HIVE Top apps stats':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        

#     with st.sidebar:    
#         option_stats_liketu_daily_stats = st.selectbox(
#             'Hive top app stats based:',
#             ('Hive Top 10 apps (including ratios)', 'Hive Top 15 apps historical data', 'Hive Top 15 apps historical data - users onboarded by liketu'))                    
#         with st.form("hive_top10stats_form"):
#             if option_stats_liketu_daily_stats.startswith('Hive Top 15 apps historical data'):
#                 option_start_date= st.date_input(
#             "Choose start date", date(2021, 12, 19))
#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         if option_stats_liketu_daily_stats == 'Hive Top 10 apps (including ratios)':
#             hive_top10_stats_ratios(CONST_REWARDS_PERIOD)
#         elif option_stats_liketu_daily_stats == 'Hive Top 15 apps historical data':
#             hive_top15_apps_historical_data_users(option_start_date)
#         # elif option_stats_liketu_daily_stats == 'Hive Top 15 apps historical data - users onboarded by liketu':
#         #     hive_top15_apps_historical_data_users_onboarded_by(option_start_date, 'liketu')            
# #        st.subheader(option_stats)    

# #        if option_stats == 'HIVE Top 10 Apps':
# #            hive_top10_stats_ratios_apps(CONST_REWARDS_PERIOD)            

# #        elif option_stats == 'HIVE Top 10 Communities':      
# #            hive_top10_stats_ratios_communities(CONST_REWARDS_PERIOD)


# elif option == 'Liketu Engagement League':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']    
#     with st.form("liketu_engagement_league_form"):
#         with st.sidebar:
#             option_stats_2 = st.selectbox(
#                 'Liketu Engagement League based on:',
#                 ('Liketu App', 'Liketu Community'))        

#             option_end_date = st.date_input(
#             "Choose end date", date.today() - timedelta(1)   )

#             engagement_days = st.number_input("Number of days:", value= 7)
#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass
    
#     if submitted:
#         year = option_end_date.year 
#         month = option_end_date.month 
#         day = option_end_date.day

#         st.subheader(option_stats_2)

#         st.write("Start date:", option_end_date - timedelta(engagement_days-1))
#         st.write("End date:", option_end_date)
#         st.write("Number of days:", engagement_days)

#         if option_stats_2 =='Liketu App':
        
#             generate_liketu_engagement_league_table_app(year, month,day,engagement_days)

#         elif option_stats_2 =='Liketu Community':
        
#             generate_liketu_engagement_league_table_community(year, month,day,engagement_days)        

# elif option == 'HIVE/Liketu Weekly Stats':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("hive_top10stats_form"):
#         with st.sidebar:

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         generate_weekly_hive_liketu_stats()

# elif option == 'Follower graph':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("liketu_follower_graph"):
#         with st.sidebar:
#             option_stats_app_community = st.selectbox(
#                     'Liketu follower graph based on:',
#                     ('Liketu App', 'Liketu Community', 'Liketu App & Community combined'))      

#             agree = st.checkbox('Add graph on dashboard (time consuming!)')
#             add_graph = False
#             if agree:
#                 add_graph=True

#             option_start_date= st.date_input(
#             "Choose start date", datetime.datetime(2021, 12, 19))

#             option_end_date= st.date_input(
#             "Choose end date", date.today()   )       

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass            

#     if submitted:
#         st.subheader(option_stats_app_community)
#         st.write("Follower graph based on users who made at least one post or comment from ", option_start_date, " to " , option_end_date)
#         generate_follower_graph_stats(option_start_date, option_end_date, option_stats_app_community,add_graph)                   

# elif option == 'Voting graph':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("liketu_voting_graph"):
#         with st.sidebar:
#             option_stats_app_community = st.selectbox(
#                     'Liketu voting graph based on:',
#                     ('Liketu App', 'Liketu Community', 'Liketu App & Community combined'))      

#             option_start_date= st.date_input(
#             "Choose start date", datetime.datetime(2021, 12, 19))

#             option_end_date= st.date_input(
#             "Choose end date", date.today()   )       

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass            

#     if submitted:
#         st.subheader(option_stats_app_community)
#         st.write("Voting graph based on upvotes on Liketu content from ", option_start_date, " to " , option_end_date)
#         generate_voting_graph(option_start_date, option_end_date, option_stats_app_community, CONST_REWARDS_PERIOD)                   


# elif option == 'HIVE Brain Energy Value':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("hive_brain_energy_form"):
#         with st.sidebar:
#             #option_stats = st.selectbox(
#             #    'Which stats?',
#             #    ('HIVE Top 10 Apps', 'HIVE Top 10 Communities'))        

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         generate_hive_brain_energy_value()

# elif option == 'Trending Ranking':    
#     if 'dashboard' in st.session_state.keys():
#         if st.session_state['dashboard']!='Liketu Trending' :
#             del st.session_state['dashboard']        
#     with st.form("trending_ranking_form"):

#         with st.sidebar:
#             option_trending_ranking = st.selectbox(
#                 'Trending Ranking for:',
#                 ('Liketu', 'Hive'))        

#             if option_trending_ranking == 'Liketu':
#                 user = st.text_input(label='Enter user')
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 pass
#             elif 'dashboard' in st.session_state.keys():
#                 if st.session_state['dashboard'] == 'Liketu Trending':
#                     pass


#     if submitted:

#         st.subheader(option_trending_ranking, " Trending")    
#         if option_trending_ranking == 'Liketu':
#             liketu_trending_ranking(user)

#         if option_trending_ranking == 'Hive':
#             if 'dashboard' in st.session_state.keys():            
#                 del st.session_state['dashboard']                
#             hive_trending_ranking()

#     elif 'dashboard' in st.session_state.keys():
#         if st.session_state['dashboard']=='Liketu Trending' :
#             liketu_trending_ranking(user)

# elif option == 'Liketu voting stats':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("liketu_voting_stats_form"):
#         with st.sidebar:

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         generate_liketu_voting(datetime.datetime(2021, 12, 19))

# elif option == 'Liketu user retention':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("liketu_user_retention_form"):
#         with st.sidebar:

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         generate_liketu_user_retention(datetime.datetime(2021, 12, 19))        

# elif option == 'Liketu Author Vests Stakes':    
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("liketu_vests_stakes_form"):
#         with st.sidebar:

#             author = st.text_input(label='Enter author')
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 pass

#     if submitted:
#         generate_liketu_author_vests_stakes(author)        

# if option == 'Geolocation stats':
#     if 'dashboard' in st.session_state.keys():
#         del st.session_state['dashboard']    
#     with st.form("geolocation"):
#         with st.sidebar:
#             option_stats_geolocation = st.selectbox(
#                 'Geolocation stats for:',
#                 ('Liketu App', 'Hive and Liketu App'))        

#             option_start_date= st.date_input(
#             "Choose start date", datetime.datetime(2021, 12, 19))

#             option_end_date= st.date_input(
#             "Choose end date", date.today() - timedelta(1)   )

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass            
    
#     if submitted:
#         st.subheader(option_stats_geolocation)    

#         if option_stats_geolocation == 'Liketu App':
#             generate_geolocation_liketu_stats_app(option_start_date, option_end_date)            

#         elif option_stats_geolocation == 'Hive and Liketu App':      
#             generate_geolocation_hive_stats(option_start_date, option_end_date)

# elif option == 'Liketu Cost Projection':    
#     #if 'dashboard' in st.session_state.keys():    
#         #del st.session_state['dashboard']        
#     with st.form("liketu_cost_projection_form"):
#         with st.sidebar:
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 pass
#             elif 'dashboard' in st.session_state.keys():
#                 if st.session_state['dashboard'] == 'Liketu Cost Projection':
#                     pass
                    

#     if submitted:
#         generate_liketu_cost_projection()
#     elif 'dashboard' in st.session_state.keys():
#         if st.session_state['dashboard'] == 'Liketu Cost Projection':
#             generate_liketu_cost_projection()

# elif option == 'Farcaster Network Dashboard':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("farcaster"):
#         with st.sidebar:

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         get_farcaster_network_dashboard(date(2021, 12, 19))                            

# elif option == 'HIVE curator':    
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("hive_curator"):

#         with st.sidebar:

#             voter = st.text_input(label='Enter voter')
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 pass

#     if submitted:
#         get_hive_curator_stats(voter, date(2021, 12, 19))

# elif option == 'Onboarded Users by leo.voter':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("onboarded_leo"):
#         with st.sidebar:

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         generate_onboarded_users_stats('leo.voter')


# elif option == 'Onboarded Users by liketu':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("onboarded_liketu"):
#         with st.sidebar:

#             # Every form must have a submit button.
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 pass

#     if submitted:
#         generate_onboarded_users_stats('liketu')


# elif option == '21 Day Challenge - Individual Runner':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("21_day"):

#         with st.sidebar:

#             list_of_runners_21_days = get_list_of_runners_21_days()
#             runner = st.selectbox(
#                 'Stats for runner:',
#                 list_of_runners_21_days)        
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 pass        


#     if submitted:
#         generate_challenge_21_days(runner)


# elif option == '21 Day Challenge - Summary':
#     if 'dashboard' in st.session_state.keys():    
#         del st.session_state['dashboard']        
#     with st.form("21_day_summary"):

#         with st.sidebar:

#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 pass        

#     if submitted:
#         generate_challenge_21_days_summary()

