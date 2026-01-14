
import streamlit as st
import pandas as pd
import random

# -------------------------------
# Funções utilitárias
# -------------------------------

def normalize_header(col_name: str) -> str:
    """Normaliza o nome da coluna removendo espaços e deixando minúsculo."""
    if not isinstance(col_name, str):
        return ""
    return col_name.strip().lower()

def find_name_column(df: pd.DataFrame):
    """
    Encontra a coluna cujo cabeçalho é 'Nome' ou 'Name'
    (case-insensitive, ignorando espaços).
    Retorna o nome exato da coluna no DataFrame ou None se não encontrado.
    """
    target_headers = {"nome", "name"}
    normalized_map = {col: normalize_header(col) for col in df.columns}
    for original_col, norm_col in normalized_map.items():
        if norm_col in target_headers:
            return original_col
    return None

def load_data(uploaded_file):
    """
    Carrega Excel (.xlsx ou .xls).
    - Usa header=0 para que a primeira linha do Excel seja tratada como cabeçalho.
    - Assim, os dados do DataFrame correspondem a partir da linha 2 do Excel.
    """
    if uploaded_file is None:
        return None

    # Tenta ambos engines conforme extensão
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif name.endswith(".xls"):
            df = pd.read_excel(uploaded_file, engine="xlrd")
        else:
            st.error("Formato não suportado. Envie um arquivo .xlsx ou .xls.")
            return None
