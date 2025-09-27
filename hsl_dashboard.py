import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("hsl_cleaned.csv")
df['VARIANCE_PERCENT'] = (df['LENGTH_VARIANCE']/df['TOTAL_DESIGN_LENGTH']*100).fillna(0)
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])

st.set_page_config(layout="wide", page_title="HSL Cable Dashboard")
st.title("⚡ Cable Management & Optimization Dashboard")

# --- Filters ---
st.sidebar.header("Filters")
procured_filter = st.sidebar.multiselect(
    "Procurement Category",
    options=df["PROCURED_BY"].unique(),
    default=df["PROCURED_BY"].unique()
)

size_filter = st.sidebar.multiselect(
    "Cable Size",
    options=df["CABLE_SIZE"].unique(),
    default=df["CABLE_SIZE"].unique()
)

df_filtered = df[
    (df["PROCURED_BY"].isin(procured_filter)) &
    (df["CABLE_SIZE"].isin(size_filter))
]

# --- Layout Columns ---
col1, col2, col3 = st.columns(3)

with col1:
    fig = px.line(df_filtered, x="TIMESTAMP", y="LENGTH_VARIANCE",
                  title="Length Variance Over Time")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(df_filtered, names="PROCURED_BY",
                 title="Procurement Category Share", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    # Highlight bars with VARIANCE_PERCENT > 20%
    bar_colors = ['crimson' if v > 20 else 'steelblue' for v in df_filtered.groupby("CABLE_SIZE")["VARIANCE_PERCENT"].mean()]
    fig = px.bar(df_filtered.groupby("CABLE_SIZE")["VARIANCE_PERCENT"].mean().reset_index(),
                 x="CABLE_SIZE", y="VARIANCE_PERCENT",
                 title="Average Variance by Cable Size",
                 color_discrete_sequence=bar_colors)
    st.plotly_chart(fig, use_container_width=True)

# --- High Variance Cables ---
st.markdown("### High Variance Cables (>20%)")
high_var = df_filtered[df_filtered["VARIANCE_PERCENT"] > 20][["CABLE_TAG","LENGTH_VARIANCE","VARIANCE_PERCENT"]]
st.dataframe(high_var)

# --- Download Button ---
csv = high_var.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download High Variance Cables CSV",
    data=csv,
    file_name='high_variance_cables.csv',
    mime='text/csv'
)

