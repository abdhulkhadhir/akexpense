# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 09:30:28 2022

@author: Abdhul Khadhir
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('ggplot')

#Title
st.title('AKspense Tracker')

link = 'https://api.onedrive.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL3gvcyFBdWZ6bnAweHVfSG5nZlpGaXg4OFZ5azdvMFlZcnc_ZT10WnBwRDA/root/content'

# # Load Uber Data
# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data = pd.read_excel(link,'Transactions', engine='openpyxl')
data['Month'] = data['Date'].dt.strftime('%b-%Y')

data_load_state.text("Done! (using st.cache)")

# Print Raw data as a DataFrame

with st.sidebar:
    st.subheader('Filters')
    st.write("Do you want to display all transactions?")
    show_trans = st.checkbox('Show All Transactions')
    
    if show_trans:
        st.write("Enter the keywords that you want to search")
        text = st.text_input('Enter keywords')
        search = st.button('Search')
        
    st.write("Select the occasions you want to use for filtering the transactions")
    occasion = st.multiselect(
        'Select Occasion',
         ['All']+list(data['Occasion'].unique()),
         ['All'])
    st.write("Do you want to display a summary table of monthly expenses?")
    show_table = st.checkbox('Show Monthly Expenses Summary Table')
    
    
if show_trans:
    st.subheader('Raw data')
    if search:
        mask1 = data['Description'].str.contains(text, case=False, na=False)
        mask2 = data['Remarks'].str.contains(text, case=False, na=False)
        data_search = data[mask1 | mask2]
        st.write(data_search)
    
    else:
        st.write(data)
        
# Select Occasion


if 'All' in occasion:
    data_filtered = data
else:
    data_filtered = data[data['Occasion'].isin(occasion)]

# # Draw a Histogram
st.subheader('Monthly Expenses Summary Plot')

# Monthly Expenses - Summary plot
table = pd.pivot_table(data = data_filtered, index = ['Month'], columns = 'Category', aggfunc={'Amount':np.sum})
table_new = table['Amount'].reset_index()
table_new['Month'] = pd.to_datetime(table_new['Month'])


fig = px.bar(table_new, x= 'Month', y=list(table_new.columns))
#fig = px.bar(data_filtered, x='Month', y="Amount", color = 'Category')

st.plotly_chart(fig, use_container_width=True)

# Show Categorywise Expenses as a table
if show_table:
    st.subheader('Monthly Expenses Summary Table')
    st.write(table['Amount'])
        




