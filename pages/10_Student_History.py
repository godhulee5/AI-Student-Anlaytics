import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.style import load_css


st.title("📋 Student Academic History")

df = pd.read_csv(
    "student_processed.csv"
)

student_id = st.selectbox(
    "Select Student",
    df["Student_ID"]
)

student = df[
    df["Student_ID"] == student_id
].iloc[0]

history = pd.DataFrame({
    "Stage": [
        "Previous CGPA",
        "Final CGPA"
    ],
    "GPA": [
        student["Previous_CGPA"],
        student["Final_CGPA"]
    ]
})

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=history["Stage"],
        y=history["GPA"],
        mode="lines+markers+text",
        text=history["GPA"].round(2),
        textposition="top center"
    )
)

fig.update_yaxes(
    range=[0, 4]
)

fig.update_layout(
    title="Academic Performance Journey"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

difference = (
    student["Final_CGPA"]
    -
    student["Previous_CGPA"]
)

if difference > 0.1:

    st.success(
        "📈 Student performance is improving."
    )

elif difference < -0.1:

    st.error(
        "📉 Student performance is declining."
    )

else:

    st.info(
        "➡️ Student performance is relatively stable."
    )

load_css()