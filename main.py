import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

url = "https://raw.githubusercontent.com/BraydenHumpherys/Snowfall-Prediction/refs/heads/main/SnowFall23_25.csv"
df = pd.read_csv(url)

#get month and year from time column
df['time'] = pd.to_datetime(df['time'])
df['month'] = df['time'].dt.month
df['year'] = df['time'].dt.year


st.title('Cracking the Snow Code')

tab1, tab2, tab3 = st.tabs(['Snowfall By Month', 'Time Series', 'Heat Map'])


# User Selects year, and a graph of the the snowfall by month is shown.
with tab1: 
    selected_year = st.selectbox('Select Year', options=df['year'].unique())
    monthly_snowfall = df[df['year'] == selected_year].groupby('month')['snowfall_sum'].sum()

    fig, ax = plt.subplots()
    sns.barplot(x=monthly_snowfall.index, y=monthly_snowfall.values, ax=ax)
    ax.set_title(f'Snowfall By Month for {selected_year}')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Snowfall')
    st.pyplot(fig)


 # User selects variables shown on a time series
 #expander is present to show the variable given
with tab2:
    variables = st.multiselect('Select Variables for Time Series', 
                               options=['temperature_2m_mean', 'precipitation_hours', 
                                        'wind_speed_10m_max', 'shortwave_radiation_sum'], 
                                        default=['temperature_2m_mean'])
    
    expander = st.expander("Selected Variables Explanation")
    variables_explanation = {
        'temperature_2m_mean': 'Mean daily air temperature at 2 meters above ground',
        'precipitation_hours': 'Total hours of precipitation',
        'wind_speed_10m_max': 'Maximum wind speed at 10 meters above ground',
        'shortwave_radiation_sum': 'The sum of solar radiaion on a given day in Megajoules'
    }
    for var in variables:
        expander.write(f"{var}: {variables_explanation[var]}")

    time_series_data = df[['time'] + variables].set_index('time')
    fig, ax = plt.subplots()
    sns.lineplot(data=time_series_data, ax=ax)
    ax.set_title('Time Series of Selected Variables')
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    st.pyplot(fig)


#heat map of the correlation between the variables
#user selects the variable to be shown.
with tab3:
    selected_variable = st.selectbox('Select Variable to Measure Correlation with a 3-Day Future Snowfall', 
                                     options=['temperature_2m_mean', 'precipitation_hours', 
                                              'wind_speed_10m_max', 'shortwave_radiation_sum'])
    
    correlation_value = round(df[['3day_prediction', selected_variable]].corr().iloc[0, 1], 2)
    st.write(f"Correlation between 3day_prediction and {selected_variable}: {correlation_value}")

    fig, ax = plt.subplots()
    sns.scatterplot(x=df[selected_variable], y=df['3day_prediction'], ax=ax)
    ax.set_title(f'Scatter Plot of 3day_prediction vs {selected_variable}')
    ax.set_xlabel(selected_variable)
    ax.set_ylabel('3day_prediction')
    st.pyplot(fig)


