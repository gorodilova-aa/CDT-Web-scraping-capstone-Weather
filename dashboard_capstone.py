import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------------
# Page configuration
st.set_page_config(
    page_title="Weather: Raleigh vs Novosibirsk",
    page_icon="⛅", 
    layout="wide"
)

# ------------------------------------------------------------------
# connect to SQLite database
try:
    db_path='capstone_weather.db'
    conn = sqlite3.connect(db_path)
    query = """
        SELECT 
            city, 
            year, 
            month, 
            month_name, 
            metric, 
            temp_f, 
            humidity_pct, 
            pressure_inHg 
        FROM weather_records
        ORDER BY month ASC;
    """
    df_weather = pd.read_sql_query(query, conn)
    conn.close()

    # Add a new column for temperature in Celsius
    df_weather['temp_c'] = ((df_weather['temp_f'] - 32) * 5 / 9).round(1)

except Exception as err:
    st.error(f"Could not connect to SQLite database: {err}")
    st.stop()


# ------------------------------------------------------------------
# Title
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #1f77b4 0%, #00b4d8 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    ">
        <h1 style="color: white; margin: 0; font-size: 2.3rem;">🌤️ Climate Comparison 2025</h1>
        <h3 style="color: #e0f2fe; margin-top: 8px; margin-bottom: 8px; font-weight: 400;">
            ❄️ Novosibirsk, Siberia, Russia vs. Raleigh, NC, USA 🌞
        </h3>
        <p style="color: #f0f9ff; margin: 0; font-size: 0.95rem;">
            Interactive historical weather graphics for the year 2025 between two geographically distinct locations.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)




# ------------------------------------------------------------------
# --- Sidebar 

# Logo
with st.sidebar:
    st.title("🐿️ Squirrel Weather")
    st.caption("Weather Analytics v1.0")
    st.divider()


# Sidebar filters
with st.sidebar:
    st.header("Choose Filters")

    # Temperature unit selection
    temp_unit = st.radio("Temperature Unit:", ["Celsius (°C)", "Fahrenheit (°F)"])
    temp_col = 'temp_c' if "Celsius" in temp_unit else 'temp_f'
    unit_symbol = "°C" if "Celsius" in temp_unit else "°F"

    # City selection
    available_cities = df_weather['city'].unique().tolist()
    selected_cities = st.multiselect(
        "Choose Cities:",
        options=available_cities,
        default=available_cities
    )

    # Metric type (Average / High / Low)
    metrics = df_weather['metric'].unique().tolist()
    selected_metrics = st.multiselect(
        "Type of Temperature Indicator:",
        options=metrics,
        default=metrics
    )
    
# ------------------------------------------------------------------
# Gallery
with st.sidebar:
    st.divider()
    st.header("Gallery")

    st.image("img/Siberia.jpg", caption="Siberia • Photo by A. Gorodilova",  use_container_width=True)
    st.image("img/NC.jpg", caption="North Carolina • Photo by A. Gorodilova", use_container_width=True)    

# Author and data info
with st.sidebar:
    st.divider()
    st.caption("Created with 🤍 to both places by **Anastasiia Gorodilova**")
    st.caption("Data Source: [Weather Around The World](https://www.timeanddate.com/weather/)")


# ------------------------------------------------------------------
# Data filtering based on user selections
filtered_df = df_weather[
    (df_weather['city'].isin(selected_cities)) & 
    (df_weather['metric'].isin(selected_metrics))
]

if filtered_df.empty:
    st.warning("The selected filters returned no data. Please adjust your selections.")
    st.stop()


# ------------------------------------------------------------------
# --- Key Metrics ---
if not selected_cities:
    st.info("Please select at least one city.")
else:
    for city in selected_cities:
        city_df = filtered_df[filtered_df['city'] == city]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("", city)
        with col2:
            max_val = city_df[temp_col].max()
            st.metric(
                f"Absolute Max ({unit_symbol})", 
                f"{max_val:.1f} {unit_symbol}" if pd.notna(max_val) else "N/A"
            )
        with col3:
            min_val = city_df[temp_col].min()
            st.metric(
                f"Absolute Min ({unit_symbol})", 
                f"{min_val:.1f} {unit_symbol}" if pd.notna(min_val) else "N/A"
            )
        with col4:
            # Учитываем фильтрацию по метрике 'Average' (или Indicator)
            metric_col = 'metric' if 'metric' in city_df.columns else 'Indicator'
            avg_series = city_df[city_df[metric_col] == 'Average'][temp_col]
            avg_val = avg_series.mean() if not avg_series.empty else city_df[temp_col].mean()
            
            st.metric(
                f"Annual Average ({unit_symbol})", 
                f"{avg_val:.1f} {unit_symbol}" if pd.notna(avg_val) else "N/A"
            )
            
        



st.markdown("---")

