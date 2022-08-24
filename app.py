import pandas as pd
import plotly.express as px
import streamlit as st
from functools import reduce
import datetime
from datetime import timedelta

# Load the data
calls = pd.read_csv("call_ammounts.csv")
calls['date'] = pd.to_datetime(calls['date'], format = '%d.%m.%Y')
calls['weekly_moving_avg'] = calls['approved_of_answered'].shift(1).rolling(7).mean()

st.set_page_config(page_title='Calls dashboard', page_icon=':bar_chart:')

# Input date widget
with st.sidebar:
    d = st.date_input(
         "Enter the date",
        datetime.date(2022, 5, 6))

previous_d = d - timedelta(days=1)

st.write("""
## Wellcome to your call center performance dashboard!!!
""")

st.write("""
### KPI: 
""")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Number of calls", int(calls.query("date == @d")['n_calls']), delta = int(calls.query("date == @previous_d")['n_calls']))
col2.metric("Answered calls", int(calls.query("date == @d")['n_answered']), delta = int(calls.query("date == @previous_d")['n_answered']))
col3.metric("Number of leads", int(calls.query("date == @d")['leads']), delta = int(calls.query("date == @previous_d")['leads']))
col4.metric("Leads approved", int(calls.query("date == @d")['approved']), delta = int(calls.query("date == @previous_d")['approved']))


st.write("""
#### **Grpahs:**
""")

# Moving average linechart

fig = px.line(calls, x = 'date', y = 'weekly_moving_avg',
              width=700, height=400,
              title = 'Weekly moving average conversion of approved out of answered',
              labels = dict(weekly_moving_avg = 'Moving average', date = 'Dates'))
fig.show()
st.plotly_chart(fig)

# Funnel
chosen_date = '2021-08-12'
array = calls.query("date == @chosen_date")[['n_calls', 'n_answered', 'leads', 'approved']].values.tolist()
funnel_values = reduce(lambda r,x:r+x, array,[])
funnel_data = dict(values = funnel_values,
                labels = ['Calls made', 'Calls answered', 'Leads', 'Approved by operator'])
fig2 = px.funnel(funnel_data, y = 'labels', x = 'values',
                 width=700, height=400,
                 title = 'Calls conversion funnel')
fig2.show()
st.plotly_chart(fig2)



