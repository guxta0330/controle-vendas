import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Controle de Vendas", layout="wide")
st.title("📊 Controle de Vendas")

# ---- CARREGAR DADOS ----
# ---- CARREGAR DADOS ----
try:
    df = pd.read_csv("vendas.csv")
except:
    df = pd.DataFrame(columns=["data", "valor"])

# GARANTIR DATA CORRETA
if not df.empty:
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df.dropna(subset=["data"])

# ---- REGISTRAR VENDA ----
st.subheader("➕ Registrar nova venda")

with st.form("nova_venda"):
    data_venda = st.date_input("Data da venda", value=date.today())
    valor_venda = st.number_input("Valor da venda (R$)", min_value=0.0, step=1.0)
    salvar = st.form_submit_button("Salvar venda")

    if salvar:
        nova_linha = pd.DataFrame(
            {"data": [pd.to_datetime(data_venda)], "valor": [valor_venda]}
        )
        df = pd.concat([df, nova_linha], ignore_index=True)
        df.to_csv("vendas.csv", index=False)
        st.success("Venda registrada com sucesso!")
        st.rerun()

st.divider()

# ---- MÉTRICAS ----
if df.empty:
    total = hoje = mes = 0
else:
    total = df["valor"].sum()
    hoje = df[df["data"].dt.date == date.today()]["valor"].sum()
    mes = df[df["data"].dt.month == date.today().month]["valor"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total vendido", f"R$ {total:.2f}")
col2.metric("📅 Hoje", f"R$ {hoje:.2f}")
col3.metric("📆 Mês", f"R$ {mes:.2f}")

st.divider()

# ---- GRÁFICO ----
st.subheader("📈 Vendas por dia")
if not df.empty:
    vendas_dia = df.groupby(df["data"].dt.date)["valor"].sum()
    st.line_chart(vendas_dia)
else:
    st.info("Nenhuma venda registrada ainda.")
