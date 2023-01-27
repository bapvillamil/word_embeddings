import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objs as go
import plotly.express as px
import base64
from plotly.offline import iplot
from pandas.io.json import json_normalize
from PIL import Image
import matplotlib.pyplot as plt


fig = go.Figure()

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img1 = get_img_as_base64("web_bg.jpg")
img2 = Image.open('logo_new.png')

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64, {img1}");
    background-size: cover;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.image(img2)
st.write('')
st.write('')

st.set_option('deprecation.showfileUploaderEncoding', False)


option = st.selectbox(
    'Analysis Type:',
    ('Single Text Analysis', 'Multiple Text Analysis'))
st.markdown("")
st.markdown("")



if option == "Single Text Analysis":

    st.markdown("")

    single_review = st.text_input('Enter text below:')
    url = 'http://127.0.0.1:8000/classify/?text='+single_review
    r = requests.get(url)
    result = r.json()["text_sentiment"]


    if result == 'positive':
        x1, x2, x3, x4 = st.columns((2, 3, 3, 2))
        with x1:
            pass
        with x2:
            st.image("pos.png")
        with x3:
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("<h3 style='text-align: center; color: green'>The Text is POSITIVE! Nice</h3>", unsafe_allow_html=True)
        with x4:
            pass

    elif result == 'negative':
        x1, x2, x3, x4 = st.columns((2, 3, 3, 2))
        with x1:
            pass
        with x2:
            st.image("neg.png")
        with x3:
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("<h3 style='text-align: center; color: red'>The Text is NEGATIVE! Oh no</h3>", unsafe_allow_html=True)
        with x4:
            pass
        
    elif result == 'neutral' and single_review != "":
        x1, x2, x3, x4 = st.columns((2, 3, 3, 2))
        with x1:
            pass
        with x2:
            st.image("neut.png")
        with x3:
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("<h3 style='text-align: center; color: yellow'>The Text is NEUTRAL. Safe</h3>", unsafe_allow_html=True)
        with x4:
            pass




elif option == "Multiple Text Analysis":

    
    count_positive = 0
    count_negative = 0
    count_neutral = 0
    
    upload_file = st.file_uploader("Upload your input CSV file:", type=["csv"])
    st.markdown("")
    st.markdown("")


    if upload_file is not None:

        input_df = pd.read_csv(upload_file)
        
        for i in range(input_df.shape[0]):
            multiple_review = str(input_df.iloc[i,1])
            url = 'http://127.0.0.1:8000/classify/?text='+multiple_review
            r = requests.get(url)
            result = r.json()["text_sentiment"]
            if result == 'positive':
                count_positive += 1
            elif result == 'negative':
                count_negative += 1
            else:
                count_neutral += 1


        col1, col2 = st.columns((3,7))
        with col1:

            if count_positive > count_negative and count_positive > count_neutral:
                st.markdown("")
                st.markdown(f"<div style='text-align: center; font-size: 15px;'><b>Majority of the file contains POSITIVE Texts</b></div>", unsafe_allow_html=True)
                st.markdown("")
                st.markdown("")
                st.image('pos.png')
            elif count_negative > count_positive and count_negative > count_neutral:
                st.markdown("")
                st.markdown(f"<div style='text-align: center; font-size: 15px;'><b>Majority of the file contains NEGATIVE Texts</b></div>", unsafe_allow_html=True)
                st.markdown("")
                st.markdown("")
                st.image('neg.png')
            elif count_neutral > count_positive and count_neutral > count_negative:
                st.markdown("")
                st.markdown(f"<div style='text-align: center; font-size: 15px;'><b>Majority of the file contains NEUTRAL Texts</b></div>", unsafe_allow_html=True)
                st.markdown("")
                st.markdown("")
                st.image('neut.png')
            elif count_positive == count_negative and count_positive == count_neutral:
                st.markdown("")
                st.markdown(f"<div style='text-align: center; font-size: 15px;'><b>The file is BALANCED between POSTIVE, NEGATIVE, and NEUTRAL Texts</b></div>", unsafe_allow_html=True)


        with col2:
            st.markdown(f"<div style='text-align: center; font-size: 15px;'><b>Summary</b></div>", unsafe_allow_html=True)
            fig, ax = plt.subplots()

            plt.rcParams['text.color'] = 'white'
            plt.rcParams['axes.labelcolor'] = 'white'
            fig.set_facecolor('#262730')
            ax.set_facecolor('#262730')
            label = ['Positive', 'Neutral', 'Negative']
            count = [count_positive, count_neutral, count_negative]
            bar = ax.bar(label, count, label=label, color=["green", "yellow", "red"])
            ax.set_ylabel('Count')
            ax.bar_label(bar)
            st.pyplot(fig)


    st.markdown("")
    st.markdown("")
    st.markdown("Download CSV Template File")
    with open("sentiment_analysis_template.csv", "rb") as fp:
         btn = st.download_button(
            label = "CSV Template",
            data = fp,
            file_name = "sentiment_analysis_template.csv",
            mime = 'text/csv'
            )

sentiment_analysis = """ Sentiment analysis, also referred to as opinion mining, is an approach to natural language processing (NLP) that identifies the emotional tone behind a body of text. 
This is a popular way for organizations to determine and categorize opinions about a product, service, or idea. 
It involves the use of data mining, machine learning (ML) and artificial intelligence (AI) to mine text for sentiment and subjective information."""

goal = """The goal of this application is to analyze the input text provided by the user to whether the text is positive, negative or neutral in nature. """
devs = "<br><br><br><br><br><br><br><br>Developers: <br>De Guzman, John Adrian <br>Porgalinas, Clan <br>Roberto, Jason <br>Villamil, Bernard Allen"

st.sidebar.markdown("<h1 style='text-align: center'>About</p1>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p1 style='text-align: center'>{sentiment_analysis}</p1>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p1 style='text-align: center'>{goal}</p1>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p1 style='text-align: center'>{devs}</p1>", unsafe_allow_html=True)

