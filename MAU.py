import streamlit as st
import pandas as pd
import datetime
import numpy as np
import pyodbc
import json
import plotly.express as px
import plotly.graph_objects as go
import pyodbc


def get_hive_onboarder_MAU(onboarder):

    # Establish the connection
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                'Server=vip.hivesql.io;'
                                'Database=DBHive;'
                                f'uid={st.secrets["DB_USERNAME"]};pwd={st.secrets["DB_PASSWORD"]}'
    )


    # Define the SQL command
    SQLCommand = f"""
    SELECT
        FORMAT(c.created, 'yyyy-MM') AS Month,
        COUNT(DISTINCT c.author) AS MAU
    FROM
        Comments c
    INNER JOIN
        TxAccountCreates t
        ON c.author = t.new_account_name
    WHERE
        t.creator = '{onboarder}' 
    GROUP BY
        FORMAT(c.created, 'yyyy-MM')
    ORDER BY
        Month ASC;
    """

    # Fetch the data
    df_result_MAU= pd.read_sql(SQLCommand, connection)

    # Close the connection
    connection.close()


    # Create a bar chart using plotly.express
    fig = px.bar(
        df_result_MAU,
        x='Month',
        y='MAU',
        title=f'MAU, Hive Global, created by {onboarder}',
        labels={'Month': 'Calendar Month', 'MAU': 'MAU'},
        #hover_data={'Month': False},  # Hides the YearMonth in hover since it's already on the x-axis
        text='MAU',  # Adds the count as text on top of each bar
    )

    # Customize the layout for better aesthetics
    fig.update_layout(
        xaxis=dict(tickangle=0),
        yaxis=dict(title='MAU, Hive Global'),
        hovermode='x',
        template='plotly_white'
    )

    # Optionally, adjust the text position
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig,use_container_width=True)    