# ------------------------------------------------------------------
# --- Yearly Temperature Profile ---
st.subheader(f"Yearly Temperature Profile ({unit_symbol})")
fig_temp = px.line(
    filtered_df,
    x="month_name",
    y=temp_col,
    color="city",
    line_dash="metric",
    markers=True,
    title=f"Temperature Dynamics by Month ({unit_symbol})",
    labels={
        "month_name": "Month",
        temp_col: f"Temperature ({unit_symbol})",
        "city": "City",
        "metric": "Indicator"
    },
    category_orders={"month_name": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]}
)
fig_temp.update_layout(hovermode="x unified", template="plotly_white")
st.plotly_chart(fig_temp, use_container_width=True)

st.markdown("---")

# Two columns for charts 2 and 3
col_left, col_right = st.columns(2)

# --- Humidity Comparison ---
with col_left:
    st.subheader("Average Humidity by Month")
    humidity_df = df_weather[(df_weather['city'].isin(selected_cities)) & (df_weather['metric'] == 'Average')]
    fig_hum = px.bar(
        humidity_df,
        x="month_name",
        y="humidity_pct",
        color="city",
        barmode="group",
        title="Average Humidity by Month",
        labels={"month_name": "Month", "humidity_pct": "Humidity (%)", "city": "City"},
        category_orders={"month_name": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]}
    )
    fig_hum.update_layout(template="plotly_white")
    st.plotly_chart(fig_hum, use_container_width=True)

# --- Relationship between Temperature and Pressure ---
with col_right:
    st.subheader("Temperature vs. Atmospheric Pressure")
    fig_scatter = px.scatter(
        filtered_df,
        x="pressure_inHg",
        y=temp_col,
        color="city",
        symbol="metric",
        hover_data=["month_name"],
        title="Correlation between Pressure (inHg) and Temperature",
        labels={
            "pressure_inHg": "Pressure (inHg)",
            temp_col: f"Temperature ({unit_symbol})",
            "city": "City",
            "metric": "Indicator"
        }
    )
    fig_scatter.update_layout(template="plotly_white")
    st.plotly_chart(fig_scatter, use_container_width=True)


st.markdown("---")



# ------------------------------------------------------------------
# --- Key Climate Insights ---
st.subheader("💡 Key Climate Insights")

col_left, col_right = st.columns(2)

with col_left:
    with st.expander("🌡️ Temperature Range & Extremes", expanded=False):
        st.markdown("""
        ➡️ Novosibirsk exhibits an extreme annual temperature **swing of 64.4 °C (116 °F)** compared to **47.2 °C (85 °F)** in Raleigh.
        
        ➡️  Both locations reach comparable summer highs **32.2 °C (90 °F)**  for Norosibirsk and **37.8 °C (100 °F)** for Raleigh 
        
        ➡️  Winter completely separates their climate profiles: Novosibirsk plunges to **−32.2 °C (−26 °F)** while Raleigh only dips to **−9.4 °C (15 °F)**.

        **Takeaway:** Both locations experience similar summer conditions, but winter climates are distinctly different.  
        """)

    with st.expander("💧 The Humidity Paradox", expanded=False):
        st.markdown("""
        ➡️ Both cities show **65–75%** relative humidity in summer.

        **Paradox 1:** Raleigh feels dramatically more humid and oppressive. 

        ➡️ Novosibirsk's winter relative humidity is **~80%**.

        **Paradox 2:** In fact, Novosibirsk winter air is drier than Raleigh's summer.

        **Takeaway:** 
        *Relative Humidity (%)* only measures how close the air is to saturation at its current temperature. So, the humidity paradox arises because Raleigh's summer air is warmer and can hold more moisture, making it feel more humid, while Novosibirsk's winter air is colder and holds less moisture, even if the relative humidity percentage is high.
        """)

with col_right:
    with st.expander("📈 Thermal Baseline & Living Conditions", expanded=False):
        st.markdown("""
        ➡️ Raleigh's annual average temperature **16.7 °C (62.1 °F)** is significantly higher than Novosibirsk's **3.7 °C (38.7 °F)**.
        
        **Takeaway:** 
        Raleigh sustains positive average temperatures across all twelve months, with freezing periods being brief and episodic. 
        Conversely, Novosibirsk endures a continuous sub-zero winter regime lasting nearly five consecutive months.

        **Obsetrvation:** 
               Raleigh's averages <-> Novosibirsk's high temperatures & 
               Novosibirsk's average <-> Raleigh's low temperatures
        """)

    with st.expander("🌀 Atmospheric Dynamics & Pressure", expanded=False):
        st.markdown("""
        ➡️ Raleigh: Atmospheric pressure remains relatively stable year-round, consistently hovering near 30.0 inHg.

        ➡️ Novosibirsk: Pressure exhibits pronounced seasonal swings, dropping to its lowest levels in the summer months and peaking sharply during winter.
           
        **Takeaway:** 
        The pressure-temperature distribution reflects the classic Siberian High: clear skies and peak winter cold coincide with maximum barometric pressure. 
        Raleigh maintains a tighter pressure window, driven by passing frontal systems and humid subtropical air masses.
        """)


st.markdown("---")
# ------------------------------------------------------------------
# --- Table of Raw Data (Collapsible)
st.subheader("Table of the original dataset")
with st.expander("View Original Records from Database"):
    st.dataframe(filtered_df, use_container_width=True)



