import streamlit as st
import pandas as pd

df = pd.read_csv('salaries_dataset.csv')

st.title('Job Salaries Dashboard')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    job_titles = sorted(list(df.job_title_short.dropna().unique()))
    job_title = st.selectbox('Job Title', options=job_titles)

with col2:
    countries = sorted(list(df.job_country.dropna().unique()))
    country = st.selectbox('Country', options= countries)

with col3:
    schedule_values = sorted(list(df.job_schedule_type.dropna().unique()))
    schedule = st.selectbox('Job Schedule', options = schedule_values )

if job_title:
    mask = (df.job_title_short == job_title) & (df.job_country == country) & (df.job_schedule_type == schedule)  
    df_filtered = df[mask].sort_values('job_posted_date').reset_index(drop=True)
    if df_filtered.shape[0] == 0:
        st.warning('No job offers meet the the selected criteria.')
    else:
        st.dataframe(df_filtered,
                #.format(precision=2) # 2 decimal places for floats
                width="content",
                hide_index=True
                )