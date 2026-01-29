import streamlit as st

def apply_gge_styles():
    """
    Applies GGE visual identity using a Premium Glassmorphism Theme.
    """
    # Color Palette - Premium Refined
    gge_blue_deep = "#0A0F1E"
    gge_blue_accent = "#0B3D91"
    gge_red = "#E31C24"
    gge_text_main = "#F8FAFC"
    gge_text_muted = "#94A3B8"
    gge_glass_bg = "rgba(30, 41, 59, 0.7)"
    gge_glass_border = "rgba(255, 255, 255, 0.1)"

    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

            /* Main Background */
            .stApp {{
                background: radial-gradient(circle at top left, #1E293B, #0A0F1E);
                color: {gge_text_main};
                font-family: 'Inter', sans-serif;
            }}
            
            /* Glassmorphism Generic Card */
            .glass-card {{
                background: {gge_glass_bg};
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border-radius: 16px;
                border: 1px solid {gge_glass_border};
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                padding: 24px;
                margin-bottom: 20px;
            }}

            /* KPI Design */
            .kpi-card {{
                background: {gge_glass_bg};
                backdrop-filter: blur(10px);
                border-radius: 16px;
                border: 1px solid {gge_glass_border};
                border-left: 4px solid {gge_red};
                padding: 20px;
                transition: all 0.3s ease;
                display: flex;
                flex-direction: column;
                justify-content: center;
                height: 100%;
            }}
            
            .kpi-card:hover {{
                transform: translateY(-5px);
                background: rgba(45, 55, 72, 0.8);
                border-left-width: 8px;
            }}
            
            .kpi-icon-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }}

            .kpi-icon {{
                color: {gge_red};
                font-size: 1.5rem;
                opacity: 0.8;
            }}

            .kpi-label {{
                font-size: 1rem;
                color: {gge_text_muted};
                text-transform: uppercase;
                letter-spacing: 0.12em;
                font-weight: 600;
            }}
            
            .kpi-value {{
                font-size: 2rem;
                font-weight: 700;
                color: {gge_text_main};
                margin: 0;
            }}
            
            .kpi-subtext {{
                font-size: 0.7rem;
                color: {gge_text_muted};
                margin-top: 4px;
                font-weight: 400;
            }}

            /* Custom Header */
            .main-header-container {{
                background: rgba(11, 61, 145, 0.15);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                border: 1px solid rgba(11, 61, 145, 0.3);
                padding: 25px 40px;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 30px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            }}

            .header-text h1 {{
                margin: 0;
                font-size: 3.2rem;
                background: linear-gradient(90deg, #FFFFFF, #CBD5E1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }}

            .header-text p {{
                margin: 0;
                color: {gge_text_muted};
                font-size: 1.1rem;
                letter-spacing: 0.05em;
            }}

            /* Chart Container Enhancement */
            .chart-card {{
                background: {gge_glass_bg};
                backdrop-filter: blur(10px);
                border-radius: 16px;
                border: 1px solid {gge_glass_border};
                padding: 20px;
                margin-bottom: 24px;
            }}

            .chart-title {{
                font-size: 1.6rem;
                font-weight: 600;
                color: {gge_text_main};
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 12px;
            }}

            .chart-title i {{
                color: {gge_red};
                font-size: 0.9rem;
            }}

            /* Filters Toolbar */
            .filter-bar {{
                background: rgba(15, 23, 42, 0.5);
                border: 1px solid {gge_glass_border};
                border-radius: 12px;
                padding: 15px 20px;
                margin-bottom: 25px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 15px;
            }}

            /* Tooltip container (now caption container) */
            .tooltip {{
              position: relative;
              width: 100%;
              display: block;
            }}

            .tooltip .tooltiptext {{
              visibility: visible;
              display: block;
              width: 100%;
              color: {gge_text_muted};
              text-align: left;
              margin-top: 10px;
              font-size: 0.85rem;
              font-weight: 400;
              line-height: 1.4;
              opacity: 0.9;
            }}

            .tooltip:hover .tooltiptext {{
              visibility: visible;
              opacity: 1;
            }}

            /* Export Button Styling */
            .stDownloadButton button {{
                background: rgba(227, 28, 36, 0.1) !important;
                color: {gge_red} !important;
                border: 1px solid {gge_red} !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                padding: 0.5rem 1rem !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                font-size: 0.8rem;
            }}

            .stDownloadButton button:hover {{
                background: {gge_red} !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(227, 28, 36, 0.4) !important;
                transform: translateY(-2px);
            }}

            /* Streamlit Overrides */
            div[data-testid="stMetricValue"] {{
                font-weight: 700 !important;
            }}

            /* Tab Styling - Larger and more 'Boniteza' */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 24px;
                background-color: transparent;
            }}

            .stTabs [data-baseweb="tab"] {{
                height: 50px;
                white-space: pre;
                background-color: transparent !important;
                border-radius: 8px 8px 0 0;
                gap: 8px;
                padding-top: 10px;
                padding-bottom: 10px;
            }}

            .stTabs [aria-selected="true"] {{
                background-color: rgba(227, 28, 36, 0.1) !important;
                border-bottom: 3px solid {gge_red} !important;
            }}
            
            .stTabs [data-baseweb="tab"] div p {{
                font-size: 1.6rem !important;
                font-weight: 700 !important;
                color: {gge_text_muted} !important;
            }}

            .stTabs [aria-selected="true"] div p {{
                color: {gge_red} !important;
            }}

            /* Hide Streamlit components */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
            
            /* Scrollbar Refinement */
            ::-webkit-scrollbar {{
                width: 8px;
            }}
            ::-webkit-scrollbar-track {{
                background: {gge_blue_deep};
            }}
            ::-webkit-scrollbar-thumb {{
                background: {gge_glass_border};
                border-radius: 4px;
            }}
            ::-webkit-scrollbar-thumb:hover {{
                background: {gge_text_muted};
            }}
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """
    Renders the premium dashboard header.
    """
    logo_path = "assets/logo.jpg"
    
    st.markdown(f"""
        <div class='main-header-container'>
            <img src='data:image/jpeg;base64,{get_img_base64(logo_path)}' width='140' style='border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2)'>
            <div class='header-text'>
                <h1>Painel DOT 7</h1>
                <p>Monitoramento Colégio GGE</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def get_img_base64(file_path):
    import base64
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except:
        return ""

