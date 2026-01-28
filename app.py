import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from data_loader import load_data, standardize_columns
from styles import apply_gge_styles, render_header

# --- CONFIGURATION ---
st.set_page_config(
    page_title="GGE Dashboard Premium",
    page_icon="assets/favicon.png",
    layout="wide"
)

# Spreadsheet URL from user
SHEET_URL = "https://docs.google.com/spreadsheets/d/196o1A0zn6YdDgfENaNbMxoqWEJuc02uzZTn-4yWAJ3U/edit?usp=sharing"

# --- AUTO REFRESH ---
st_autorefresh(interval=300000, key="datarefresher")

# --- DATA LOADING ---
@st.cache_data(ttl=300)
def fetch_and_process():
    raw_df = load_data(SHEET_URL)
    return standardize_columns(raw_df)

# --- UI INITIALIZATION ---
apply_gge_styles()
render_header()

df = fetch_and_process()

if df.empty:
    st.warning("⚠️ Aguardando carregamento de dados ou verifique as credenciais.")
    st.info("💡 Certifique-se de que a planilha está configurada como pública e a aba se chama 'Página1'.")
else:
    # Identify key columns
    occ_col = next((c for c in df.columns if 'OCORR' in c.upper()), None)
    status_col = next((c for c in df.columns if 'STATUS' in c.upper()), None)

    # --- HORIZONTAL FILTERS ---
    st.markdown("### 🔍 Filtros Rápidos")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        anos = ["Todos os anos"] + sorted([str(x) for x in df['ano'].unique().tolist()]) if 'ano' in df.columns else ["Todos os anos"]
        selected_year = st.selectbox("Filtrar por Ano", anos)
    
    with f_col2:
        meses = ["Todos os meses"] + sorted(df['mes'].unique().tolist()) if 'mes' in df.columns else ["Todos os meses"]
        selected_month = st.selectbox("Filtrar por Mês", meses)
        
    with f_col3:
        unidades = ["Todas as unidades"] + sorted(df['unidade'].unique().tolist()) if 'unidade' in df.columns else ["Todas as unidades"]
        selected_unit = st.selectbox("Filtrar por Unidade", unidades)

    # Apply Filtering
    filtered_df = df.copy()
    if selected_year != "Todos os anos":
        filtered_df = filtered_df[filtered_df['ano'].astype(str) == selected_year]
    if selected_month != "Todos os meses":
        filtered_df = filtered_df[filtered_df['mes'] == selected_month]
    if selected_unit != "Todas as unidades":
        filtered_df = filtered_df[filtered_df['unidade'] == selected_unit]

    # --- KPI CARDS ---
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Total de Registros</div>
                <div class='kpi-value'>{len(filtered_df)}</div>
                <div class='kpi-subtext'>registros filtrados</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k2:
        if status_col:
            resolved_pct = (len(filtered_df[filtered_df[status_col].astype(str).str.upper() == 'RESOLVIDO']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            val = f"{resolved_pct:.1f}%"
        else:
            val = "N/A"
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Taxa de Resolução</div>
                <div class='kpi-value'>{val}</div>
                <div class='kpi-subtext'>itens finalizados</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k3:
        n_units = filtered_df['unidade'].nunique() if 'unidade' in filtered_df.columns else 0
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Unidades Ativas</div>
                <div class='kpi-value'>{n_units}</div>
                <div class='kpi-subtext'>com ocorrências</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k4:
        top_u = filtered_df['unidade'].value_counts().idxmax() if not filtered_df.empty and 'unidade' in filtered_df.columns else "-"
        st.markdown(f"""
            <div class='kpi-card' style='border-top-color: #0B3D91;'>
                <div class='kpi-label'>Top Unidade</div>
                <div class='kpi-value' style='font-size: 24px;'>{top_u}</div>
                <div class='kpi-subtext'>maior volume</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ROW 1: Evolution & Types ---
    r1_c1, r1_c2 = st.columns([2, 1])

    with r1_c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("#### Evolução Mensal")
        if 'data_dt' in filtered_df.columns:
            evolution_df = filtered_df.copy()
            evolution_df['mes_ano'] = evolution_df['data_dt'].dt.strftime('%b/%y')
            # Sort by date for correct line plot
            evolution_df = evolution_df.sort_values('data_dt')
            evo_data = evolution_df.groupby('mes_ano', sort=False).size().reset_index(name='Registros')
            
            fig_line = px.line(evo_data, x='mes_ano', y='Registros', template='plotly_dark', markers=True)
            fig_line.update_traces(line_color='#E31C24', fill='tozeroy', fillcolor='rgba(227, 28, 36, 0.1)')
            fig_line.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=20, b=0), height=300,
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title=""),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="")
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Dados temporais necessários para evolução.")
        st.markdown("</div>", unsafe_allow_html=True)

    with r1_c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("#### Tipos de Ocorrência")
        if occ_col:
            occ_types = filtered_df[occ_col].value_counts().head(5).reset_index()
            occ_types.columns = ['Tipo', 'Conversão']
            fig_donut = px.pie(occ_types, values='Conversão', names='Tipo', hole=0.6, template='plotly_dark')
            fig_donut.update_traces(textinfo='none', hovertemplate="<b>%{label}</b><br>Total: %{value}<extra></extra>")
            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=300,
                showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ROW 2: Problems by Unit & General Status ---
    r2_c1, r2_c2 = st.columns([2, 1])

    with r2_c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("#### Problemas por Unidade")
        if 'unidade' in filtered_df.columns:
            unit_data = filtered_df.groupby('unidade').size().reset_index(name='Problemas')
            fig_bar = px.bar(unit_data, x='unidade', y='Problemas', template='plotly_dark')
            fig_bar.update_traces(marker_color='#E31C24', hovertemplate="<b>%{x}</b><br>Problemas: %{y}<extra></extra>")
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=20, b=0), height=300,
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title=""),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="")
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("#### Status Geral")
        if status_col:
            status_data = filtered_df[status_col].value_counts().reset_index()
            status_data.columns = ['Status', 'Total']
            fig_status = px.pie(status_data, values='Total', names='Status', hole=0.7, template='plotly_dark')
            fig_status.update_traces(textinfo='none', marker=dict(colors=['#0B3D91', '#E31C24']))
            fig_status.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=300,
                showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            # Center text for donut
            resolved_count = len(filtered_df[filtered_df[status_col].astype(str).str.upper() == 'RESOLVIDO'])
            total_count = len(filtered_df)
            res_pct = int(resolved_count/total_count*100) if total_count > 0 else 0
            fig_status.add_annotation(text=f"{res_pct}%<br>RESOLVIDOS", showarrow=False, font_size=20, font_color="white")
            
            st.plotly_chart(fig_status, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ROW 3: Recent Table & Performance Table ---
    r3_c1, r3_c2 = st.columns([1, 1])

    with r3_c1:
        st.markdown("#### 📋 Ocorrências Recentes")
        display_cols = ['data', 'unidade', occ_col, status_col]
        display_cols = [c for c in display_cols if c in filtered_df.columns]
        st.dataframe(filtered_df[display_cols].head(10), use_container_width=True, hide_index=True)

    with r3_c2:
        st.markdown("#### 📈 Desempenho por Unidade")
        if 'unidade' in filtered_df.columns:
            perf_df = filtered_df.groupby('unidade').agg(
                Total=('unidade', 'count')
            ).reset_index()
            
            if status_col:
                norms = filtered_df[filtered_df[status_col].astype(str).str.upper() == 'RESOLVIDO'].groupby('unidade').size().reset_index(name='Normais')
                probs = filtered_df[filtered_df[status_col].astype(str).str.upper() != 'RESOLVIDO'].groupby('unidade').size().reset_index(name='Problemas')
                perf_df = perf_df.merge(norms, on='unidade', how='left').merge(probs, on='unidade', how='left').fillna(0)
                perf_df['% Normal'] = (perf_df['Normais'] / perf_df['Total'] * 100).round(1).astype(str) + "%"
            
            st.dataframe(perf_df, use_container_width=True, hide_index=True)

    # Footer
    st.markdown(f"""
        <div style='text-align: right; color: #a0aec0; font-size: 0.8em; margin-top: 20px;'>
            Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        </div>
    """, unsafe_allow_html=True)
