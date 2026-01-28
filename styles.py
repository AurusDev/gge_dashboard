import streamlit as st

def apply_gge_styles():
    """
    Applies GGE visual identity using a Premium Dark Theme.
    """
    # Color Palette
    gge_blue_dark = "#051C3F"
    gge_blue_bright = "#0B3D91"
    gge_red = "#E31C24"
    gge_text_main = "#E2E8F0"
    gge_text_muted = "#A0AEC0"
    gge_card_bg = "#1A202C"
    gge_bg = "#0F172A"

    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

            /* Main Background */
            .stApp {{
                background-color: {gge_bg};
                color: {gge_text_main};
                font-family: 'Inter', sans-serif;
            }}
            
            /* Sidebar and Sidebar components */
            [data-testid="stSidebar"] {{
                background-color: {gge_card_bg};
                border-right: 1px solid #2D3748;
            }}

            /* Headers */
            h1, h2, h3 {{
                color: {gge_text_main} !important;
                font-weight: 600 !important;
            }}

            /* KPI Cards Style */
            .kpi-container {{
                display: flex;
                gap: 15px;
                margin-bottom: 25px;
            }}
            
            .kpi-card {{
                background-color: {gge_card_bg};
                padding: 20px;
                border-radius: 12px;
                border-top: 3px solid {gge_red};
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                flex: 1;
                min-width: 200px;
                transition: transform 0.2s;
            }}
            
            .kpi-card:hover {{
                transform: translateY(-5px);
            }}
            
            .kpi-value {{
                font-size: 32px;
                font-weight: 700;
                color: {gge_text_main};
                margin: 5px 0;
            }}
            
            .kpi-label {{
                font-size: 12px;
                color: {gge_text_muted};
                text-transform: uppercase;
                letter-spacing: 1.2px;
                font-weight: 600;
            }}
            
            .kpi-subtext {{
                font-size: 11px;
                color: {gge_text_muted};
                margin-top: 5px;
            }}

            /* Charts Container */
            .chart-card {{
                background-color: {gge_card_bg};
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                margin-bottom: 20px;
            }}

            /* Tables */
            .stDataFrame {{
                border-radius: 10px;
                overflow: hidden;
                border: 1px solid #2D3748;
            }}
            
            /* Hide Streamlit elements */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}

            /* Metric Redesign */
            [data-testid="stMetricValue"] {{
                font-size: 28px !important;
                font-weight: 700 !important;
                color: {gge_text_main} !important;
            }}
            
            [data-testid="stMetricLabel"] {{
                color: {gge_text_muted} !important;
            }}

            /* Custom Header */
            .main-header {{
                background: linear-gradient(90deg, {gge_blue_bright}, {gge_blue_dark});
                padding: 10px 30px;
                border-radius: 15px;
                color: white;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 30px;
                box-shadow: 0 8px 32px rgba(11, 61, 145, 0.2);
            }}
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """
    Renders the premium dashboard header.
    """
    logo_path = "assets/logo.jpg"
    
    col_logo, col_text = st.columns([1, 7])
    
    with col_logo:
        st.image(logo_path, width=140)
        
    with col_text:
        st.markdown(f"""
            <div style='background: linear-gradient(90deg, #0B3D91, #051C3F); padding: 20px 30px; border-radius: 15px; color: white; box-shadow: 0 8px 32px rgba(11, 61, 145, 0.2); margin-left: -20px;'>
                <h1 style='margin:0; font-size: 2.3em; color: white !important;'>Painel DOT 7</h1>
                <p style='margin:0; opacity:0.8; font-size: 1em;'>Colégio GGE - Monitoramento</p>
            </div>
        """, unsafe_allow_html=True)

