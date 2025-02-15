import streamlit as st
import pandas as pd
import numpy as np

# Title of the dashboard
st.title("My Basic Streamlit Dashboard")

# Header
st.header("Welcome to the Dashboard")

# Write a text
st.write("This is a simple dashboard built with Streamlit. You can display data, charts, and more!")

# Generate some sample data
data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=['A', 'B', 'C']
)

# Display the data as a table
st.subheader("Random Data Table")
st.write(data)

# Plot a line chart
st.subheader("Line Chart of the Data")
st.line_chart(data)

# Add a sidebar for user input
st.sidebar.header("User Input")
number = st.sidebar.slider("Select a number", 0, 100, 50)
st.sidebar.write("You selected:", number)

# Conditional display based on sidebar input
if number > 50:
    st.write("The selected number is greater than 50!")
else:
    st.write("The selected number is 50 or less.")
