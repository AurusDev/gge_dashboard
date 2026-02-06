import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
from data_loader import load_data, standardize_columns
from styles import apply_gge_styles, render_header

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Painel DOT 7 (GGE)",
    page_icon="assets/favicon.png",
    layout="wide"
)

# Spreadsheet URL from user
SHEET_URL = "https://docs.google.com/spreadsheets/d/196o1A0zn6YdDgfENaNbMxoqWEJuc02uzZTz-4yWAJ3U/edit?usp=sharing"


# --- AUTO REFRESH ---
st_autorefresh(interval=300000, key="datarefresher")

# --- DATA LOADING ---
@st.cache_data(ttl=60)  # Reduced TTL for more frequent updates
def fetch_and_process():
    raw_df = load_data(SHEET_URL)
    df = standardize_columns(raw_df)
    if not df.empty and 'data_dt' in df.columns:
        df = df.sort_values('data_dt', ascending=False)
    return df

# --- PLOTLY THEME ---
def apply_plotly_theme(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#F8FAFC"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(size=10)),
        hoverlabel=dict(bgcolor="#1E293B", font_size=12, font_family="Inter")
    )
    if hasattr(fig, "update_xaxes"):
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)', zeroline=False, showline=False)
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', zeroline=False, showline=False)
    return fig

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

    # --- FILTERS TOOLBAR ---
    st.markdown("<div class='filter-bar'>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3, f_col4 = st.columns([1, 1, 1, 0.8])
    
    with f_col1:
        anos = ["Todos os anos"] + sorted([str(x) for x in df['ano'].unique().tolist()]) if 'ano' in df.columns else ["Todos os anos"]
        selected_year = st.selectbox("📅 Ano", anos)
    
    with f_col2:
        month_order = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        available_months = sorted(df['mes'].unique().tolist(), key=lambda m: month_order.index(m) if m in month_order else 99) if 'mes' in df.columns else []
        meses = ["Todos os meses"] + available_months
        selected_month = st.selectbox("📆 Mês", meses)
        
    with f_col3:
        unidades = ["Todas as unidades"] + sorted(df['unidade'].unique().tolist()) if 'unidade' in df.columns else ["Todas as unidades"]
        selected_unit = st.selectbox("🏢 Unidade", unidades)
        
    # Apply Filtering
    filtered_df = df.copy()
    if selected_year != "Todos os anos":
        filtered_df = filtered_df[filtered_df['ano'].astype(str) == selected_year]
    if selected_month != "Todos os meses":
        filtered_df = filtered_df[filtered_df['mes'] == selected_month]
    if selected_unit != "Todas as unidades":
        filtered_df = filtered_df[filtered_df['unidade'] == selected_unit]

    with f_col4:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Exportar CSV",
            data=csv,
            file_name=f"relatorio_gge_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # --- KPI CARDS ---
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
            <div class='tooltip'>
                <div class='kpi-card'>
                    <div class='kpi-icon-row'>
                        <span class='kpi-label'>Total Registros</span>
                        <i class='fas fa-database kpi-icon'></i>
                    </div>
                    <div class='kpi-value'>{len(filtered_df)}</div>
                    <div class='kpi-subtext'>ocorrências registradas</div>
                </div>
                <span class='tooltiptext'>Volume total de entradas com base nos filtros selecionados.</span>
            </div>
        """, unsafe_allow_html=True)
        
    with k2:
        if status_col:
            resolved_pct = (len(filtered_df[filtered_df[status_col].astype(str).str.upper() == 'RESOLVIDO']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            val = f"{resolved_pct:.1f}%"
        else:
            val = "N/A"
        st.markdown(f"""
            <div class='tooltip'>
                <div class='kpi-card'>
                    <div class='kpi-icon-row'>
                        <span class='kpi-label'>Resolvidos</span>
                        <i class='fas fa-check-circle kpi-icon'></i>
                    </div>
                    <div class='kpi-value'>{val}</div>
                    <div class='kpi-subtext'>taxa de finalização</div>
                </div>
                <span class='tooltiptext'>Percentual de ocorrências marcadas como 'RESOLVIDO'.</span>
            </div>
        """, unsafe_allow_html=True)
        
    with k3:
        n_units = filtered_df['unidade'].nunique() if 'unidade' in filtered_df.columns else 0
        st.markdown(f"""
            <div class='tooltip'>
                <div class='kpi-card'>
                    <div class='kpi-icon-row'>
                        <span class='kpi-label'>Unidades</span>
                        <i class='fas fa-school kpi-icon'></i>
                    </div>
                    <div class='kpi-value'>{n_units}</div>
                    <div class='kpi-subtext'>campus com dados</div>
                </div>
                <span class='tooltiptext'>Quantidade de unidades escolares diferentes representadas nos dados.</span>
            </div>
        """, unsafe_allow_html=True)
        
    with k4:
        top_u = filtered_df['unidade'].value_counts().idxmax() if not filtered_df.empty and 'unidade' in filtered_df.columns else "-"
        st.markdown(f"""
            <div class='tooltip'>
                <div class='kpi-card'>
                    <div class='kpi-icon-row'>
                        <span class='kpi-label'>Principal Unidade</span>
                        <i class='fas fa-star kpi-icon'></i>
                    </div>
                    <div class='kpi-value' style='font-size: 1.5rem;'>{top_u}</div>
                    <div class='kpi-subtext'>maior volume registrado</div>
                </div>
                <span class='tooltiptext'>A unidade com o maior número total de ocorrências.</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 1: Evolution & Types ---
    r1_c1, r1_c2 = st.columns([2, 1])

    with r1_c1:
        st.markdown(f"""
            <div class='chart-card'>
                <div class='chart-title'><i class='fas fa-chart-line'></i> Evolução Temporal</div>
        """, unsafe_allow_html=True)
        if 'data_dt' in filtered_df.columns:
            evolution_df = filtered_df.copy()
            evolution_df['mes_ano'] = evolution_df['data_dt'].dt.strftime('%b/%y')
            evolution_df = evolution_df.sort_values('data_dt')
            evo_data = evolution_df.groupby('mes_ano', sort=False).size().reset_index(name='Registros')
            
            fig_line = px.line(evo_data, x='mes_ano', y='Registros', markers=True)
            fig_line.update_traces(
                line=dict(color='#E31C24', width=3),
                marker=dict(size=8, color='#0B3D91', line=dict(width=2, color='white')),
                fill='tozeroy', fillcolor='rgba(227, 28, 36, 0.1)',
                hovertemplate="<b>Mês:</b> %{x}<br><b>Registros:</b> %{y}<extra></extra>"
            )
            st.plotly_chart(apply_plotly_theme(fig_line), use_container_width=True)
        else:
            st.info("Dados temporais necessários para evolução.")
        st.markdown("</div>", unsafe_allow_html=True)

    with r1_c2:
        st.markdown(f"""
            <div class='chart-card'>
                <div class='chart-title'><i class='fas fa-list-ul'></i> Tipos Frequentes</div>
        """, unsafe_allow_html=True)
        if occ_col:
            occ_types = filtered_df[occ_col].value_counts().head(5).reset_index()
            occ_types.columns = ['Tipo', 'Total']
            fig_donut = px.pie(occ_types, values='Total', names='Tipo', hole=0.7)
            fig_donut.update_traces(
                textinfo='none', 
                marker=dict(colors=['#0B3D91', '#E31C24', '#1E293B', '#334155', '#475569']),
                hovertemplate="<b>Tipo:</b> %{label}<br><b>Total:</b> %{value}<extra></extra>"
            )
            st.plotly_chart(apply_plotly_theme(fig_donut), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ROW 2: Problems by Unit & General Status ---
    r2_c1, r2_c2 = st.columns([1, 1])

    with r2_c1:
        st.markdown(f"""
            <div class='chart-card'>
                <div class='chart-title'><i class='fas fa-chart-bar'></i> Volume por Unidade</div>
        """, unsafe_allow_html=True)
        if 'unidade' in filtered_df.columns:
            unit_data = filtered_df.groupby('unidade').size().reset_index(name='Problemas').sort_values('Problemas', ascending=False)
            fig_bar = px.bar(unit_data, x='unidade', y='Problemas', category_orders={"unidade": unit_data['unidade'].tolist()})
            fig_bar.update_traces(
                marker_color='#0B3D91', 
                marker_line_color='#E31C24', 
                marker_line_width=1.5,
                hovertemplate="<b>Unidade:</b> %{x}<br><b>Problemas:</b> %{y}<extra></extra>"
            )
            st.plotly_chart(apply_plotly_theme(fig_bar), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_c2:
        st.markdown(f"""
            <div class='chart-card'>
                <div class='chart-title'><i class='fas fa-circle-notch'></i> Status das Demandas</div>
        """, unsafe_allow_html=True)
        if status_col:
            status_data = filtered_df[status_col].value_counts().reset_index()
            status_data.columns = ['Status', 'Total']
            fig_status = px.pie(status_data, values='Total', names='Status', hole=0.8)
            fig_status.update_traces(
                textinfo='none', 
                marker=dict(colors=['#0B3D91', '#E31C24']),
                hovertemplate="<b>Status:</b> %{label}<br><b>Total:</b> %{value}<extra></extra>"
            )
            
            # Center text for donut
            resolved_count = len(filtered_df[filtered_df[status_col].astype(str).str.upper() == 'RESOLVIDO'])
            total_count = len(filtered_df)
            res_pct = int(resolved_count/total_count*100) if total_count > 0 else 0
            fig_status.add_annotation(text=f"<b>{res_pct}%</b><br>RESOLVIDO", showarrow=False, font_size=16, font_color="#F8FAFC")
            
            st.plotly_chart(apply_plotly_theme(fig_status), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ROW 3: Data Tables ---
    tab1, tab2 = st.tabs(["📋 Ocorrências Detalhadas", "📊 Performance por Unidade"])
    
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        display_cols = ['data', 'unidade', occ_col, status_col]
        display_cols = [c for c in display_cols if c in filtered_df.columns]
        st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if 'unidade' in filtered_df.columns:
            perf_df = filtered_df.groupby('unidade').agg(Total=('unidade', 'count')).reset_index()
            if status_col:
                norms = filtered_df[filtered_df[status_col].astype(str).str.upper() == 'RESOLVIDO'].groupby('unidade').size().reset_index(name='Resolvidos')
                perf_df = perf_df.merge(norms, on='unidade', how='left').fillna(0)
                perf_df['Taxa %'] = (perf_df['Resolvidos'] / perf_df['Total'] * 100).round(1).astype(str) + "%"
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer with timezone correction
    brazil_tz = pytz.timezone('America/Sao_Paulo')
    now_br = datetime.now(brazil_tz)
    
    st.markdown(f"""
        <div style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px;'>
            <i class='fas fa-clock'></i> Última atualização: {now_br.strftime('%d/%m/%Y %H:%M:%S')} | <b>GGE BI Solution</b>
        </div>
    """, unsafe_allow_html=True)
