import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

def get_gspread_client():
    """
    Establishes connection to Google Sheets using credentials or API Key from st.secrets.
    """
    try:
        if "google_service_account" in st.secrets:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds_dict = dict(st.secrets["google_service_account"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            return gspread.authorize(creds)
        elif "google" in st.secrets and "api_key" in st.secrets["google"]:
            # Using API Key for public sheets
            return gspread.api_key(st.secrets["google"]["api_key"])
        else:
            st.error("Credenciais (google_service_account or api_key) não encontradas em st.secrets.")
            return None
    except Exception as e:
        st.error(f"❌ Erro crítico de autenticação: {e}")
        st.info("💡 Dica: Verifique se as permissões da conta de serviço estão corretas no Google Cloud Console.")
        return None

def load_data(spreadsheet_url):
    """
    Loads data from 'Página1' of the specified Google Spreadsheet.
    """
    client = get_gspread_client()
    if not client:
        return pd.DataFrame()
        
    try:
        sh = client.open_by_url(spreadsheet_url)
        
        # Try to find 'Página1' first, else fallback to the first worksheet
        try:
            worksheet = sh.worksheet("Página1")
        except gspread.exceptions.WorksheetNotFound:
            worksheets = sh.worksheets()
            if worksheets:
                worksheet = worksheets[0]
                st.info(f"💡 Aba 'Página1' não encontrada. Usando a primeira aba: '{worksheet.title}'")
            else:
                st.error("Nenhuma aba encontrada na planilha.")
                return pd.DataFrame()

        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao acessar a planilha: {e}")
        st.info("💡 Dica: Verifique se a URL da planilha está correta e se o acesso foi compartilhado com o e-mail da conta de serviço.")
        return pd.DataFrame()

def standardize_columns(df):
    """
    Robustly detects and standardizes columns for Year, Month, and Unit.
    """
    if df.empty:
        return df

    # Standard mapping (case-insensitive)
    mapping = {
        'ano': ['ano', 'year', 'exercício', 'exercicio', 'annee'],
        'mes': ['mês', 'mes', 'month', 'período', 'periodo', 'mois'],
        'unidade': ['unidade', 'campus', 'unidade escolar', 'escola', 'unidade_escolar', 'local', 'site'],
        'data': ['data', 'date', 'timestamp', 'criado em', 'created_at', 'horário', 'horario']
    }
    
    new_cols = {}
    current_cols = [c.lower() for c in df.columns]
    
    # 1. Direct mapping
    for target, variations in mapping.items():
        for col in df.columns:
            if col.lower() in variations:
                new_cols[col] = target
                break
                
    df_mapped = df.rename(columns=new_cols)
    
    # 2. Derive from 'data' if 'ano' or 'mes' missing
    if 'data' in df_mapped.columns:
        try:
            df_mapped['data_dt'] = pd.to_datetime(df_mapped['data'], errors='coerce')
            if 'ano' not in df_mapped.columns:
                df_mapped['ano'] = df_mapped['data_dt'].dt.year.astype(str)
            if 'mes' not in df_mapped.columns:
                df_mapped['mes'] = df_mapped['data_dt'].dt.month_name()
        except:
            pass
            
    # Normalize values for filters
    if 'ano' in df_mapped.columns:
        df_mapped['ano'] = df_mapped['ano'].astype(str)
    if 'mes' in df_mapped.columns:
        df_mapped['mes'] = df_mapped['mes'].astype(str)
    if 'unidade' in df_mapped.columns:
        df_mapped['unidade'] = df_mapped['unidade'].astype(str).str.strip().str.upper()
        
    return df_mapped
