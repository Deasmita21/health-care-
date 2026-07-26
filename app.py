import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Healthcare Capacity Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Capacity Analytics Dashboard")
st.markdown("### System Capacity & Care Load Analytics for Unaccompanied Children")

st.markdown("---")

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")
    df["Total_System_Load"] = (
    df["Children in CBP custody"] +
    df["Children in HHS Care"]
)

    return df


df = load_data()
st.write(df.columns)

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.header("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# -----------------------------------------------------
# DATA PREVIEW
# -----------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(filtered_df)

st.markdown("---")

# -----------------------------------------------------
# DATA STATISTICS
# -----------------------------------------------------

st.subheader("Basic Statistics")

st.dataframe(filtered_df.describe())

st.markdown("---")
st.subheader("Key Performance Indicators")

col1,col2,col3,col4=st.columns(4)

col1.metric(
    "Maximum System Load",
    int(filtered_df["Total_System_Load"].max())
)

col2.metric(
    "Maximum Net Intake",
    int(filtered_df["Net_Daily_Intake"].max())
)

col3.metric(
    "Maximum Backlog",
    int(filtered_df["Backlog"].max())
)

col4.metric(
    "Average System Load",
    round(filtered_df["Total_System_Load"].mean(),2)
)
st.subheader("Total System Load")

fig = px.line(
    filtered_df,
    x="Date",
    y="Total_System_Load",
    title="Total System Load"
)

st.plotly_chart(fig,use_container_width=True)
st.subheader("CBP vs HHS")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Children in CBP custody"],
        name="CBP Custody"
    )
)

fig.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Children in HHS Care"],
        name="HHS Care"
    )
)

st.plotly_chart(fig,use_container_width=True)
st.subheader("Net Daily Intake")

fig = px.line(
    filtered_df,
    x="Date",
    y="Net_Daily_Intake"
)

st.plotly_chart(fig,use_container_width=True)
st.subheader("Backlog")

fig = px.line(
    filtered_df,
    x="Date",
    y="Backlog"
)

st.plotly_chart(fig,use_container_width=True)
st.subheader("Care Load Growth Rate")

fig = px.line(
    filtered_df,
    x="Date",
    y="Care_Load_Growth_Rate"
)

st.plotly_chart(fig,use_container_width=True)
st.subheader("Rolling Average")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Rolling_7_Day"],
        name="7-Day Average"
    )
)

fig.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Rolling_14_Day"],
        name="14-Day Average"
    )
)

st.plotly_chart(fig,use_container_width=True)
st.markdown("---")

st.success("Healthcare Capacity Analytics Dashboard Successfully Loaded")
