import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    layout='wide',
    page_title='Indian Startup Funding Trends Dashboard',
    page_icon='📊'
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
df = pd.read_csv('startup_cleaned.csv')

# ---------------------------------------------------
# OVERALL ANALYSIS
# ---------------------------------------------------
def load_overall_analysis():

    st.title('🚀 Indian Startup Funding Trends Dashboard')
    st.markdown("### Comprehensive Investment Insights (2015–2020)")
    st.markdown("---")

    # ---------------- KPI Section ----------------
    total = round(df['amount'].sum())
    maximum = round(df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0])
    average = round(df['amount'].mean(), 2)
    funded_startups = df['startup'].nunique()
    total_deals = df.shape[0]

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric('💰 Total Funding', f"{total} Cr")
    with c2:
        st.metric('📈 Maximum Investment', f"{maximum} Cr")
    with c3:
        st.metric('📊 Average Investment', f"{average} Cr")
    with c4:
        st.metric('🏢 Funded Startups', funded_startups)
    with c5:
        st.metric('📑 Total Deals', total_deals)

    st.markdown("---")

    # ---------------- Month-on-Month ----------------
    st.header('📅 Month-on-Month Investments')

    selected_option = st.selectbox('Select Type', ['Total Amount', 'Total Deals'])

    if selected_option == 'Total Amount':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

    fig5, ax5 = plt.subplots(figsize=(14,5))
    ax5.plot(temp_df['x_axis'], temp_df['amount'], marker='o')

    # Reduce overlapping labels
    ax5.set_xticks(ax5.get_xticks()[::4])
    ax5.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig5)

    st.markdown("---")

    # ---------------- Year-wise Funding ----------------
    st.header('📊 Year-wise Total Funding Analysis')

    yearly_funding = df.groupby('year')['amount'].sum()

    fig_year, ax_year = plt.subplots(figsize=(8,4))
    ax_year.bar(yearly_funding.index.astype(str), yearly_funding.values)
    ax_year.set_xlabel("Year")
    ax_year.set_ylabel("Total Funding (Cr)")

    plt.tight_layout()
    st.pyplot(fig_year)

    st.markdown("---")

    # ---------------- Top Sectors ----------------
    c1, c2 = st.columns(2)

    with c1:
        st.subheader('Top 10 Sectors (Number of Investments)')
        top_verticals = df['vertical'].value_counts().nlargest(10)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.pie(top_verticals, labels=top_verticals.index,
               autopct='%0.1f%%', textprops={'fontsize':8})
        plt.tight_layout()
        st.pyplot(fig)

    with c2:
        st.subheader('Top 10 Sectors (Total Amount)')
        top_verticals_amt = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.pie(top_verticals_amt, labels=top_verticals_amt.index,
               autopct='%0.1f%%', textprops={'fontsize':8})
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    # ---------------- Top Cities ----------------
    c1, c2 = st.columns(2)

    with c1:
        st.subheader('Top Cities (Number of Fundings)')
        top_cities = df['city'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.pie(top_cities, labels=top_cities.index,
               autopct='%0.1f%%', textprops={'fontsize':8})
        plt.tight_layout()
        st.pyplot(fig)

    with c2:
        st.subheader('Top Cities (Total Funding Amount)')
        top_cities_amt = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.pie(top_cities_amt, labels=top_cities_amt.index,
               autopct='%0.1f%%', textprops={'fontsize':8})
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    # ---------------- Heatmap ----------------
    st.header('🔥 Funding Heatmap')

    heatmap_option = st.selectbox('Select Heatmap Type',
                                  ['Total Amount', 'Total Deals'])

    if heatmap_option == 'Total Amount':
        heatmap_data = pd.pivot_table(df,
                                      columns="year",
                                      index="month",
                                      values="amount",
                                      aggfunc='sum')
    else:
        heatmap_data = pd.pivot_table(df,
                                      columns="year",
                                      index="month",
                                      values="amount",
                                      aggfunc='count')

    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(heatmap_data,
                annot=True,
                fmt=".1f",
                cmap="cividis",
                ax=ax)

    plt.tight_layout()
    st.pyplot(fig)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title('📌 Dashboard Navigation')
st.sidebar.markdown("Explore Funding Insights Below")

option = st.sidebar.radio(
    'Select Analysis Type',
    ['Overall Analysis']
)

if option == 'Overall Analysis':
    load_overall_analysis()