import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Streamlit page layout
st.set_page_config(page_title="CitiBike NYC Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("Manipulated Data/merged_citibike_weather_2022.csv", parse_dates=["date", "started_at", "ended_at"])

# Dashboard title
st.title("🚲 CitiBike NYC Dashboard")
st.markdown("Interactive dashboard showing ride patterns, temperature trends, and a trip flow map.")

# SECTION 1: Top 20 Start Stations
top_stations = df['start_station_name'].value_counts().nlargest(20).reset_index()
top_stations.columns = ['station', 'count']
fig1 = px.bar(top_stations, x='count', y='station', orientation='h', title='Top 20 Start Stations')
st.plotly_chart(fig1, use_container_width=True)

# SECTION 2: Dual Axis Line Chart (Trips vs Temp)
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

# SECTION 3: Kepler.gl Map (via Streamlit's static path)
st.markdown("### 📍 Kepler.gl Trip Flow Map")

map_file_name = "citibike_trip_map.html"
static_path = os.path.join("static", map_file_name)
public_url = f"/static/{map_file_name}"

if os.path.exists(static_path):
    st.success("✅ Map file found!")
    st.markdown(
        '[🌍 Open Kepler.gl Map](./static/citibike_trip_map.html)',
     unsafe_allow_html=True
)

else:
    st.error("❌ Map file not found in /static folder.")


# Footer
st.markdown("---")
st.write("🔧 Reached the end of the dashboard script.")
