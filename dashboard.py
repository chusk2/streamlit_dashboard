import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data(show_spinner=True)
def load_data(file):
    return pd.read_csv(file)

df = load_data('salaries_dataset.csv')

# ========== SIDEBAR: SELECCIONAR COLUMNAS ==========
st.sidebar.title("⚙️ Configurar Vista")

# Seleccionar qué columnas mostrar
available_columns = df.columns.tolist()
selected_columns = st.sidebar.multiselect(
    "📊 Select columns to show:",
    available_columns, default=available_columns  # Por defecto: todas
)

st.title('Job Salaries Dashboard')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    job_titles = ['All'] + sorted(list(df.job_title_short.dropna().unique()))
    job_title = st.selectbox('Job Title', options=job_titles)

with col2:
    countries = ['All'] + sorted(list(df.job_country.dropna().unique()))
    country = st.selectbox('Country', options= countries)

with col3:
    schedule_values = ['All'] + sorted(list(df.job_schedule_type.dropna().unique()))
    schedule = st.selectbox('Job Schedule', options = schedule_values )

if job_title:

    df_filtered = df

    if job_title != 'All':
        df_filtered = df_filtered[df_filtered.job_title_short == job_title]
    
    if country != 'All':
        df_filtered = df_filtered[df_filtered.job_country == country]

    if schedule != 'All':
        df_filtered = df_filtered[df_filtered.job_schedule_type == schedule]

    df_filtered = df_filtered.sort_values('job_posted_date').reset_index(drop=True)
    
    if df_filtered.shape[0] == 0:
        st.warning('No job offers meet the the selected criteria.')
    
    else:
        column_config = {
            'job_title' : st.column_config.TextColumn(
                label = 'Job Position'),
            'job_location' : st.column_config.TextColumn(
                label = 'Location'),
            'job_schedule_type' : st.column_config.TextColumn(
                label = 'Schedule'),
            'job_posted_date' : st.column_config.DatetimeColumn(
                label = 'Posted on',
                format = "YYYY/MM/DD"),
            'job_no_degree_mention' : st.column_config.CheckboxColumn(
                label = 'Degree required'),
            'job_health_insurance' : st.column_config.CheckboxColumn(
                label = 'Health insurance'),
            'job_country' : st.column_config.TextColumn(
                label = 'Job country'),
            'salary_rate' : st.column_config.TextColumn(
                label = 'Salary rate'),
            'salary_year_avg' : st.column_config.NumberColumn(
                label = 'Avg yearly salary'),
            'salary_hour_avg' : st.column_config.NumberColumn(
                label = 'Avg hourly salary'),
            'company_name' : st.column_config.TextColumn(
                label = 'Company'),
            'job_skills' : st.column_config.TextColumn(
                label = 'Skills required')
            }
        
        # show only selected columns
        selected_columns = list(column_config.keys())

        selected_cols_df = df_filtered[selected_columns]

        st.write(f'### *{selected_cols_df.shape[0]}* job positions found for current selection.')

        st.dataframe(selected_cols_df,
                     column_config=column_config,
                     #.format(precision=2) # 2 decimal places for floats
                     width="content",
                     hide_index=True
                    )

    # job positions for the filtered dataframe
    job_positions_count = (df_filtered.groupby(['job_country', 'country_code'])
                        .size()
                        .to_frame()
                        .rename(columns = {0 : 'count'})
                        .reset_index()                       
                        )

    # GRÁFICO COROPLÉTICO (grande)
    fig_mapa = px.choropleth(
        job_positions_count,
        locations="country_code",
        color="count",
        hover_name="job_country",
        hover_data={'country_code': False, 'count': True},
        color_continuous_scale="Plasma",
        title="Job positions count by country",
        labels={'count': 'Job Offers'}
    )

    fig_mapa.update_layout(
        height=600,
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)'
        )
    )

    st.plotly_chart(fig_mapa, use_container_width=True)
