import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import gzip
import os
import math
import json
import plost

#Giao dien navigator
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('Dashboard/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Dashboard `GAME RECOMMENDATION`')

st.sidebar.subheader('Heat map parameter')
choose_chart = st.sidebar.selectbox('Chọn loại chart', ('Pie', 'Scatter plot phân bố đánh giá','Scatter plot phân bố đánh giá')) 


st.sidebar.markdown('''
---
# IS334.N22.TMCL
### Giảng viên: Đỗ Duy Thanh
### Họ và Tên sinh viên:
#### Thiều Vĩnh Tiến
#### Vũ Đình Tuấn Kiệt
#### Nguyễn Minh Hà
 



''')

#Load dataframe
def parse(path):
      g = gzip.open(path, 'rb')
      for l in g:
        yield json.loads(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df = getDF('E:/Nam 2/THƯƠNG MẠI ĐIỆN TỬ/Final(Mô Phật)/Video_Games_5.json.gz')



# Row A
a1, a2 = st.columns((5,5))
with a1:
    st.markdown('### Bảng phân bố đánh giá')
    ratings = []
    for review in parse('E:/Nam 2/THƯƠNG MẠI ĐIỆN TỬ/Final(Mô Phật)/Video_Games_5.json.gz'):
        ratings.append(review['overall'])     
    counts = {}
    for item in ratings:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

# Đếm số lần xuất hiện của từng phần tử
    for item in ratings:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    with sns.axes_style('white'):
    # Create count plot
        plt.bar(counts.keys(), counts.values())
    plt.xlabel('Rating')
    plt.ylabel('Total number of ratings')
    plt.title('Bảng phân bố đánh giá')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

# Row A.5
with a2:
    st.markdown('### Bảng xếp hạng đánh giá của người dùng')
    popular_products = pd.DataFrame(df.groupby('reviewerName')['reviewText'].count())
    most_popular = popular_products.sort_values('reviewText', ascending=False)
    most_popular = most_popular.tail(-2)
    #most_popular = most_popular.drop(most_popular[most_popular['reviewText'] <2 ].index)
    most_popular.head(30).plot(kind = "bar")
    #Biểu đồ xem sản phẩm có nhiều reviewText nhất
    st.pyplot()

# Row B


c1, c2 = st.columns((5,5))
with c1:
    st.markdown('### Scatter plot phân bố đánh giá')
    ratings_mean_count = pd.DataFrame(df.groupby('asin')['overall'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(df.groupby('asin')['overall'].count())
    plt.figure(figsize=(8,6))
    plt.rcParams['patch.force_edgecolor'] = True