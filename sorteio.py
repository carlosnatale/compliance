
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
    - header=0 trata a primeira linha como cabeçalho.
    """
    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    # Bloco try/except corretamente fechado
    try:
        if file_name.endswith(".xlsx"):
            # openpyxl para .xlsx
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif file_name.endswith(".xls"):
            # xlrd para .xls
            df = pd.read_excel(uploaded_file, engine="xlrd")
        else:
            st.error("Formato não suportado. Envie um arquivo .xlsx ou .xls.")
            return None
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return None

# -------------------------------
# App principal
# -------------------------------

def main():
    st.set_page_config(page_title="Sorteio Aleatório de Nomes", page_icon="🎲", layout="centered")
    st.title("🎲 Sorteio Aleatório de Nomes")
    st.write("Faça o upload de um arquivo **Excel** contendo a lista de nomes.")
    st.info(
        "Deve existir **exatamente uma** coluna cujo cabeçalho (linha 1) seja **Nome** ou **Name**. "
        "O sorteio considera os dados **a partir da linha 2**."
    )

    uploaded_file = st.file_uploader("Envie um arquivo Excel (.xlsx ou .xls)", type=["xlsx", "xls"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        if df is not None and not df.empty:
            name_col = find_name_column(df)

            if name_col is None:
                st.error("O arquivo não possui uma coluna com cabeçalho 'Nome' ou 'Name'. Verifique a primeira linha do Excel.")
                return

            # A leitura com header=0 já faz com que os dados sejam a partir da linha 2 do Excel
            nomes_series = df[name_col].dropna()

            # Normalização e limpeza
            nomes = [str(x).strip() for x in nomes_series.tolist() if str(x).strip() != ""]

            if len(nomes) == 0:
                st.warning(f"A coluna **{name_col}** existe, mas não há valores de nomes (linhas de dados) para sortear.")
                return

            col1, col2 = st.columns(2)
            with col1:
                qtd_sorteados = st.number_input(
                    "Quantidade de sorteados:",
                    min_value=1,
                    max_value=len(nomes),
                    value=1,
                    step=1
                )
            with col2:
                seed_opt = st.text_input("Seed (opcional, para reprodutibilidade)", value="")

            remove_dups = st.checkbox("Remover duplicados antes do sorteio", value=True)
            if remove_dups:
                nomes = list(dict.fromkeys(nomes))  # preserva ordem e remove duplicados
                if len(nomes) < qtd_sorteados:
                    st.warning(
                        "Após remover duplicados, a quantidade de nomes ficou menor que a quantidade a sortear. "
                        "Reduza a quantidade de sorteados ou desmarque a opção de remover duplicados."
                    )
                    return

            if st.button("Sortear"):
                if seed_opt.strip():
                    random.seed(seed_opt.strip())  # strings são válidas como seeds

                sorteados = random.sample(nomes, k=qtd_sorteados)

                st.success("Nomes sorteados:")
                for nome in sorteados:
                    st.write(f"- {nome}")
        else:
            st.error("Não foi possível ler o arquivo ou o arquivo está vazio.")

if __name__ == "__main__":
    main()
