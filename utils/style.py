
import streamlit as st
from pathlib import Path


def load_css():
    """
    Load and apply the project's custom CSS
    to the current Streamlit page.
    """

    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent

    # Locate the CSS file
    css_path = project_root / "assets" / "style.css"

    # Check whether CSS exists
    if not css_path.exists():
        st.warning(
            f"CSS file not found: {css_path}"
        )
        return

    # Read CSS
    with open(
        css_path,
        "r",
        encoding="utf-8"
    ) as f:

        css = f.read()

    # Apply CSS to Streamlit
    st.markdown(
        f"""
        <style>
        {css}
        </style>
        """,
        unsafe_allow_html=True
    )
