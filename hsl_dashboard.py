import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("hsl_cleaned.csv")
df['VARIANCE_PERCENT'] = (df['LENGTH_VARIANCE']/df['TOTAL_DESIGN_LENGTH']*100).fillna(0)
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])

st.set_page_config(layout="wide", page_title="HSL Cable Dashboard")
st.title("⚡ Cable Management & Optimization Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    fig = px.line(df, x="TIMESTAMP", y="LENGTH_VARIANCE", title="Length Variance Over Time")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(df, names="PROCURED_BY", title="Procurement Category Share", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = px.bar(df.groupby("CABLE_SIZE")["VARIANCE_PERCENT"].mean().reset_index(),
                 x="CABLE_SIZE", y="VARIANCE_PERCENT", title="Average Variance by Cable Size")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### High Variance Cables (>20%)")
high_var = df[df["VARIANCE_PERCENT"] > 20][["CABLE_TAG","LENGTH_VARIANCE","VARIANCE_PERCENT"]]
st.dataframe(high_var.head(20))
