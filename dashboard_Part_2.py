import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Streamlit page layout
st.set_page_config(page_title="CitiBike NYC Dashboard", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Choose a page:", [
    "Intro",
    "Top Start Stations",
    "Trips vs Temperature",
    "Trip Flow Map",
    "Recommendations"
])

# Load dataset
df = pd.read_csv("sampled_citibike_weather_2022.csv", parse_dates=["date", "started_at", "ended_at"])

# ========== PAGE: INTRO ==========
if page == "Intro":
    st.title("\U0001F6B2 CitiBike NYC Dashboard")
    st.image("images/nyc_citibike.jpg", caption="CitiBike in New York City", use_column_width=True)
    st.markdown("""
    Welcome to the interactive dashboard for New York's CitiBike program.

    This dashboard explores bike usage trends, temperature correlations, and geographic movement across the city.

    Use the sidebar to navigate through each section.
    """)
    st.metric(label="Total Trips in 2022", value=f"{df.shape[0]:,}")

# ========== PAGE: TOP START STATIONS ==========
elif page == "Top Start Stations":
    st.subheader("\U0001F51D Top 20 Start Stations")
    month_choice = st.selectbox("Filter by Month", df['date'].dt.month_name().unique())
    filtered_df = df[df['date'].dt.month_name() == month_choice]
    top_stations = filtered_df['start_station_name'].value_counts().nlargest(20).reset_index()
    top_stations.columns = ['station', 'count']

    fig1 = px.bar(top_stations, x='count', y='station', orientation='h', 
                  title=f'Top 20 Start Stations - {month_choice}',
                  hover_data=['count'])
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Insight:** These stations consistently attract high demand.  
    Consider:  
    - Increasing bike supply at these locations during peak hours.  
    - Adding nearby satellite stations to reduce congestion.
    """)

# ========== PAGE: TRIPS VS TEMPERATURE ==========
elif page == "Trips vs Temperature":
    st.subheader("\U0001F4C8 Trip Count and Temperature Over Time")
    trip_counts = df.groupby('date').size().reset_index(name='trip_count')
    weather = df[['date', 'TMAX']].dropna().drop_duplicates()
    combined = pd.merge(trip_counts, weather, on='date')

    date_range = st.slider("Select Date Range", min_value=combined['date'].min(), max_value=combined['date'].max(), value=(combined['date'].min(), combined['date'].max()))
    combined_filtered = combined[(combined['date'] >= date_range[0]) & (combined['date'] <= date_range[1])]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=combined_filtered['date'], y=combined_filtered['trip_count'], name='Trips', yaxis='y1'))
    fig2.add_trace(go.Scatter(x=combined_filtered['date'], y=combined_filtered['TMAX'], name='TMAX (°F)', yaxis='y2'))
    fig2.update_layout(
        title='Trip Count and Temperature Over Time',
        yaxis=dict(title='Trip Count'),
        yaxis2=dict(title='TMAX (°F)', overlaying='y', side='right')
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Interpretation:** Warmer temperatures are strongly associated with increased ridership.

    Use this relationship to adjust supply proactively during heatwaves and promote off-peak usage during cold spells.
    """)

# ========== PAGE: KEPLER MAP ==========
elif page == "Trip Flow Map":
    st.subheader("\U0001F30D Kepler.gl Trip Flow Map")

    st.warning("\U0001F6A8 The map is hosted externally due to file size. Click below to view it in a new tab.")
    st.markdown(
        '[\U0001F30D Open Kepler.gl Map in New Tab](https://drive.google.com/uc?id=13N1MMIG08gxIIwq3Kh49_hY90etjiEt8)',
        unsafe_allow_html=True
    )

    with st.expander("See Example Snapshot of the Map"):
        st.image("images/kepler_map_preview.png", caption="Sample Trip Flows")

    st.markdown("""
    **Insight:** Dense flows are visible in lower Manhattan and waterfront zones, highlighting commuter corridors.  
    Target infrastructure improvements in these high-density zones.
    """)

# ========== PAGE: RECOMMENDATIONS ==========
elif page == "Recommendations":
    st.subheader("\U0001F4CC Final Recommendations")
    st.markdown("""
    - \U0001F9CA **Scale back supply by ~30% from November to April**, when ridership drops due to weather.
    - \U0001F30A **Add stations near the waterfront**, where trip flows are heavily concentrated but station presence is lower.
    - \U0001F501 **Use dynamic bike rebalancing** at peak stations (e.g., top 10) to prevent stockouts and overflows.
    """)

    if st.checkbox("Show Seasonal Usage Trend"):
        monthly_trips = df['date'].dt.month.value_counts().sort_index()
        st.bar_chart(monthly_trips)

# Footer
st.markdown("---")
st.write("\U0001F527 Reached the end of the dashboard script.")
