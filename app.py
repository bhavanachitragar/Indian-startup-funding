import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

# Overall Analysis
def load_overall_analysis():
    st.title('Overall Analysis')

    #total invested amount
    total = round(df['amount'].sum())
    # maximum
    max_fund = df.groupby('startup')['amount'].max().sort_values(ascending=False).head().values[0]
    # avg ticket size
    avg_fund=df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups=df['startup'].nunique()


    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',str(total)  + 'Cr')
    with col2:
        st.metric('Max', str(max_fund) + 'Cr')
    with col3:
        st.metric('Avg', str(round(avg_fund)) + 'Cr')
    with col4:
        st.metric('Funded Startups', (num_startups))
    col1, col2 = st.columns(2)
    with col1:
        st.header('MoM Graph')
        selected_option=st.selectbox('Select Type',['Total','Count'])
        if selected_option=='Total':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        else:
            temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()



        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df['x_axis'],temp_df['amount'])

        # Format x-axis labels as month-year
        ax5.xaxis.set_major_locator(mdates.MonthLocator())
        ax5.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig5)

    # Sector Analysis - Pie chart
    with col2:
        st.header('Sector Analysis')
        sector_option = st.selectbox('Select Type ', ['total', 'count'])
        if sector_option == 'total':
            tmp_df = df.groupby(['vertical'])['amount'].sum().sort_values(ascending=False).head(5)
        else:
            tmp_df = df.groupby(['vertical'])['amount'].count().sort_values(ascending=False).head(5)

        fig7, ax7 = plt.subplots()
        ax7.pie(tmp_df, labels=tmp_df.index, autopct="%0.01f%%")
        st.pyplot(fig7)


    col1, col2, = st.columns(2)
    with col1:
        st.header('Top Funding Type')
        funding_series = df.groupby('round')['round'].count().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.barh(funding_series.index[::-1], funding_series.values[::-1])
        st.pyplot(fig)

    with col2:
        st.header('Top Cities for Startups')
        city_funding = df.groupby('city')['amount'].sum().sort_values(ascending=False).head()
        fig_city, ax_city = plt.subplots()
        ax_city.barh(city_funding.index[::-1], city_funding.values[::-1])
        st.pyplot(fig_city)

    col1, col2, = st.columns(2)
    with col1:
        startups_df = df.groupby(['year', 'startup'])['amount'].sum().reset_index()
        st.header('Select Year:')
        selected_year = st.selectbox('Select Year', sorted(df['year'].unique()))
        selected_year_df = startups_df[startups_df['year'] == selected_year]
        top_startups = selected_year_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.write(f'Top Startups in {selected_year}:')
        st.table(top_startups)

    with col2:
        st.header('Overall Top Startups Analysis')
        overall_startups = df.groupby(['startup'])['date'].count().sort_values(ascending=False).head(7)
        fig8, ax8 = plt.subplots()
        ax8.barh(overall_startups.index[::-1], overall_startups.values[::-1])
        ax8.set_xlabel('amount')
        st.pyplot(fig8)


    st.header('Top Investors Analysis')
    investors_df = df.groupby('investors')['amount'].sum().reset_index()
    top_investors = investors_df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(7)
    st.write('Top Investors:')
    st.table(top_investors)


    def funding_heatmap():
        st.title('Funding Heatmap')
        st.subheader('Round Heatmap')
        heatmap_data = df[['year', 'amount', 'round']]
        heatmap_matrix2 = heatmap_data.pivot_table(index='round', columns='year', values='amount', aggfunc='sum',fill_value=0)
        fig17, ax17 = plt.subplots(figsize=(20, 8))
        sns.heatmap(heatmap_matrix2, cmap='rocket_r', annot=True, fmt=',.0f', linewidths=.5, ax=ax17,cbar_kws={"label": "Funding Amount"})
        plt.title('Funding Heatmap')
        plt.xlabel('Year')
        plt.ylabel('Round')
        st.pyplot(fig17)


        st.subheader('Startup Heatmap')
        df_agg = df[['year', 'amount', 'startup']]
        heatmap_matrix1 = df_agg.pivot_table(index='startup', columns='year', values='amount', aggfunc='sum')
        fig16, ax16 = plt.subplots(figsize=(15, 5))
        sns.heatmap(heatmap_matrix1,cmap='crest',vmax=20000, annot_kws={"size": 14},ax=ax16,cbar_kws={"label": "Funding Amount"})
        plt.xlabel('Year')
        plt.ylabel('Startup')
        st.pyplot(fig16)

    funding_heatmap()


# Investors Menu:
def load_investor_details(investor):
    st.title(investor)
    # load recent 5 investments
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    # biggest investment
    col1,col2=st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector Investments')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f")
        st.pyplot(fig1)


    # stage
        with col1:
            stage_series=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
            st.subheader('Stage Investments')
            fig2, ax2 = plt.subplots()
            ax2.pie(stage_series,labels=stage_series.index,autopct="%0.01f")
            st.pyplot(fig2)

        with col2:
            city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
            st.subheader('City Investments')
            fig3, ax3 = plt.subplots()
            ax3.pie(city_series, labels=city_series.index, autopct="%0.01f")
            st.pyplot(fig3)
        print(df.info())

    # year
        with col1:
            df['year'] = df['date'].dt.year
            year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
            st.subheader('YoY Investments')
            fig4, ax4 = plt.subplots()
            ax4.plot(year_series.index, year_series.values)
            st.pyplot(fig4)



    # Startup Menu:
def load_startup_details(startup):
    st.title(startup)

    st.subheader('Basic Information:')
    col1, col2 = st.columns(2)
    with col1:
        startup_vertical = df[df['startup'].str.contains(startup)]['vertical'].iloc[0]
        st.info(f'**Industy:** {startup_vertical}')

        startup_subvertical = df[df['startup'].str.contains(startup)]['subvertical'].iloc[0]
        st.info(f'**Sub-Industry:** {startup_subvertical}')

        startup_city = df[df['startup'].str.contains(startup)]['city'].iloc[0]
        st.info(f'**City:** {startup_city}')

        startup_date = df[df['startup'].str.contains(startup)]['date'].iloc[0]
        # Date Formating
        formatted_date = startup_date.strftime("%Y-%m-%d")
        st.info(f'**Date:** {formatted_date}')

        startup_investors = df[df['startup'].str.contains(startup)]['investors'].iloc[0]
        st.info(f'**Investors:** {startup_investors}')

        startup_round = df[df['startup'].str.contains(startup)]['round'].iloc[0]
        st.info(f'**Round:** {startup_round}')

        startup_amount = df[df['startup'].str.contains(startup)]['amount'].iloc[0]
        st.info(f'**Amount:** {startup_amount}'+' Cr')


# Sidebar
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option =='Overall Analysis':
        load_overall_analysis()

elif option =='StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)
