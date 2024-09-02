import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

page = ["Home", "Insights", "EduEz", "Predictions"]

styles = {
    "nav": {
        "background-color": "#73c6b6",
        "height": "60px",
        "box-shadow": "0 4px 6px rgba(0, 0, 0.1)",
        "display": "flex",
        "justify-content": "flex-start",  # Align items to the left
        "padding-left": "20px"  # Optional: Add some padding to the left
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "padding": "0.4375rem 0.625rem", 
        "margin": "0 0.125rem",
        "font-family": "'Roboto', sans-serif", 
        "font-size": "16px", 
    },
    "active": {
        "background-color": "#FFFFFF",  
    },
    "hover": {
        "background-color": "#FFFFFF", 
    },
}

page = st_navbar(page, styles=styles)

if page == "Home":
    pg.homepage()
elif page == "Insights":
    pg.EducationAnalysis()
elif page == "EduEz":
    pg.EduEz()
elif page == "Predictions":
    pg.predictions()
