import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objs as go
import plotly.express as px
import base64
from plotly.offline import iplot
from pandas.io.json import json_normalize

fig = go.Figure()

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img1 = get_img_as_base64("bg.jpg")
img2 = get_img_as_base64("bg2.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64, {img1}");
    background-size: cover;
}}
    
[data-testid="stHeader"] {{
    background-color: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
   right: 2rem; 
   display: none;
}}

[data-testid="stSidebar"] {{
    background-image: url("data:image/png;base64, {img2}");
    background-size: cover;
}}

.sidebar .sidebar-content {{
    width: 100px;
}}
</style>
"""


st.markdown(page_bg_img, unsafe_allow_html=True)

st.write("""
         # Sentiment Analysis
         """)

st.write('This application predicts if a text or a file that contains numerous texts are Positve, Negative, or Neutral in nature')
st.set_option('deprecation.showfileUploaderEncoding', False)
st.sidebar.header('User Input')
st.sidebar.subheader('Single Text Analysis')
single_review = st.sidebar.text_input('Enter text below:')
st.sidebar.header('')
st.sidebar.subheader('Multiple Text Analysis')
upload_file = st.sidebar.file_uploader("Upload your input CSV file:", type=["csv"])
count_positive = 0
count_negative = 0
count_neutral = 0

if upload_file is not None:
    input_df = pd.read_csv(upload_file)
    for i in range(input_df.shape[0]):
        url = 'http://127.0.0.1:8000/classify/?text='+str(input_df.iloc[i])
        r = requests.get(url)
        result = r.json()["text_sentiment"]
        if result == "positive":
            count_positive += 1
        elif result == "negative":
            count_negative += 1
        else:
            count_neutral += 1
            
    x = ["Positive", "Negative", "Neutral"]
    y = [count_positive, count_negative, count_neutral]
    
    if count_positive > count_negative:
        st.write("""# Majority of the file contains POSITIVE Texts """)
        st.image('positive.png')
    elif count_negative > count_positive:
        st.write(""" # Majority of the file contains NEGATIVE Texts """)
        st.image('negative.png')
    elif count_positive == count_negative:
        st.write("""# The file contains EQUAL number of POSITIVE and NEGATIVE Texts""")
    else:
        st.write("""# The file is BALANCED between POSTIVE, NEGATIVE, and NEUTRAL Texts """)
        
    layout = go.Layout(
        title = 'Multiple Text Analysis',
        xaxis = dict(title = 'Sentiment'),
        yaxis = dict(title = 'Number of reviews'),
    )
    
    fig.update_layout(dict1=layout, overwrite=True)
    fig.add_trace(go.Bar(name = 'Multiple Reviews', x=x, y=y))
    st.plotly_chart(fig, use_container_width=True)

elif single_review:
    url = 'http://127.0.0.1:8000/classify/?text='+single_review
    r = requests.get(url)
    result = r.json()["text_sentiment"]
    if result == "positive":
        st.write("""# The Text is POSITIVE! Nice """)
        st.image('positive.png')
    elif result == "negative":
        st.write("""# The Text is NEGATIVE! Oh no """)
        st.image('negative.png')
    else:
        st.write("""# The Text is NEUTRAL. Safe """)
        st.image('neutral.png')

else:
    st.write('')
    st.write('')
    st.markdown('Enter user input from the sidebar to see if it is POSITIVE, NEGATIVE, or NEUTRAL', unsafe_allow_html=True)

st.sidebar.header("Download CSV Template File")
with open("sentiment_analysis_template.csv", "rb") as fp:
    btn = st.sidebar.download_button(
        label = "CSV Template",
        data = fp,
        file_name = "sentiment_analysis_template.csv",
        mime = 'text/csv'
    )

st.sidebar.header('')
st.sidebar.subheader("""Created by Revalida Group 5""")
st.sidebar.subheader("""All rights reserved 2023""")