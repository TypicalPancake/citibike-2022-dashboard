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
    st.markdown("""
    Welcome to this interactive presentation on New York City's CitiBike program.  
    If you're unfamiliar, CitiBike is a bike-sharing service across NYC, with stations allowing riders to borrow and return bikes as needed.

    This dashboard explores how people used CitiBikes during 2022 — when and where people rode, how it relates to weather, and what patterns we found.

    👉 Use the sidebar on the left to choose an interactive section.
    """)
    st.metric(label="Total Trips in 2022", value=f"{df.shape[0]:,}")

    st.markdown("""
    ---
    ✅ **Navigation Guide**:  
    - **Top Start Stations**: See the busiest pickup spots.  
    - **Trips vs Temperature**: Explore how weather affects ridership.  
    - **Trip Flow Map**: View trip patterns on an interactive map.  
    - **Recommendations**: Data-backed suggestions for the CitiBike program.
    """)

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
    **Insight:** These stations are the most used in NYC.  
    This helps planners know where demand is highest — usually near transit hubs, parks, and busy work zones.

    Recommending more frequent maintenance and bike rebalancing at these hotspots.
    """)

# ========== PAGE: TRIPS VS TEMPERATURE ==========
elif page == "Trips vs Temperature":
    st.subheader("\U0001F4C8 Trip Count and Temperature Over Time")
    trip_counts = df.groupby('date').size().reset_index(name='trip_count')
    weather = df[['date', 'TMAX']].dropna().drop_duplicates()
    combined = pd.merge(trip_counts, weather, on='date')

    try:
        min_date = pd.to_datetime(combined['date'].min()).date()
        max_date = pd.to_datetime(combined['date'].max()).date()
        date_range = st.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

        if isinstance(date_range, tuple) and len(date_range) == 2:
            combined_filtered = combined[(combined['date'] >= pd.to_datetime(date_range[0])) & (combined['date'] <= pd.to_datetime(date_range[1]))]
        else:
            combined_filtered = combined

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
        **Insight:** There's a clear trend — as temperatures rise, more people ride.  
        This suggests warm weather campaigns or promotions could encourage even more usage.
        """)
    except Exception as e:
        st.error(f"Could not display temperature trend: {e}")

# ========== PAGE: KEPLER MAP ==========
elif page == "Trip Flow Map":
    st.subheader("\U0001F30D Kepler.gl Trip Flow Map")

    st.warning("\U0001F6A8 The map is hosted externally due to file size. Click below to view it in a new tab.")
    st.markdown('[\U0001F30D Open Kepler.gl Map in New Tab](https://drive.google.com/uc?id=13N1MMIG08gxIIwq3Kh49_hY90etjiEt8)', unsafe_allow_html=True)

    st.markdown("""
    **Insight:** The interactive map shows bike paths forming visible corridors — especially in lower Manhattan and by the water.
    This helps reveal urban travel behavior and where infrastructure like new stations or bike lanes would help.
    """)

# ========== PAGE: RECOMMENDATIONS ==========
elif page == "Recommendations":
    st.subheader("\U0001F4CC Final Recommendations")
    st.markdown("""
    - \U0001F9CA **Scale back supply by ~30% from November to April**, when ridership drops due to weather.
    - \U0001F30A **Add stations near the waterfront**, where trip flows are heavily concentrated but station presence is lower.
    - \U0001F501 **Use dynamic bike rebalancing** at peak stations (e.g., top 10) to prevent stockouts and overflows.
    """)

    if st.checkbox("Show Monthly Ride Totals"):
        monthly_trips = df['date'].dt.month.value_counts().sort_index()
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_trips.index = [month_labels[i-1] for i in monthly_trips.index]

        fig_monthly = px.bar(x=monthly_trips.index, y=monthly_trips.values, labels={'x': 'Month', 'y': 'Trips'}, title='Monthly CitiBike Trips')
        st.plotly_chart(fig_monthly, use_container_width=True)
        st.markdown("""
        This chart helps visualize the seasonal demand — peaks in summer and low points in winter.  
        This insight can be used to plan staffing, maintenance, and bike inventory.
        """)

# Footer
st.markdown("---")
st.write("\U0001F527 Reached the end of the dashboard script.")
