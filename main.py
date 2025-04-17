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
df['month_year'] = df['time'].dt.to_period('M').astype(str)



st.title('Cracking the Snow Code')

tab1, tab2, tab3 = st.tabs(['Snowfall By Month', 'Time Series', 'Heat Map'])

season_mapping = {
        "23-24": ["2023-12", "2024-01", "2024-02", "2024-03"],
        "24-25": ["2024-12", "2025-01", "2025-02"]
    }

# User Selects year, and a graph of the the snowfall by month is shown.
with tab1: 
    selected_season = st.selectbox('Select Snow Season', options=season_mapping.keys())

    filtered_months = season_mapping[selected_season]
    seasonal_data = df[df['month_year'].isin(filtered_months)]

    monthly_snowfall = seasonal_data.groupby('month_year')['snowfall_sum'].sum()

    fig, ax = plt.subplots()
    sns.barplot(x=monthly_snowfall.index, y=monthly_snowfall.values, ax=ax)
    ax.set_title(f'Snowfall by Month-Year for Season {selected_season}')
    ax.set_xlabel('Month-Year')
    ax.set_ylabel('Total Snowfall')
    plt.xticks(rotation=45)
    st.pyplot(fig)


 # User selects variables shown on a time series
 #expander is present to show the variable given
with tab2:

    selected_season = st.selectbox('Select Snow Season for Time Series', options=season_mapping.keys(), key='season_ts')
    filtered_months = season_mapping[selected_season]
    seasonal_df = df[df['month_year'].isin(filtered_months)]

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

    time_series_data = seasonal_df[['time'] + variables].set_index('time')
    fig, ax = plt.subplots()
    sns.lineplot(data=time_series_data, ax=ax)
    ax.set_title(f'Time Series of Selected Variables ({selected_season} Season)')
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    plt.xticks(rotation=45)
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


