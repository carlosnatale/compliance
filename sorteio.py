import streamlit as st
import pandas as pd
import random

# Função para carregar o dataset a partir do upload do usuário
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    return None

def main():
    st.title("Sorteio Aleatório de Nomes")
    st.write("Faça o upload de um arquivo Excel contendo a lista de nomes.")
    
    uploaded_file = st.file_uploader("Envie um arquivo Excel (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None and "Nome" in df.columns:
            nomes = df["Nome"].dropna().tolist()
            
            # Selecionar a quantidade de sorteados
            qtd_sorteados = st.number_input("Quantidade de sorteados:", min_value=1, max_value=len(nomes), value=1)
            
            if st.button("Sortear"):
                sorteados = random.sample(nomes, qtd_sorteados)
                st.success("Nomes sorteados:")
                for nome in sorteados:
                    st.write(f"- {nome}")
        else:
            st.error("O arquivo enviado não contém uma coluna chamada 'Nome'.")

if __name__ == "__main__":
    main()
