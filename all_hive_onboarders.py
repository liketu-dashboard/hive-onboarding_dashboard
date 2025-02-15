import streamlit as st
import pandas as pd
import datetime
import numpy as np
import pyodbc
import json
import plotly.express as px
import plotly.graph_objects as go
import pyodbc

def generate_all_hive_onboarders():
    connection = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=vip.hivesql.io;'
    'Database=DBHive;'
    f'uid={st.secrets["DB_USERNAME"]};pwd={st.secrets["DB_PASSWORD"]}'
    )

    # SQL query to group by 'creator' and count entries
    SQLCommand = """
    SELECT creator, COUNT(*) AS number_of_created_accounts
    FROM TxAccountCreates
    GROUP BY creator;
    """

    # Run the query and load the result into a DataFrame
    df = pd.read_sql(SQLCommand, connection).rename(columns = {"number_of_created_accounts": "Number of created accounts"}).sort_values(by="Number of created accounts", ascending=False).reset_index(drop=True)
    df.index=df.index+1

    # Set a title for your Streamlit app
    st.title("Hive onboarding accounts")

    # Display the DataFrame in the Streamlit app
    st.dataframe(df)