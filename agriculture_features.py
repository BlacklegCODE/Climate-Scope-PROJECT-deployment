import streamlit as st
import pandas as pd
import plotly.express as px

def show_agriculture_dashboard(df, filters):
    st.title("🌾 Agriculture Analysis")
    st.markdown("**Climate impact on agriculture productivity**")

    # ===============================
    # BASIC SAFETY CHECK
    # ===============================
    required_cols = ['temperature_celsius', 'humidity', 'precip_mm', 'wind_kph']
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing column: {col}")
            return

    # ===============================
    # AGRICULTURE METRICS
    # ===============================
    st.subheader("🌱 Crop-Friendly Conditions Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Avg Temperature",
        f"{df['temperature_celsius'].mean():.1f} °C"
    )

    col2.metric(
        "Avg Humidity",
        f"{df['humidity'].mean():.0f} %"
    )

    col3.metric(
        "Avg Rainfall",
        f"{df['precip_mm'].mean():.1f} mm"
    )

    col4.metric(
        "Avg Wind Speed",
        f"{df['wind_kph'].mean():.1f} km/h"
    )

    st.markdown("---")

    # ===============================
    # IDEAL CONDITIONS LOGIC
    # ===============================
    st.subheader("✅ Ideal Farming Days Detection")

    ideal_days = df[
        (df['temperature_celsius'].between(18, 32)) &
        (df['humidity'].between(40, 75)) &
        (df['precip_mm'] <= 10) &
        (df['wind_kph'] <= 25)
    ]

    st.success(f"🌾 Ideal Farming Days Found: {len(ideal_days):,}")

    # ===============================
    # TREND CHARTS
    # ===============================
    st.markdown("---")
    st.subheader("📈 Climate Trends Affecting Crops")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            df.groupby(df['last_updated_dt'].dt.date)['temperature_celsius'].mean().reset_index(),
            x='last_updated_dt',
            y='temperature_celsius',
            title="Daily Avg Temperature"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.line(
            df.groupby(df['last_updated_dt'].dt.date)['precip_mm'].mean().reset_index(),
            x='last_updated_dt',
            y='precip_mm',
            title="Daily Avg Rainfall"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # AGRICULTURE RISK ANALYSIS
    # ===============================
    st.markdown("---")
    st.subheader("⚠️ Agriculture Risk Analysis")

    risks = {
        "Heat Stress (>35°C)": len(df[df['temperature_celsius'] > 35]),
        "Drought (Rain <1mm)": len(df[df['precip_mm'] < 1]),
        "Excess Rain (>20mm)": len(df[df['precip_mm'] > 20]),
        "High Wind (>40km/h)": len(df[df['wind_kph'] > 40])
    }

    fig = px.bar(
        x=list(risks.keys()),
        y=list(risks.values()),
        title="Crop Risk Events Count",
        text=list(risks.values())
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # LOCATION TABLE
    # ===============================
    st.markdown("---")
    st.subheader("📍 Location-wise Agriculture Summary")

    table = df.groupby('location_name').agg({
        'temperature_celsius': 'mean',
        'humidity': 'mean',
        'precip_mm': 'mean',
        'wind_kph': 'mean'
    }).round(1).reset_index()

    table.columns = [
        "Location",
        "Avg Temp (°C)",
        "Avg Humidity (%)",
        "Avg Rainfall (mm)",
        "Avg Wind (km/h)"
    ]

    st.dataframe(table, use_container_width=True)

    st.markdown("---")
    st.success("🌾 Agriculture Analysis Module Loaded Successfully")

