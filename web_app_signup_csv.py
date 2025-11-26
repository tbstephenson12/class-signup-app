#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 10:26:02 2025

@author: taylorstephenson

This is a web application that, when deployed, can be sent to class attendees
to record their responses for any number of class activities.
- potluck
- activity sign-up
- etc.
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='First Love Activity Sign-up',
)

st.image('first_love_logo.png', width='stretch')

def read_data_temp(filename):
    df = pd.read_csv(filename)
    print(f'Imported dataframe: {df.shape}')
    print('----columns:')
    for c in df.columns:
        print('    ' + c)
    temp_df = pd.DataFrame()
    for c in df.columns:
        if 'Unnamed' in c:
            continue
        else:
            temp_df[c] = df[c]
    
    df = temp_df
    
    return df

def add_data(data):
    previous_df = data[0]
    new_data_df = data[1]
    new_response_data = pd.concat([previous_df, new_data_df], ignore_index=True)
    return new_response_data

def save_data(filename):
    if 'signup-editor' in st.session_state:
        changes = st.session_state['signup-editor']
    
        if changes['edited_rows']:
            print(changes['edited_rows'])
            change_dict = changes['edited_rows']
            key = next(iter(change_dict.keys()))
            change_fields = list(change_dict[key].keys())
            df = st.session_state.data
            for field in change_fields:
                df.loc[key, field] = change_dict[key][field]
                
            st.session_state.data = df
    
    print(st.session_state.data)

# google sheet credentials and details
SPREADSHEET_NAME = 'Activity sign-up'
SHEET_NAME = 'Sheet1'
CREDENTIALS_FILE = './credentials.json'
SHEET_FILENAME = 'signups.csv'

# read in response csv only once upon startup
if 'data' not in st.session_state:
    st.session_state.data = read_data_temp(SHEET_FILENAME)

# grab column headers
cols = list(st.session_state.data.columns)

# give a title to the page
st.markdown('# First Love Activity Sign-up')

# side bar for data entry
with st.sidebar:
    st.header('Enter your information')
    
    # the sheet has the columns: Name(s), Number of people, What you're bringing
    with st.form(key='data_form'):
        name = st.text_input('Name(s)')
        number = st.number_input('Number of people', min_value=0)
        bringing = st.text_input('What are you bringing?')
        
        #submit button inside the side bar
        submitted = st.form_submit_button('Submit')
        
        # handle form submission
        if submitted:
            if name and number and bringing:
                new_data = [name, number, bringing]
                new_data_df = pd.DataFrame([new_data], columns=cols)
                st.session_state.data = add_data([st.session_state.data, new_data_df])
                st.success('Form submitted successfully')
            else:
                st.error('Please fill out the form completely before submitting')

# display data in the main window
st.markdown('## All responses')
bullets = '''
            **Note**: If you need to delete your entry:  
            - check the box next to that line  
            - click the trash icon
            '''
st.markdown(bullets)
editor_df = st.data_editor(
    st.session_state.data, 
    key='signup-editor', 
    on_change=save_data(SHEET_FILENAME), 
    num_rows='dynamic',
    width='stretch')
st.session_state.data = editor_df

st.session_state.data.to_csv(SHEET_FILENAME)