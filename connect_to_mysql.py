# streamlit_app.py

import pandas as pd
import numpy as np
import streamlit as st
import mysql.connector
import datetime
import streamlit.components.v1 as components

# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])
    # return mysql.connector.connect(user='root',
    #                                password='', 
    #                                host='127.0.0.1',
    #                                port='3306',
    #                                database='lalit')

conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from lalit_production;")

# Print results.
# for row in rows:
#     st.write(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")

st.header('Records of MySQL table: lalit_production')
df =pd.DataFrame(rows, columns=['id','date','description','kg','price','total'])
st.dataframe(df)

st.header('Test selectedbox')
option = st.selectbox(
    'Which number do you like best?',
     df['description'])
'You selected: ', option

st.header('Test Form xxx')
with st.form("form1"):
     st.write('Inide the form')
     slider_val = st.slider('form slider')
     checkbox_val = st.checkbox('form checkbox')
     submitted = st.form_submit_button("Submit")
     pDate = st.date_input("date of birth:",datetime.date(2019,7,6))
     if submitted:
          st.write("slider", slider_val,"checkboc",checkbox_val)

components.iframe("https://pirus-unggul.com",height=800,scrolling=True)



# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.sidebar.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.sidebar.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")