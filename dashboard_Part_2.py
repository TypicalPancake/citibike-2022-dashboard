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
    st.title("🚲 CitiBike NYC Dashboard")
    st.markdown("""
    Welcome to the interactive dashboard for New York's CitiBike program.
    
    This dashboard explores bike usage trends, temperature correlations, and geographic movement across the city.
    
    Use the sidebar to navigate through each section.
    """)

# ========== PAGE: TOP START STATIONS ==========
elif page == "Top Start Stations":
    st.subheader("🔝 Top 20 Start Stations")
    top_stations = df['start_station_name'].value_counts().nlargest(20).reset_index()
    top_stations.columns = ['station', 'count']
    fig1 = px.bar(top_stations, x='count', y='station', orientation='h', title='Top 20 Start Stations')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("**Insight:** These stations consistently see high ridership and should be prioritized for bike rebalancing and station maintenance.")

# ========== PAGE: TRIPS VS TEMPERATURE ==========
elif page == "Trips vs Temperature":
    st.subheader("📈 Trip Count and Temperature Over Time")
    trip_counts = df.groupby('date').size().reset_index(name='trip_count')
    weather = df[['date', 'TMAX']].dropna().drop_duplicates()
    combined = pd.merge(trip_counts, weather, on='date')

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=combined['date'], y=combined['trip_count'], name='Trips', yaxis='y1'))
    fig2.add_trace(go.Scatter(x=combined['date'], y=combined['TMAX'], name='TMAX (°F)', yaxis='y2'))
    fig2.update_layout(
        title='Trip Count and Temperature Over Time',
        yaxis=dict(title='Trip Count'),
        yaxis2=dict(title='TMAX (°F)', overlaying='y', side='right')
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("**Interpretation:** Warmer temperatures are strongly associated with increased ridership.")

# ========== PAGE: KEPLER MAP ==========
elif page == "Trip Flow Map":
    st.subheader("🌍 Kepler.gl Trip Flow Map")

    map_file_name = "citibike_trip_map.html"
    static_path = os.path.join("static", map_file_name)

    if os.path.exists(static_path):
        st.success("✅ Map file found!")
        st.markdown(
            f'[🌍 Open Kepler.gl Map in New Tab](./static/{map_file_name})',
            unsafe_allow_html=True
        )
        st.markdown("**Insight:** Dense flows are visible in lower Manhattan and waterfront zones, highlighting commuter corridors.")
    else:
        st.error("❌ Map file not found in /static folder.")

# ========== PAGE: RECOMMENDATIONS ==========
elif page == "Recommendations":
    st.subheader("📌 Final Recommendations")
    st.markdown("""
    - 🧊 **Scale back supply by ~30% from November to April**, when ridership drops due to weather.
    - 🌊 **Add stations near the waterfront**, where trip flows are heavily concentrated but station presence is lower.
    - 🔄 **Use dynamic bike rebalancing** at peak stations (e.g., top 10) to prevent stockouts and overflows.
    """)

# Footer
st.markdown("---")
st.write("🔧 Reached the end of the dashboard script.")
