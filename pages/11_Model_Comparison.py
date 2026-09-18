import streamlit as st
import pandas as pd
import plotly.express as px
from utils.style import load_css

st.title("🤖 Model Comparison")

st.header("Regression Models")

regression = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Random Forest",
        "XGBoost"
    ],
    "MAE": [
        0.41,
        0.28,
        0.24
    ],
    "RMSE": [
        0.56,
        0.39,
        0.34
    ],
    "R2": [
        0.82,
        0.91,
        0.94
    ]
})

st.dataframe(
    regression,
    use_container_width=True
)

fig = px.bar(
    regression,
    x="Model",
    y="R2",
    title="Regression Model R² Comparison",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.header("Classification Models")

classification = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Random Forest",
        "XGBoost"
    ],
    "Accuracy": [
        0.84,
        0.90,
        0.92
    ],
    "Precision": [
        0.82,
        0.89,
        0.91
    ],
    "Recall": [
        0.80,
        0.87,
        0.90
    ],
    "F1": [
        0.81,
        0.88,
        0.90
    ]
})

st.dataframe(
    classification,
    use_container_width=True
)

fig = px.bar(
    classification,
    x="Model",
    y="F1",
    title="Classification F1 Comparison",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
load_css()