# Dashboard GGE — MVP

Este é o dashboard oficial do Colégio GGE, desenvolvido em Python utilizando Streamlit e integrado ao Google Sheets.

## 🚀 Estrutura do Projeto
- `app.py`: Ponto de entrada da aplicação, lógica de filtros e KPIs.
- `data_loader.py`: Ingestão de dados via Google Sheets e padronização de colunas.
- `styles.py`: Definição de identidade visual (CSS) e componentes de UI.
- `requirements.txt`: Dependências do sistema.

## 🛠️ Configuração e Execução

### 1. Requisitos
- Python 3.9+
- Credenciais de Service Account do Google Cloud.

### 2. Configuração do Google Sheets
1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2. Ative as APIs: **Google Sheets API** e **Google Drive API**.
3. Crie uma **Service Account** e baixe o arquivo JSON de chaves.
4. Abra a planilha do dashboard e **compartilhe** (botão Share) com o e-mail da Service Account (ex: `seunome@projeto.iam.gserviceaccount.com`).
5. Certifique-se de que a aba se chama exatamente `Planilha1`.

### 3. Rodando Localmente
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Crie uma pasta `.streamlit/` na raiz do projeto e um arquivo `secrets.toml`:
   ```toml
   [google_service_account]
   type = "service_account"
   project_id = "seu-projeto"
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "..."
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "..."
   ```
3. Execute o dashboard:
   ```bash
   streamlit run app.py
   ```

## 📈 Funcionalidades
- **Filtros Inteligentes:** Detecção automática de colunas de Ano, Mês e Unidade.
- **KPIs Dinâmicos:** Cálculo automático de Soma/Média para as 3 colunas numéricas mais relevantes.
- **Auto-Refresh:** Atualização automática a cada 5 minutos sem necessidade de recarregar a página.
- **Branding GGE:** Identidade visual baseada nas cores Azul #0B3D91 e Vermelho #E31C24.

## ✅ Checklist de Entrega
- [x] Filtros de Ano (dropdown), Mês (dropdown), Unidade (dropdown).
- [x] Leitura da aba `Planilha1`.
- [x] Auto-refresh ativo (5 min) + `st.cache_data`.
- [x] Paleta GGE aplicada via CSS.
- [x] Tratamento de erro para credenciais/planilha offline.
- [x] Exibição de timestamp da última atualização.
