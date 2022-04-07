# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 09:30:28 2022

@author: Abdhul Khadhir
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openpyxl

#Title
st.title('AKespense Tracker')

link = 'https://api.onedrive.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL3gvcyFBdWZ6bnAweHVfSG5nZlpGaXg4OFZ5azdvMFlZcnc_ZT10WnBwRDA/root/content'


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')

data = pd.read_excel(link,'Transactions', engine='openpyxl')
data['Month'] = data['Date'].dt.strftime('%b-%Y')
data = data.fillna(0)
data = data.round(decimals =2)

data_load_state.text("Loading data -DONE!")

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
table = pd.pivot_table(data = data_filtered, index = ['Month'], columns = 'Category', values = 'Amount',
                       aggfunc=np.sum, margins = True, fill_value = 0)

table_new = table.reset_index()
table_new = table_new.iloc[:-1,]
table_new['Month'] = pd.to_datetime(table_new['Month'])

fig = px.bar(table_new, x= 'Month', y=list(table_new.columns))

st.plotly_chart(fig, use_container_width=True)

# Show Categorywise Expenses as a table
if show_table:
    st.subheader('Monthly Expenses Summary Table')
    cols = [table.columns[-1]] + [col for col in table if col != table.columns[-1]]
    table = table[cols]
    table = table.round(decimals =2)
    st.write(table)
